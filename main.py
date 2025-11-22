import requests
from bs4 import BeautifulSoup
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
import os

# 載入 .env 檔案
load_dotenv()

# ================= 設定區 =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TARGET_CURRENCY = "SGD"                  # 新加坡幣
URL = "https://www.hsbc.com.tw/currency-rates/"
START_HOUR = 9                           # 開始時間（早上9點）
END_HOUR = 24                            # 結束時間（晚上12點 = 0點）
# =========================================

def send_telegram_notify(msg):
    """發送 Telegram 通知"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML" # 支援 HTML 格式 (粗體等)
    }
    
    try:
        resp = requests.post(url, data=payload)
        if resp.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M')}] Telegram 通知發送成功")
        else:
            print(f"發送失敗: {resp.text}")
    except Exception as e:
        print(f"Telegram 連線錯誤: {e}")

def get_hsbc_rate():
    """爬取匯豐銀行匯率"""
    print(f"[{datetime.now()}] 正在查詢匯率...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        resp = requests.get(URL, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        currency_row = None
        rows = soup.find_all('tr')
        for row in rows:
            if TARGET_CURRENCY in row.text or "新加坡幣" in row.text:
                currency_row = row
                break
        
        if currency_row:
            cols = currency_row.find_all('td')
            data = [ele.text.strip() for ele in cols]
            
            # Telegram 訊息格式 (支援 HTML <b>粗體</b>)
            rate_info = f"<b>💰 匯率到價通知</b>\n"
            rate_info += f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            rate_info += f"幣別: {TARGET_CURRENCY} (新加坡幣)\n"
            
            if len(cols) >= 3:
                # 根據經驗：cols[1] 是銀行買入, cols[2] 是銀行賣出
                # 如果您是要「新幣換台幣」，請看「銀行買入」
                buy_rate = cols[1].text.strip()
                sell_rate = cols[2].text.strip()
                
                rate_info += f"----------------------\n"
                rate_info += f"銀行跟你買 (匯率): <b>{buy_rate}</b>\n"
                rate_info += f"銀行賣給你 (匯率): <b>{sell_rate}</b>\n"
                rate_info += f"----------------------"
            else:
                rate_info += f"原始數據: {' '.join(data)}"

            return rate_info
        else:
            return "⚠️ 錯誤：找不到新加坡幣匯率，網頁可能已改版。"

    except Exception as e:
        return f"❌ 程式錯誤: {e}"

def is_within_working_hours():
    """檢查目前時間是否在運行時段內（9:00-24:00）"""
    current_hour = datetime.now().hour
    return START_HOUR <= current_hour < END_HOUR

def job():
    """執行匯率查詢並發送通知（僅在工作時段內）"""
    if not is_within_working_hours():
        print(f"[{datetime.now().strftime('%H:%M')}] 不在運行時段內，跳過本次執行")
        return

    msg = get_hsbc_rate()
    print(msg)
    send_telegram_notify(msg)

if __name__ == "__main__":
    print(f"匯率監控機器人啟動中...")
    print(f"運行時段: 每天 {START_HOUR:02d}:00 - {END_HOUR:02d}:00")
    print(f"查詢幣別: {TARGET_CURRENCY}")
    print(f"查詢頻率: 每小時一次")
    print("-" * 50)

    # 啟動時先執行一次（會檢查時段）
    job()

    # 設定每小時執行一次
    schedule.every(1).hours.do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)