import pandas as pd
import numpy as np
import igraph as ig
import csv
import os
import matplotlib.pyplot as plt

class GraphConverter:
    def __init__(self, input_paths):
        self.input_paths = input_paths
        self.output_path = None
        self.df = None
        self.vertex_df = None
        self.graph = ig.Graph()
        self.users = []
        self.comments = []
        self.upvotes = []
        self.comment_edges = []
        self.upvote_edges = []
        self.weighted_edges = []
        self.clusters = None
        self.centrality_measures = None
    
    def print_stats(self):
        print(f"Users: {len(self.users)}")
        print(f"Comment Edges: {len(self.comment_edges)}")
        print(f"Upvote Edges: {len(self.upvote_edges)}")
        print(f"Unique Edges: {len(self.weighted_edges)}")
    
    
    def print_users(self):
        for user in self.users:
            print(user)
    
    def print_comments(self):
        for comment in self.comments:
            print(comment)
    def print_upvotes(self):
        for upvote in self.upvotes:
            print(upvote)
    
    def print_comment_edges(self):
        for edge in self.comment_edges:
            print(edge)
    
    def print_upvote_edges(self):
        for edge in self.upvote_edges:
            print(edge)
    
    def print_weighted_edges(self):
        for edge in self.weighted_edges:
            print(edge)
    
    def read_csv(self):
        for path in self.input_paths:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                # skip the header
                next(reader)
                for row in reader:
                    self.users.append(row['author'])
                    
                    commenters = row['commenters'].strip("][").split(', ')
                    commenters = [x.strip("'") for x in commenters]
                    self.users.extend(commenters)
                    
                    upvoters = row['upvoters'].strip("][").split(', ')
                    upvoters = [x.strip("'") for x in upvoters]
                    self.users.extend(upvoters)
                    
                    self.comments.append({
                        'author': row['author'],
                        'commenters': commenters,
                        "csv": path.split("/")[-1].split(".")[0]
                    })
                    
                    self.upvotes.append({
                        'author': row['author'],
                        'upvoters': upvoters,
                        "csv": path.split("/")[-1].split(".")[0]
                    })
        # give each user a unique id
        self.users = list(set(self.users))
        self.users = {user: i for i, user in enumerate(self.users)}
    
    def set_comment_edges(self):
        for comment in self.comments:
            for commenter in comment['commenters']:
                self.comment_edges.append((self.users[comment['author']], self.users[commenter], comment['csv']))
    
    def set_upvote_edges(self):
        for upvote in self.upvotes:
            for upvoter in upvote['upvoters']:
                self.upvote_edges.append((self.users[upvote['author']], self.users[upvoter], upvote['csv']))
    
    def set_weighted_edges(self):
        for edge in self.comment_edges:
            self.weighted_edges.append([edge[0], edge[1], 1, edge[2]])
        for edge in self.upvote_edges:
            if [edge[0], edge[1], 1, edge[2]] in self.weighted_edges:
                index = self.weighted_edges.index([edge[0], edge[1], 1, edge[2]])
                self.weighted_edges[index][2] += 1
            else:
                self.weighted_edges.append([edge[0], edge[1], 1])
        # get unique edges
        self.weighted_edges = list(set(tuple(x) for x in self.weighted_edges))
        
    def create_dataframes(self):
        # edge dataframe
        self.df = pd.DataFrame(self.weighted_edges, columns=['from', 'to', 'weight', 'label'])
        
        # vertex dataframe
        # use key as label and value as id
        self.vertex_df = pd.DataFrame(list(self.users.items()), columns=['label', 'id'])
        # reverse the columns
        self.vertex_df = self.vertex_df[['id', 'label']]
    
    def create_graph(self):
        self.graph = ig.Graph.DataFrame(self.df, directed=False)
        # print edge attributes
        print(self.graph.es.attributes())
        # print vertex attributes
        print(self.graph.vs.attributes())
    
    def plot_graph(self):
        fig, ax = plt.subplots()
        ig.plot(
            self.graph,
            target=ax,
            palette=ig.RainbowPalette(),
            vertex_size=0.2,
            edge_width=1,
            layout="kk"
        )
        plt.show()
    
    def leiden(self, resolution=0.01, n_iterations=100):
        self.clusters = self.graph.community_leiden(
            n_iterations=n_iterations,
            resolution=resolution,
            weights="weight",
        )
    
    def plot_leiden(self, pdf_path=None):
        fig, ax = plt.subplots()
        target = ax if pdf_path is None else pdf_path
        ig.plot(
            self.clusters,
            target=target,
            vertex_size=0.2,
            edge_width=1,
            layout="fr",
        )
        plt.show()
    
    def calc_centrality_measures(self):
        degree = self.graph.degree()
        closeness = self.graph.closeness()
        betweenness = self.graph.betweenness()
        eigenvector = self.graph.eigenvector_centrality()
        pagerank = self.graph.pagerank()
        self.centrality_measures = {
            'degree': degree,
            'closeness': closeness,
            'betweenness': betweenness,
            'eigenvector': eigenvector,
            'pagerank': pagerank,
        }
    
    def plot_centrality(self, measure):
        # plot each cluster separately on the same plot
        fig, ax = plt.subplots()
        for cluster in self.clusters:
            cluster_measure = [self.centrality_measures[measure][i] for i in cluster]
            subgraph = self.graph.subgraph(cluster)
            # plot only the nodes with top 10% centrality
            # subgraph = subgraph.induced_subgraph(np.argsort(cluster_measure)[-int(len(cluster_measure) * 0.1):])
            ig.plot(
                subgraph,
                target=ax,
                palette=ig.GradientPalette("red", "green", n=20),
                vertex_size=0.2,
                edge_width=0.4,
                layout="kk",
                vertex_color=list(map(int, ig.rescale(cluster_measure, (0, 19), clamp=True))),
            )
        plt.show()
    
    def print_modularity(self):
        print(self.clusters.modularity)

if __name__ == "__main__":
    
    input_paths = []
    # get all csv files in the posts directory
    for root, dirs, files in os.walk("posts"):
        for file in files:
            if file.endswith(".csv"):
                input_paths.append(os.path.join(root, file))
    
    converter = GraphConverter(input_paths)
    converter.read_csv()
    converter.set_comment_edges()
    converter.set_upvote_edges()
    converter.set_weighted_edges()
    converter.print_stats()
    converter.create_dataframes()
    converter.create_graph()
    converter.leiden(resolution=0.01, n_iterations=100)
    converter.plot_leiden()
    # converter.print_modularity()
    # converter.calc_centrality_measures()
    # converter.plot_centrality('degree')
    # converter.plot_graph()