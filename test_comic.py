#!/usr/bin/env python3
"""
簡單的測試腳本 - 測試四格漫畫生成器的各項功能
"""

import os
from comic_generator import ComicGenerator

def test_news_analysis():
    """測試新聞分析功能"""
    print("🧪 測試新聞分析功能...")
    
    generator = ComicGenerator()
    test_title = "貓咪當選市長，政見是增加貓食預算"
    
    try:
        # 先嘗試使用搜尋功能
        analysis = generator.analyze_news_title(test_title, use_search=True)
        print("✅ 新聞分析測試通過（含搜尋）")
        print(f"主角: {analysis.main_character}")
        print(f"摘要: {analysis.summary}")
        return analysis
    except Exception as e:
        print(f"⚠️  搜尋模式失敗，嘗試基本模式: {e}")
        try:
            # 如果搜尋失敗，使用基本分析模式
            analysis = generator.analyze_news_title(test_title, use_search=False)
            print("✅ 新聞分析測試通過（基本模式）")
            print(f"主角: {analysis.main_character}")
            print(f"摘要: {analysis.summary}")
            return analysis
        except Exception as e2:
            print(f"❌ 新聞分析測試失敗: {e2}")
            return None

def test_script_generation(news_analysis):
    """測試劇本生成功能"""
    print("\n🧪 測試劇本生成功能...")
    
    if not news_analysis:
        print("❌ 無法測試劇本生成 - 新聞分析失敗")
        return None
    
    generator = ComicGenerator()
    
    try:
        script = generator.generate_comic_script(news_analysis)
        print("✅ 劇本生成測試通過")
        print(f"標題: {script.title}")
        print(f"總格數: {len(script.panels)}")
        return script
    except Exception as e:
        print(f"❌ 劇本生成測試失敗: {e}")
        return None

def test_full_workflow():
    """測試完整工作流程"""
    print("\n🧪 測試完整工作流程...")
    
    generator = ComicGenerator()
    test_title = "AI 機器人學會做珍珠奶茶，手搖店老闆緊張"
    
    try:
        # 只測試到劇本生成，跳過圖片生成以節省時間和 API 配額
        analysis = generator.analyze_news_title(test_title, use_search=False)  # 使用基本模式確保測試穩定
        script = generator.generate_comic_script(analysis)
        script_path = generator.save_script(script, "test_output")
        
        print("✅ 完整工作流程測試通過")
        print(f"劇本已儲存: {script_path}")
        
        # 顯示劇本摘要
        generator.print_script_summary(script)
        
        return True
    except Exception as e:
        print(f"❌ 完整工作流程測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🎨 四格漫畫生成器 - 功能測試")
    print("=" * 50)
    
    # 檢查 API 金鑰
    # if 'GENAI_API_KEY' not in os.environ:
    #     print("⚠️  請設定 GENAI_API_KEY 環境變數")
    #     print("例如: $env:GENAI_API_KEY='你的API金鑰'")
    #     return
    
    # 執行測試
    analysis = test_news_analysis()
    script = test_script_generation(analysis)
    test_full_workflow()
    
    print("\n" + "=" * 50)
    print("🎉 測試完成")
    
    # 提供下一步建議
    print("\n📝 下一步建議:")
    print("1. 執行 'python main.py' 進行互動式測試")
    print("2. 開啟 'comic_demo.ipynb' 進行進階測試")
    print("3. 嘗試不同的新聞標題測試創意效果")

if __name__ == "__main__":
    main()