# Quora Scraper

## How to use

1. Install the requirements
It is recommended to use a virtual environment. Use the following command to install the requirements:
```
pip install -r requirements.txt
```

2. Configure the search terms
Please list the search terms in `serach.terms` with one term per line. For example:
```
python
java
c++
```

3. Run the script
Running with the `-u` flag will scrape user profiles. Otherwise, it will scrape posts.
```
usage: run.py [-h] [-c TOTAL_POST_COUNT] [-u] [-a] [-f] [-uu]
              [-t {all,year,month,week,day,hour}]

options:
  -h, --help            show this help message and exit
  -c TOTAL_POST_COUNT, --count TOTAL_POST_COUNT
                        number of posts to scrape
  -u, --user            scrape user profiles
  -a, --answer          scrape answers
  -f, --flag_user
  -uu, --user_utils
  -t {all,year,month,week,day,hour}, --timeline {all,year,month,week,day,hour}
                        timeline to scrape
```
