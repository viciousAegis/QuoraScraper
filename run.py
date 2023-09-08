import subprocess

if __name__ == '__main__':
    search_queries = [
        'Cristiano Ronaldo',
    ]

    posts_per_query = 50

    for search_query in search_queries:
        subprocess.call(['python3', 'scraper.py', search_query, str(posts_per_query)])