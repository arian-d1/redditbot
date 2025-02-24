import praw
import re
from collections import Counter
import sys
import pandas as pd

from keys import USER_AGENT, CLIENT_ID, CLIENT_SECRET

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)

BLACKLIST = ["I", "WSB", "A", "AI", "OP", "DD", "RH", "LOL",
             "LMAO", "THE", "OTM", "ITM", "AND", "ARE" "YOLO", 
             "DCA", "FOMO", "US", "IRS", "MAX", "ELON", "OPEN",
             "YTD", "ROI", "IRA", "DTE", "GONNA", "GDP", "ATH", 
             "FBI", "YOLO", "NOT", "FOR", "LONG", "ARE", "IN",
             "DESK", "CEO", "HELP"]

def extract_tickers(text): 
    """
    Extracts all mentions of words that are 2-4 letters in length and alphabetical
    using Regular Expressions
    """
    possible_tickers = re.findall(r"\b[A-Z]{2,4}\b", text)
    
    return [ticker for ticker in possible_tickers if ticker.upper() not in BLACKLIST]

def analyze_subreddit(subreddit_name, limit):
    """
    Produces all mentions of a ticker in a given subreddit
    """
    subreddit = reddit.subreddit(subreddit_name)
    ticker_counts = Counter()

    # Check given amount of posts in the "hot" section of a subreddit
    for submission in subreddit.hot(limit=limit): 
        # Analyze title
        tickers_in_title = extract_tickers(submission.title)
        ticker_counts.update(tickers_in_title)

        # Analyze body
        tickers_in_body = extract_tickers(submission.selftext)
        result = []
        for ticker in tickers_in_body:
            if ticker not in tickers_in_body:
                result.append(ticker)
        ticker_counts.update(result)

    return ticker_counts


def main(subreddit="stocks", limit = 25):
    """
    Produces the number of mentions of unique mentions of a ticker in a subreddit
    (in the title and body of a post)
    """
    
    try:
        print(f"Analyzing {limit} posts in r/{subreddit}...")
        ticker_results = analyze_subreddit(subreddit, limit)
    except:
        print("Subreddit does not exist")
        return

    print("\nTrending Tickers:")
    for ticker, count in ticker_results.most_common(): # in descending order
        print(f"{ticker}: {count} mentions")

# Usage: python .\tickerBot.py "subreddit name" "limit"
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Incorrent usage, try: python .\\tickerBot.py \"subreddit name\" \"limit\"")
        print("Calling the search function with default arguments")
        main()
    else:
        try:
            subreddit = sys.argv[1]
            limit = int(sys.argv[2])
            main(sys.argv[1], int(sys.argv[2]))
        except ValueError:
            print("2nd argument must be an number > 0")

        
    