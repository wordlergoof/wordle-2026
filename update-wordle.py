import json
import urllib.request
import urllib.parse
import re
import ssl
from datetime import datetime, timedelta

# 1. Calculate yesterday's, today's, and tomorrow's dates
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

# 2. Build cleanly encoded search query
raw_query = f'title:"Daily Wordle #{game_tomorrow_num}"'
encoded_query = urllib.parse.quote(raw_query)
SEARCH_URL = f"https://www.reddit.com/r/wordle/search.json?q={encoded_query}&restrict_sr=on&sort=new&limit=1"

try:
    context = ssl._create_unverified_context()
    req = urllib.request.Request(
        SEARCH_URL, 
        headers={'User-Agent': 'Macintosh:WordleEntropyHelper:v1.0 (by /u/WordleDeveloper)'}
    )
    
    with urllib.request.urlopen(req, context=context) as response:
        search_data = json.loads(response.read().decode('utf-8'))
        
    children = search_data.get("data", {}).get("children", [])
    if children:
        permalink = children[0]["data"]["permalink"]
        THREAD_URL = f"https://www.reddit.com{permalink}.json"
        
        req_thread = urllib.request.Request(
            THREAD_URL, 
            headers={'User-Agent': 'Macintosh:WordleEntropyHelper:v1.0 (by /u/WordleDeveloper)'}
        )
        with urllib.request.urlopen(req_thread, context=context) as thread_resp:
            thread_data = json.loads(thread_resp.read().decode('utf-8'))
            
        raw_text_dump = json.dumps(thread_data).upper()
        
        # NEW STRATEGY: Look for standard spoiler tags >!WORD!< or escaped JSON variants \>!WORD!\<
        # The parentheses () capture ONLY the 5-letter word inside, leaving the symbols behind.
        found_solutions = re.findall(r'(?:>|\\>)\!([A-Z]{5})\!(?:<|\\<)', raw_text_dump)
        
        if found_solutions:
            # Filter out common false-positive uppercase words
            valid_words = [w for w in found_solutions if w not in ["SCORE", "LINES", "WORDS", "REPLY"]]
            if valid_words:
                word_tomorrow = valid_words[0]

except Exception as e:
    pass

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
