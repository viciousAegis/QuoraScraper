import subprocess
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    # open file to get search terms
    
    search_queries = []

    with open('search.terms', 'r') as f:
        for line in f:
            search_queries.append(line.strip())
    
    parser.add_argument("-t", "--type", dest="type", help="type of scrape: post or user", required=True)
    # if user scrape
    parser.add_argument("-u", "--user", dest="user_url", help="user profile link")
    # if post scrape
    parser.add_argument("-c", "--count", dest="total_post_count", help="number of posts or users to scrape", default=50)
    
    args = parser.parse_args()
    
    if(args.type == "user"):
        subprocess.call(['python3', 'scraper.py', '-t', 'user', '-u', args.user_url])
        sys.exit()

    for search_query in search_queries:
        subprocess.call(['python3', 'scraper.py', '-t', 'post', '-q', search_query, '-c', args.total_post_count])