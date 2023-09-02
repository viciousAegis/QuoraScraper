# Quora Scraper

## How to use

1. Install the requirements
It is recommended to use a virtual environment. Use the following command to install the requirements:
```
pip install -r requirements.txt
```

2. Configure the settings
The only script you need to run is `run.py`. You can configure the settings in the same file. The settings are as follows:
```
# The search queries to search for
queries = ["What is the best way to learn programming?", "What is the best way to learn Python?"]
# The number of posts to scrape for each query
num_posts = 10
```

3. Run the script
Run the script using the following command:
```
python run.py
```
