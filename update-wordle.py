import json
import urllib.request
from datetime import datetime, timedelta

# 1. Calculate today's and tomorrow's dates based on your Mac's current time
today_dt = datetime.now()
tomorrow_dt = today_dt + timedelta(days=1)

date_today = today_dt.strftime("%Y-%m-%d")
date_tomorrow = tomorrow_dt.strftime("%Y-%m-%d")

# 2. Define our anchor points (Update these to match your community file mapping if needed)
# Example anchor: Game 1846 is on July 9, 2026
ANCHOR_DATE = datetime(2026, 7, 9)
ANCHOR_GAME_NUM = 1846

# Calculate the exact game numbers for today and tomorrow
game_today_num = ANCHOR_GAME_NUM + (today_dt - ANCHOR_DATE).days
game_tomorrow_num = game_today_num + 1

# 3. Fetch the definitive list from your open community data URL
# (Replace this URL with your actual community data source link)
COMMUNITY_DATA_URL = "https://raw.githubusercontent.com/username/repo/main/community-words.txt"

try:
    with urllib.request.urlopen(COMMUNITY_DATA_URL) as response:
        # Assuming the file is a clean list of words, one per line
        all_words = [line.decode('utf-8').strip().upper() for line in response.readlines() if line.strip()]
    
    # Extract the exact words using the game numbers as index positions
    # (Adjust the index math if your community file starts at a different game number)
    word_today = all_words[game_today_num % len(all_words)]
    word_tomorrow = all_words[game_tomorrow_num % len(all_words)]

except Exception as e:
    print(f"Error fetching community data: {e}")
    # Safety fallbacks if the internet fetch fails, keeping your game playable
    word_today = "AMEND"
    word_tomorrow = "CANAL"

# 4. Construct the strict, clean 2-word sliding window
simplified_matrix = {
    date_today: {
        "word": word_today,
        "num": game_today_num
    },
    date_tomorrow: {
        "word": word_tomorrow,
        "num": game_tomorrow_num
    }
}

# 5. Overwrite the local words.json file with only these 2 entries
with open("words.json", "w") as f:
    json.dump(simplified_matrix, f, indent=2)

print(f"Successfully synchronized words.json for {date_today} and {date_tomorrow}!")