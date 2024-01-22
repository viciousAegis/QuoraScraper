import sys
import os
import csv

def get_users(search_query):
    with open("posts/"+search_query.replace(" ", "")+"/"+search_query.replace(" ", "")+".csv", "r", newline="", encoding="utf-8") as csvfile:
        # get all unique users
        reader = csv.DictReader(csvfile)
        
        users = []
        
        for row in reader:
            users.append(row['author'])
            
            commenters = row['commenters'].strip("][").split(', ')
            commenters = [x.strip("'") for x in commenters]
            users.extend(commenters)
            
            upvoters = row['upvoters'].strip("][").split(', ')
            upvoters = [x.strip("'") for x in upvoters]
            users.extend(upvoters)
        
        users = list(set(users))
        
        # remove empty strings
        users = [x for x in users if x]
        
        if not os.path.exists("users/user_urls/"+search_query.replace(" ", "")):
            os.makedirs("users/user_urls/"+search_query.replace(" ", ""))
        
        with open("users/user_urls/"+search_query.replace(" ", "")+"/"+search_query.replace(" ", "")+".csv", "w") as f:
            writer = csv.writer(f)
            for user in users:
                writer.writerow([user])

def get_authors(search_query):
     with open("posts/"+search_query.replace(" ", "")+"/"+search_query.replace(" ", "")+".csv", "r", newline="", encoding="utf-8") as csvfile:
        # get all unique users
        reader = csv.DictReader(csvfile)
        
        users = []
        
        for row in reader:
            users.append(row['author'])
        
        users = list(set(users))
        
        # remove empty strings
        users = [x for x in users if x]
        
        if not os.path.exists("users/user_urls/"+search_query.replace(" ", "")):
            os.makedirs("users/user_urls/"+search_query.replace(" ", ""))
        
        with open("users/user_urls/"+search_query.replace(" ", "")+"/"+search_query.replace(" ", "")+".csv", "w") as f:
            writer = csv.writer(f)
            for user in users:
                writer.writerow([user])


if __name__ == "__main__":
    search_queries = []

    with open('search.terms', 'r') as f:
        for line in f:
            search_queries.append(line.strip())
    
    for search_query in search_queries:
        get_users(search_query)