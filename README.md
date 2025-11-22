# 匯率監控機器人 (Currency Rate Monitor)

自動監控匯豐銀行新加坡幣匯率，並透過 Telegram 發送通知。

## 功能特色

- 每小時自動查詢匯率
- 運行時段：每天 09:00 - 23:00（台灣時間）
- 透過 Telegram Bot 發送通知
- 使用 GitHub Actions 自動執行

## 部署到 GitHub Actions

### 1. 建立 Telegram Bot

1. 在 Telegram 搜尋 `@BotFather`
2. 發送 `/newbot` 建立新機器人
3. 取得 `BOT_TOKEN`（格式：`1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ`）
4. 在 Telegram 搜尋你的 Bot 並發送訊息 `/start`
5. 前往 `https://api.telegram.org/bot<你的BOT_TOKEN>/getUpdates` 取得 `CHAT_ID`

### 2. 設定 GitHub Secrets

1. 進入你的 GitHub Repository
2. 點選 `Settings` → `Secrets and variables` → `Actions`
3. 新增以下 Secrets：
   - `BOT_TOKEN`: 你的 Telegram Bot Token
   - `CHAT_ID`: 你的 Telegram Chat ID

### 3. 推送程式碼到 GitHub

```bash
git add .
git commit -m "Add currency rate monitor"
git push origin main
```

### 4. 啟用 GitHub Actions

1. 進入 GitHub Repository 的 `Actions` 頁面
2. 如果看到提示，點選 `I understand my workflows, go ahead and enable them`
3. Workflow 會自動執行，或手動觸發測試

### 5. 手動觸發測試

1. 進入 `Actions` 頁面
2. 選擇 `Currency Rate Monitor` workflow
3. 點選 `Run workflow` → `Run workflow`

## 本地測試

### 安裝依賴

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安裝套件
pip install -r requirements.txt
```

### 設定環境變數

建立 `.env` 檔案：

```
BOT_TOKEN=你的_BOT_TOKEN
CHAT_ID=你的_CHAT_ID
```

### 執行程式

```bash
python main.py
```

## 排程說明

GitHub Actions 使用 UTC 時區，設定為：
- Cron: `0 1-15 * * *`
- 執行時間：UTC 01:00-15:00（台灣時間 09:00-23:00）
- 頻率：每小時執行一次

## 自訂設定

修改 `main.py` 中的設定區：

```python
TARGET_CURRENCY = "SGD"  # 目標幣別
URL = "https://www.hsbc.com.tw/currency-rates/"
```

## 注意事項

- GitHub Actions 免費方案有使用時間限制（每月 2000 分鐘）
- 本程式每次執行約 10-20 秒，每天執行 15 次，每月約使用 75-150 分鐘
- 確保不要將 `.env` 檔案推送到 GitHub
