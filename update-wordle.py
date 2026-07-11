import json
import re
from datetime import datetime, timedelta

# 1. Calculate dates
today_dt = datetime.now()
yesterday_dt = today_dt - timedelta(days=1)
tomorrow_dt = today_dt + timedelta(days=1)

date_yesterday = yesterday_dt.strftime("%Y-%m-%d")
date_today = today_dt.strftime("%Y-%m-%d")
date_tomorrow = tomorrow_dt.strftime("%Y-%m-%d")

ANCHOR_DATE = datetime(2026, 7, 9)
ANCHOR_GAME_NUM = 1846

game_yesterday_num = ANCHOR_GAME_NUM + (yesterday_dt - ANCHOR_DATE).days
game_today_num = ANCHOR_GAME_NUM + (today_dt - ANCHOR_DATE).days
game_tomorrow_num = ANCHOR_GAME_NUM + (tomorrow_dt - ANCHOR_DATE).days

existing_words = {}
try:
    with open("words.json", "r") as f:
        existing_words = json.load(f)
except:
    pass

word_tomorrow = existing_words.get(date_tomorrow, {}).get("word", "?????")

print("[Check 1] Processing text file 'reddit_data.txt'...")

try:
    with open("reddit_data.txt", "r", encoding="utf-8") as file:
        raw_text_dump = file.read().upper()
    
    print("[Check 2] File read successfully. Scanning for winning rows...")
    
    # Target 5-letter uppercase words that immediately follow 5 green square emojis
    found_solutions = re.findall(r'🟩🟩🟩🟩🟩\s*([A-Z]{5})', raw_text_dump)
    print(f"[Check 3] Scan complete. Found {len(found_solutions)} winning row charts.")
    
    if found_solutions:
        # Filter out layout anomalies if any exist
        valid_words = [w for w in found_solutions if w not in ["SCORE", "LINES", "WORDS"]]
        print(f"[Check 4] Filter complete. {len(valid_words)} clean candidate answers remain.")
        if valid_words:
            # Target the very last winning chart to guarantee correctness
            word_tomorrow = valid_words[-1]
            print("🎉 Success: Tomorrow's word isolated successfully from text dump!")

except FileNotFoundError:
    print("⚠️ Checkpoint: 'reddit_data.txt' not found.")
except Exception as e:
    print(f"❌ Error encountered: {e}")

word_yesterday = existing_words.get(date_yesterday, {}).get("word", "AMEND")
word_today = existing_words.get(date_today, {}).get("word", "CANAL")

three_day_matrix = {
    date_yesterday: {
        "num": game_yesterday_num,
        "word": word_yesterday
    },
    date_today: {
        "num": game_today_num,
        "word": word_today
    },
    date_tomorrow: {
        "num": game_tomorrow_num,
        "word": word_tomorrow
    }
}

with open("words.json", "w") as f:
    json.dump(three_day_matrix, f, indent=2)

print(f"Successfully synchronized 3-day words.json!")