import subprocess
import argparse
from flask import Flask

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    # open file to get search terms
    
    search_queries = []

    with open('search.terms', 'r') as f:
        for line in f:
            search_queries.append(line.strip())

    parser.add_argument("-c", "--count", dest="total_post_count", help="number of posts to scrape", default=50)
    parser.add_argument('-u', '--user', dest='user', action='store_true', help='scrape user profiles')
    parser.add_argument('-a', '--answer', dest='answer', action='store_true', help='scrape answers')
    parser.add_argument('-f', '--flag_user', action='store_true')
    parser.add_argument('-uu', '--user_utils', action='store_true')
    parser.add_argument('-t', '--timeline', type=str, help='timeline to scrape', default='week', choices=['all', 'year', 'month', 'week', 'day', 'hour'])
    
    args = parser.parse_args()

    if args.answer:
        subprocess.call(['python3', './src/scraper.py', '-t', 'answer', '-c', str(args.total_post_count)])
        exit()

    if args.user:
        subprocess.call(['python3', './src/scraper.py', '-t', 'user'])
        exit()

    if args.user_utils:
        subprocess.call(['python3', './src/userUtils.py'])
        exit()

    if args.flag_user:
        subprocess.call(['python3', './src/scraper.py', '-t', 'user'])
        exit()
    
    subprocess.call(['python3', './src/scraper.py', '-t', 'post', '-c', str(args.total_post_count), '--timeline', args.timeline])
    
    subprocess.call(['python3', './src/userUtils.py'])
    
    subprocess.call(['python3', './src/scraper.py', '-t', 'user'])
