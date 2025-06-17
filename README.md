# 🎨 四格漫畫生成器

## 一個基於 Google Gemini AI 的自動四格漫畫生成系統，能夠根據新聞標題自動創作幽默的四格漫畫

![image](image.png)
![image-1](image-1.png)

## 🎯 功能特色

### 1. 📰 智能新聞分析

- 使用 Gemini + Google Search 分析新聞標題
- 自動提取關鍵資訊：主角、動作、動機、場景、結果
- 蒐集相關背景資訊增強創作品質

### 2. ✍️ 結構化劇本生成

- 遵循「起承轉合」的四格漫畫結構
- 每格包含畫面描述、幽默對白、敘事功能
- 使用 Pydantic 模型確保輸出結構化

### 3. 🎨 AI 圖像生成

- 整合 Gemini 圖像生成模型
- 為每格生成對應的漫畫風格圖片
- 自動優化 prompt 確保視覺一致性

### 4. 📱 完整輸出管理

- 自動儲存劇本 JSON 檔案
- 圖片檔案有序命名和分類
- 支援批次處理和結果追蹤

## 🚀 快速開始

### 環境需求

- Python 3.8+
- Google Gemini API 金鑰

### 安裝

1. 使用 uv 安裝相依套件（推薦）：

```powershell
uv pip install -r requirements.txt
```

或使用 pip：

```powershell
pip install -r requirements.txt
```

### 設定 API 金鑰

```powershell
# 設定環境變數
$env:GENAI_API_KEY = "你的API金鑰"
```

或在程式中設定：

```python
import os
os.environ['GENAI_API_KEY'] = '你的API金鑰'
```

## 📖 使用方法

### 方法一：命令列使用

```powershell
# 互動式輸入
python main.py

# 直接指定新聞標題
python main.py "台積電股價創新高，投資人瘋狂搶購"
```

### 方法二：程式整合

```python
from comic_generator import ComicGenerator

# 建立生成器
generator = ComicGenerator()

# 生成四格漫畫
result = generator.generate_full_comic("你的新聞標題")

if result["success"]:
    print(f"劇本: {result['script_path']}")
    print(f"圖片: {result['image_paths']}")
```

### 方法三：Jupyter Notebook

開啟 `comic_demo.ipynb` 進行互動式測試和調整。

## 📁 專案結構

```markdown
comic-agent/
├── comic_generator.py # 主要生成器類別
├── main.py # 命令列介面
├── comic_demo.ipynb # 示範 Notebook
├── requirements.txt # Python 套件需求
├── README.md # 說明文檔
├── comic_output/ # 輸出目錄（自動建立）
│ ├── comic_20240101_120000/
│ │ ├── panel_1.png
│ │ ├── panel_2.png
│ │ ├── panel_3.png
│ │ └── panel_4.png
│ └── comic_script_20240101_120000.json
└── 參考檔案/
├── gemini_google_search_example.py
├── gemini_image_example.py
└── gemini_struct_output_example.py
```

## 🔧 API 說明

### ComicGenerator 類別

#### 初始化

```python
generator = ComicGenerator(api_key=None)
```

#### 主要方法

##### `analyze_news_title(news_title: str) -> NewsAnalysis`

分析新聞標題並蒐集相關資訊

- **參數**: `news_title` - 新聞標題字串
- **回傳**: `NewsAnalysis` 物件，包含主角、動作、動機等資訊

##### `generate_comic_script(news_analysis: NewsAnalysis) -> ComicScript`

根據新聞分析生成四格漫畫劇本

- **參數**: `news_analysis` - 新聞分析結果
- **回傳**: `ComicScript` 物件，包含完整的四格漫畫劇本

##### `generate_comic_images(comic_script: ComicScript, output_dir: str) -> List[str]`

根據劇本生成四格漫畫圖片

- **參數**:
  - `comic_script` - 漫畫劇本
  - `output_dir` - 輸出目錄路徑
- **回傳**: 圖片檔案路徑列表

##### `generate_full_comic(news_title: str, output_dir: str) -> dict`

完整的漫畫生成流程（一鍵完成）

- **參數**:
  - `news_title` - 新聞標題
  - `output_dir` - 輸出目錄（預設: "comic_output"）
- **回傳**: 包含所有結果的字典

### 資料模型

#### NewsAnalysis

```python
class NewsAnalysis(BaseModel):
    main_character: str  # 主角
    action: str         # 動作/事件
    motivation: str     # 動機
    setting: str        # 場景
    result: str         # 結果
    summary: str        # 摘要
```

#### ComicPanel

```python
class ComicPanel(BaseModel):
    panel_number: int           # 格數 (1-4)
    scene_description: str      # 畫面描述
    dialogue: str              # 對白
    narrative_function: str     # 敘事功能 (起/承/轉/合)
    english_prompt: str        # 英文圖像生成prompt
```

#### ComicScript

```python
class ComicScript(BaseModel):
    title: str                 # 標題
    panels: List[ComicPanel]   # 四格內容
    overall_style: str         # 整體風格描述
```

## 💡 使用範例

### 基本範例

```python
from comic_generator import ComicGenerator

generator = ComicGenerator()

# 步驟1: 分析新聞
news_analysis = generator.analyze_news_title("貓咪當選市長，政見是增加貓食預算")

# 步驟2: 生成劇本
comic_script = generator.generate_comic_script(news_analysis)

# 步驟3: 生成圖片
image_paths = generator.generate_comic_images(comic_script)

print(f"生成了 {len(image_paths)} 張圖片")
```

### 一鍵生成範例

```python
from comic_generator import ComicGenerator

generator = ComicGenerator()

result = generator.generate_full_comic("AI 機器人學會做珍珠奶茶，手搖店老闆緊張")

if result["success"]:
    print("生成成功！")
    generator.print_script_summary(result["comic_script"])
```

## ⚠️ 注意事項

1. **API 金鑰**: 確保正確設定 Google Gemini API 金鑰
2. **網路連線**: 需要穩定的網路連線進行 Google 搜尋和圖像生成
3. **輸出目錄**: 程式會自動建立輸出目錄，確保有寫入權限
4. **圖像生成**: 圖像生成可能需要較長時間，請耐心等待
5. **中文支援**: 系統支援繁體中文輸入和輸出

## 🔧 故障排除

### 常見問題

#### Q: 出現 "API 金鑰未設定" 錯誤

A: 請確保正確設定 `GENAI_API_KEY` 環境變數

#### Q: 圖片生成失敗

A: 檢查網路連線和 API 配額，某些複雜的 prompt 可能需要調整

#### Q: 搜尋結果不準確

A: 嘗試使用更具體的新聞標題，或手動調整分析結果

#### Q: 中文字型顯示問題

A: 確保系統安裝了適當的中文字型

## 🤝 參與開發

歡迎提交 Issue 和 Pull Request！

### 開發環境設定

```powershell
# 使用 uv 建立虛擬環境
uv venv
uv pip install -r requirements.txt
```

## 📄 授權

MIT License

## 🔗 相關連結

- [Google Gemini API 文檔](https://ai.google.dev/docs)
- [Pydantic 文檔](https://docs.pydantic.dev/)
- [PIL/Pillow 文檔](https://pillow.readthedocs.io/)

---

Made with ❤️ and AI 🤖
