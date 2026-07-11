import json
from datetime import datetime, timedelta

# 1. Calculate the keys exactly like the main script does
today_dt = datetime.now()
date_yesterday = (today_dt - timedelta(days=1)).strftime("%Y-%m-%d")
date_today = today_dt.strftime("%Y-%m-%d")
date_tomorrow = (today_dt + timedelta(days=1)).strftime("%Y-%m-%d")

try:
    with open("words.json", "r") as f:
        data = json.load(f)
        
    # Extract the words for comparison without printing them
    word_yesterday = data.get(date_yesterday, {}).get("word", "")
    word_today = data.get(date_today, {}).get("word", "")
    word_tomorrow = data.get(date_tomorrow, {}).get("word", "")
    
    print("--- Wordle Verification Status ---")
    
    # Run the strict checks you requested
    if not word_tomorrow:
        print("❌ STATUS: Tomorrow's date entry is missing entirely from the file.")
    elif word_tomorrow == "?????":
        print("❌ STATUS: Tomorrow's word is still the default placeholder ('?????').")
    elif word_tomorrow == word_today:
        print("❌ STATUS: Tomorrow's word is an exact duplicate of today's word.")
    elif word_tomorrow == word_yesterday:
        print("❌ STATUS: Tomorrow's word is an exact duplicate of yesterday's word.")
    elif len(word_tomorrow) == 5 and word_tomorrow.isalpha():
        print("✅ SUCCESS: Tomorrow's word has been successfully updated with a fresh, hidden 5-letter answer!")
        print("   (No spoilers revealed. You are safe to play your game!)")
    else:
        print(f"⚠️ STATUS: Tomorrow's entry contains unexpected data structure.")

except FileNotFoundError:
    print("❌ ERROR: Could not find 'words.json'. Make sure you are in the correct directory.")
except Exception as e:
    print(f"❌ ERROR: An unexpected error occurred: {e}")