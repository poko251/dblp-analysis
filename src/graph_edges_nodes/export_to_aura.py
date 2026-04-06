import pandas as pd
from itertools import combinations

# creates csv files required to neo4j

# load and filter data
top_venues = ['NeurIPS', 'CVPR', 'ICML', 'ICSE', 'SIGGRAPH', 'KDD', 'AAAI']
df = pd.read_parquet("data/dblp_data_2015_plus.parquet")
df = df[(df['venue'].isin(top_venues)) & (df['year'] >= 2024)]

#  nodes
unique_authors = df['authors'].explode().unique()
nodes = pd.DataFrame({'id': range(len(unique_authors)), 'name': unique_authors})
name_to_id = dict(zip(nodes['name'], nodes['id']))

# edges
pairs = []
for authors in df['authors']:
    if len(authors) > 1:
        # sort to avoid duplicates like (A,B) and (B,A)
        pairs.extend([tuple(sorted(p)) for p in combinations(authors, 2)])

edges = pd.DataFrame(pairs, columns=['source', 'target'])
edges = edges.groupby(['source', 'target']).size().reset_index(name='weight')

# map names to IDs
edges['source_id'] = edges['source'].map(name_to_id)
edges['target_id'] = edges['target'].map(name_to_id)

nodes.to_csv('nodes_for_aura.csv', index=False)
edges[['source_id', 'target_id', 'weight']].to_csv('edges_for_aura.csv', index=False)
