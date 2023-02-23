import networkx as nx
import ctgan
import matplotlib.pyplot as plt


# Load demo data from ctgan module
data = ctgan.load_demo()
# Keep only the columns of interest
columns = ['age', 'marital-status', 'relationship', 'capital-gain', 'capital-loss', 'hours-per-week']
data = data[columns]
data = data.sample(1000)

print(f"Perform social network analysis on the data")
# Perform social network analysis on the data
G = nx.Graph()
# Add nodes to the graph
for i in range(len(data)):
    G.add_node(i)

# Add edges to the graph
for i in range(len(data)):
    for j in range(i + 1, len(data)):
        age_diff = abs(data.iloc[i]['age'] - data.iloc[j]['age'])
        if age_diff <= 5:
            G.add_edge(i, j)
        if data.iloc[i]['marital-status'] == data.iloc[j]['marital-status']:
            G.add_edge(i, j)
        if data.iloc[i]['relationship'] == data.iloc[j]['relationship']:
            G.add_edge(i, j)
        if data.iloc[i]['capital-gain'] > 0 and data.iloc[j]['capital-loss'] > 0:
            G.add_edge(i, j)
        if data.iloc[i]['hours-per-week'] == data.iloc[j]['hours-per-week']:
            G.add_edge(i, j)

# Print the number of nodes and edges in the graph
print('Number of nodes:', G.number_of_nodes())
print('Number of edges:', G.number_of_edges())

# Convert the graph to a list of edges
edges = []
for edge in G.edges:
    edges.append((edge[0], edge[1]))

print("*** Edges After Social Network Analysis ***")
print(edges)

################## Graphic Visualization of Connected Netwok
#Matplotlib
G = nx.Graph(edges)

# Compute centrality measures
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
degree_centrality = nx.degree_centrality(G)

# Compute average path distance
avg_path_length = nx.average_shortest_path_length(G)

# Perform community detection
communities = nx.algorithms.community.greedy_modularity_communities(G)

# plot degree distribution
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
plt.hist(degree_sequence, bins=20)
plt.xlabel('Degree')
plt.ylabel('Count')
plt.title('Degree Distribution')

# plot centrality measures
plt.figure()
plt.scatter(degree_centrality.values(), closeness_centrality.values(), label='Closeness')
plt.scatter(degree_centrality.values(), betweenness_centrality.values(), label='Betweenness')
plt.xlabel('Degree')
plt.ylabel('Centrality')
plt.legend()
plt.title('Node Centrality Measures')

# plot average path distance
plt.figure()
shortest_paths = [length for node in G for length in dict(nx.all_pairs_shortest_path_length(G))[node].values()]
plt.hist(shortest_paths, bins=20)
plt.xlabel('Distance')
plt.ylabel('Count')
plt.title('Average Path Distance')

# plot communities
plt.figure()
pos = nx.spring_layout(G)
for i, comm in enumerate(communities):
    nx.draw_networkx_nodes(G, pos, nodelist=list(comm), node_color=f'C{i}', alpha=0.5)
nx.draw_networkx_edges(G, pos, alpha=0.3)
plt.title('Community Detection')

plt.show()
###### End Graphic Visualization MatplotLib
