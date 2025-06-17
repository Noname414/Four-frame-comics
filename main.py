#!/usr/bin/env python3
"""
四格漫畫生成器 - 主程式
使用新聞標題生成四格漫畫
"""

import os
import sys
from comic_generator import ComicGenerator

def main():
    """主程式入口"""
    print("🎨 四格漫畫生成器")
    print("=" * 50)
    
    # 檢查 API 金鑰
    # api_key = os.getenv('GEMINI_API_KEY')
    # if not api_key:
    #     print("⚠️  請設定 GEMINI_API_KEY 環境變數")
    #     print("例如: export GEMINI_API_KEY='你的API金鑰'")
    #     return
    
    # 初始化生成器
    generator = ComicGenerator()
    
    # 取得使用者輸入
    if len(sys.argv) > 1:
        # 從命令列參數取得新聞標題
        news_title = " ".join(sys.argv[1:])
    else:
        # 互動式輸入
        print("請輸入新聞標題：")
        news_title = input("> ").strip()
    
    if not news_title:
        print("❌ 請提供新聞標題")
        return
    
    print(f"\n開始處理新聞標題: {news_title}")
    
    # 詢問是否使用搜尋功能
    if len(sys.argv) <= 1:  # 只有在互動模式時詢問
        search_choice = input("是否使用 Google 搜尋功能？(y/n，預設 y): ").strip().lower()
        use_search = search_choice != 'n'
    else:
        use_search = True  # 命令列模式預設使用搜尋
    
    # 生成四格漫畫
    result = generator.generate_full_comic(news_title, use_search=use_search)
    
    if result["success"]:
        print("\n🎉 生成成功！")
        print("檔案位置：")
        print(f"📄 劇本: {result['script_path']}")
        print(f"🖼️  四格漫畫: {result['image_path']}")
        
        # 顯示劇本摘要
        generator.print_script_summary(result['comic_script'])
        
    else:
        print(f"\n❌ 生成失敗: {result.get('error', '未知錯誤')}")

if __name__ == "__main__":
    main() 