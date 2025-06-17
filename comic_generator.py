from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from google.genai import types
from pydantic import BaseModel
from typing import List, Optional
import json
import re
from PIL import Image
from io import BytesIO
import os
from datetime import datetime

class NewsAnalysis(BaseModel):
    """新聞分析結果結構"""
    main_character: str # 主角
    action: str         # 動作/事件
    motivation: str     # 動機
    setting: str        # 場景
    result: str         # 結果
    summary: str        # 摘要

class ComicPanel(BaseModel):
    """四格漫畫單格結構"""
    panel_number: int          # 格數 (1-4)
    scene_description: str     # 畫面描述
    dialogue: str              # 對白
    narrative_function: str    # 敘事功能 (起/承/轉/合)
    english_prompt: str        # 英文圖像生成prompt

class ComicScript(BaseModel):
    """完整四格漫畫劇本"""
    title: str                 # 標題
    panels: List[ComicPanel]   # 四格內容
    overall_style: str         # 整體風格描述

class ComicGenerator:
    """四格漫畫生成器"""
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化生成器"""
        if api_key:
            os.environ['GEMINI_API_KEY'] = api_key
        self.client = genai.Client()
        self.model_id = "gemini-2.0-flash"
        self.image_model_id = "gemini-2.0-flash-preview-image-generation"
        
        # 設定 Google 搜尋工具
        self.google_search_tool = Tool(
            google_search=GoogleSearch()
        )
    
    def analyze_news_title(self, news_title: str, use_search: bool = True) -> NewsAnalysis:
        """分析新聞標題並蒐集相關資訊"""
        print(f"🔍 分析新聞標題: {news_title}")
        
        search_result = ""
        
        if use_search:
            try:
                # 步驟 1: 使用 Google 搜尋蒐集背景資訊
                search_prompt = f"""
                請分析這則新聞標題並上網搜尋相關資訊："{news_title}"
                
                請提供以下資訊的詳細分析：
                1. 主角 (人物、組織、動物等)
                2. 主要動作或事件
                3. 可能的動機或原因
                4. 事件發生的場景或背景
                5. 事件的結果或影響
                6. 整體事件摘要
                
                請基於搜尋到的資訊提供準確且詳細的分析。
                """
                
                # 使用 Google Search 搜尋資訊
                search_response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=search_prompt,
                    config=GenerateContentConfig(
                        tools=[self.google_search_tool],
                        response_modalities=["TEXT"],
                    )
                )
                
                search_result = search_response.text
                print("📊 已完成資訊搜尋，正在分析...")
                
            except Exception as e:
                print(f"⚠️  Google 搜尋失敗，使用基本分析模式: {e}")
                use_search = False
        
        # 步驟 2: 根據搜尋結果或直接基於標題進行結構化分析
        if use_search and search_result:
            analysis_prompt = f"""
            基於以下新聞標題和搜尋到的資訊，請提供結構化的分析：
            
            新聞標題："{news_title}"
            
            搜尋資訊：
            {search_result}
            
            請根據上述資訊，提供以下結構化分析：
            - main_character: 主角 (人物、組織、動物等)
            - action: 主要動作或事件
            - motivation: 可能的動機或原因
            - setting: 事件發生的場景或背景
            - result: 事件的結果或影響
            - summary: 整體事件摘要
            
            請確保分析準確且詳細。
            """
        else:
            print("📝 使用基本分析模式（無網路搜尋）")
            analysis_prompt = f"""
            請分析以下新聞標題，並提供結構化的分析：
            
            新聞標題："{news_title}"
            
            請根據標題內容，推測並提供以下結構化分析：
            - main_character: 主角 (人物、組織、動物等)
            - action: 主要動作或事件
            - motivation: 可能的動機或原因
            - setting: 事件發生的場景或背景
            - result: 事件的結果或影響
            - summary: 整體事件摘要
            
            請發揮創意，基於標題合理推測相關情節，確保分析有趣且適合創作四格漫畫。
            """
        
        analysis_response = self.client.models.generate_content(
            model=self.model_id,
            contents=analysis_prompt,
            config=GenerateContentConfig(
                response_modalities=["TEXT"],
                response_mime_type="application/json",
                response_schema=NewsAnalysis,
            )
        )
        
        return analysis_response.parsed
    
    def generate_comic_script(self, news_analysis: NewsAnalysis) -> ComicScript:
        """根據新聞分析生成四格漫畫劇本"""
        print("✍️ 生成四格漫畫劇本...")
        
        script_prompt = f"""
        根據以下新聞分析，創作一個四格漫畫劇本：
        
        新聞分析：
        - 主角: {news_analysis.main_character}
        - 動作: {news_analysis.action}
        - 動機: {news_analysis.motivation}
        - 場景: {news_analysis.setting}
        - 結果: {news_analysis.result}
        - 摘要: {news_analysis.summary}
        
        請創作一個具有「起承轉合」結構的四格漫畫：
        
        第1格 (起)：設定場景和人物，引入問題或情況
        第2格 (承)：發展情節，展現衝突或挑戰
        第3格 (轉)：意外轉折或高潮時刻
        第4格 (合)：結局，通常帶有幽默或諷刺效果
        
        每格都要包含：
        - 生動的畫面描述 (適合漫畫風格)
        - 幽默有趣的對白
        - 明確的敘事功能
        - 適合 AI 圖像生成的英文 prompt (風格：cartoon style, 4-panel comic, clear characters)
        
        整體風格要幽默諷刺，適合成人閱讀。
        標題請使用原新聞標題的簡化版本。
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=script_prompt,
            config=GenerateContentConfig(
                response_modalities=["TEXT"],
                response_mime_type="application/json",
                response_schema=ComicScript,
            )
        )
        
        return response.parsed
    
    def generate_comic_images(self, comic_script: ComicScript, output_dir: str = "comic_output") -> str:
        """根據劇本生成四格漫畫圖片（一張完整圖片）"""
        print("🎨 生成四格漫畫圖片...")
        
        # 建立輸出目錄
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        comic_dir = os.path.join(output_dir, f"comic_{timestamp}")
        os.makedirs(comic_dir, exist_ok=True)
        
        # 組合所有格子的描述為一個完整的四格漫畫 prompt
        full_comic_prompt = f"""
        Create a 4-panel comic strip layout in a single image with the following story:
        
        Title: {comic_script.title}
        Overall style: {comic_script.overall_style}
        
        Panel 1 (Top Left - {comic_script.panels[0].narrative_function}):
        Scene: {comic_script.panels[0].scene_description}
        Dialogue: "{comic_script.panels[0].dialogue}"
        
        Panel 2 (Top Right - {comic_script.panels[1].narrative_function}):
        Scene: {comic_script.panels[1].scene_description}
        Dialogue: "{comic_script.panels[1].dialogue}"
        
        Panel 3 (Bottom Left - {comic_script.panels[2].narrative_function}):
        Scene: {comic_script.panels[2].scene_description}
        Dialogue: "{comic_script.panels[2].dialogue}"
        
        Panel 4 (Bottom Right - {comic_script.panels[3].narrative_function}):
        Scene: {comic_script.panels[3].scene_description}
        Dialogue: "{comic_script.panels[3].dialogue}"
        
        Style requirements:
        - 4-panel comic strip layout (2x2 grid)
        - Clear panel borders separating each scene
        - Consistent character design across all panels
        - Clean cartoon illustration style
        - Speech bubbles with dialogue text
        - Bright, colorful, family-friendly comic art
        - Traditional manga/comic book style layout
        - Each panel should be clearly distinct but part of a cohesive story
        """
        
        try:
            print("正在生成完整的四格漫畫...")
            response = self.client.models.generate_content(
                model=self.image_model_id,
                contents=full_comic_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE', 'TEXT']
                )
            )
            
            # 儲存完整的四格漫畫圖片
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    image_path = os.path.join(comic_dir, f"4panel_comic.png")
                    image.save(image_path)
                    print(f"✅ 四格漫畫已儲存: {image_path}")
                    return image_path
                    
        except Exception as e:
            print(f"❌ 生成四格漫畫時發生錯誤: {e}")
            return None
    
    def save_script(self, comic_script: ComicScript, output_dir: str = "comic_output") -> str:
        """儲存漫畫劇本為 JSON 檔案"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_path = os.path.join(output_dir, f"comic_script_{timestamp}.json")
        
        with open(script_path, 'w', encoding='utf-8') as f:
            json.dump(comic_script.model_dump(), f, ensure_ascii=False, indent=2)
        
        return script_path
    
    def generate_full_comic(self, news_title: str, output_dir: str = "comic_output", use_search: bool = True) -> dict:
        """完整的漫畫生成流程"""
        print("🚀 開始四格漫畫生成流程...")
        print("=" * 50)
        
        try:
            # 步驟 1: 分析新聞標題
            news_analysis = self.analyze_news_title(news_title, use_search=use_search)
            print(f"✅ 新聞分析完成")
            
            # 步驟 2: 生成劇本
            comic_script = self.generate_comic_script(news_analysis)
            print(f"✅ 劇本生成完成: {comic_script.title}")
            
            # 步驟 3: 儲存劇本
            script_path = self.save_script(comic_script, output_dir)
            print(f"✅ 劇本已儲存: {script_path}")
            
            # 步驟 4: 生成圖片
            image_path = self.generate_comic_images(comic_script, output_dir)
            print(f"✅ 圖片生成完成: {image_path}")
            
            print("=" * 50)
            print("🎉 四格漫畫生成完成！")
            
            return {
                "news_analysis": news_analysis,
                "comic_script": comic_script,
                "script_path": script_path,
                "image_path": image_path,
                "success": True
            }
            
        except Exception as e:
            print(f"❌ 生成過程中發生錯誤: {e}")
            return {
                "error": str(e),
                "success": False
            }
    
    def print_script_summary(self, comic_script: ComicScript):
        """印出劇本摘要"""
        print("\n📖 漫畫劇本摘要")
        print("=" * 40)
        print(f"標題: {comic_script.title}")
        print(f"風格: {comic_script.overall_style}")
        print("\n各格內容:")
        
        for panel in comic_script.panels:
            print(f"\n第 {panel.panel_number} 格 ({panel.narrative_function}):")
            print(f"  畫面: {panel.scene_description}")
            print(f"  對白: {panel.dialogue}")
            print(f"  英文提示: {panel.english_prompt[:100]}...") 
            
if __name__ == "__main__":
    generator = ComicGenerator()
    result = generator.generate_full_comic("Trump vs. Musk: The Great Tweet War")
    if result["success"]:
        print("\n🎉 生成成功！")
        print("檔案位置：")
        print(f"📄 劇本: {result['script_path']}")
        print(f"🖼️  四格漫畫: {result['image_path']}")
        
        # 顯示劇本摘要
        generator.print_script_summary(result['comic_script'])
    else:
        print(f"\n❌ 生成失敗: {result.get('error', '未知錯誤')}")