import subprocess
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    # open file to get search terms
    
    search_queries = []

    with open('search.terms', 'r') as f:
        for line in f:
            search_queries.append(line.strip())

    parser.add_argument("-c", "--count", dest="total_post_count", help="number of posts to scrape", default=50)
    
    args = parser.parse_args()

    for search_query in search_queries:
        subprocess.call(['python3', 'scraper.py', '-t', 'post', '-q', search_query, '-c', args.total_post_count])
    
    subprocess.call(['python3', 'userUtils.py'])