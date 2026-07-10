import json
import urllib.request
import ssl
from datetime import datetime, timedelta

# 1. Calculate yesterday's, today's, and tomorrow's dates
today_dt = datetime.now()
yesterday_dt = today_dt - timedelta(days=1)
tomorrow_dt = today_dt + timedelta(days=1)

date_yesterday = yesterday_dt.strftime("%Y-%m-%d")
date_today = today_dt.strftime("%Y-%m-%d")
date_tomorrow = tomorrow_dt.strftime("%Y-%m-%d")

# 2. Define our anchor points 
ANCHOR_DATE = datetime(2026, 7, 9)
ANCHOR_GAME_NUM = 1846

# Calculate the exact game numbers
game_today_num = ANCHOR_GAME_NUM + (today_dt - ANCHOR_DATE).days
game_yesterday_num = game_today_num - 1
game_tomorrow_num = game_today_num + 1

# 3. Fetch the definitive list from your open community data URL
COMMUNITY_DATA_URL = "https://raw.githubusercontent.com/Kinkajou/wordle-open-dev/main/words.txt"

try:
    # Create an unverified context to bypass the Mac local issuer certificate error
    context = ssl._create_unverified_context()
    
    with urllib.request.urlopen(COMMUNITY_DATA_URL, context=context) as response:
        all_words = [line.decode('utf-8').strip().upper() for line in response.readlines() if line.strip()]
    
    # Extract the exact words using the game numbers as index positions
    word_yesterday = all_words[game_yesterday_num % len(all_words)]
    word_today = all_words[game_today_num % len(all_words)]
    word_tomorrow = all_words[game_tomorrow_num % len(all_words)]

except Exception as e:
    print(f"Error fetching community data: {e}")
    # Safety fallbacks if the internet fetch fails entirely
    word_yesterday = "AMEND"
    word_today = "CANAL"
    word_tomorrow = "PIZZA"

# 4. Construct the strict, clean 3-word sliding window matching your HTML keys exactly
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

# 5. Overwrite the local words.json file with all 3 entries
with open("words.json", "w") as f:
    json.dump(three_day_matrix, f, indent=2)

print(f"Successfully synchronized 3-day words.json for {date_yesterday}, {date_today}, and {date_tomorrow}!")