import networkx as nx
import ctgan
import random
from web3 import Web3
import json
import sys
import matplotlib.pyplot as plt

def config_tx():
    # Define the account address and private key for sending transactions
    account = '0xa48223053AAAa4EEB0A8c436679658dD0E485548'
    
    return {
    'from':account,
    'nonce': w3.eth.getTransactionCount(account),
    'gas': 300000000,
    'gasPrice': w3.toWei('0', 'gwei'),
    }


# Connect to the blockchain network and instantiate the smart contracts
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
rosca_contract_address = '0xa89e6CD81C88722ABe882624eC827B6822a0001f'
with open('rosca_abi.json') as f:
    rosca_abi = json.load(f)
rosca_contract = w3.eth.contract(address=rosca_contract_address, abi=rosca_abi)
oracle_contract_address = '0x05746168DA7f47E916D6008d30ec7ecEf5582b0f'
with open('oracle_abi.json') as f:
    oracle_abi = json.load(f)
oracle_contract = w3.eth.contract(address=oracle_contract_address, abi=oracle_abi)


# Load demo data from ctgan module
data = ctgan.load_demo()
# Keep only the columns of interest
columns = ['age', 'marital-status', 'relationship', 'capital-gain', 'capital-loss', 'hours-per-week']
data = data[columns]
data = data.sample(20)


# Fill oracle with random collateralization data
print('Filling oracle with random collateralization data')
collateralization_range = (100, 1000)
for i in range(data.shape[1]):
    print(f"User {i} ... Treatment")
    user = i
    collateralization = random.randint(*collateralization_range)
    oracle_contract.functions.setCollateralization(user, collateralization).transact(config_tx())

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

# Test collateralization and remove users with insufficient collateralization
currentRoundPot = 500
for edge in edges:
    user_i = edge[0]
    user_j = edge[1]
    collateralization_i = oracle_contract.functions.getCollateralization(user_i).call(config_tx())
    collateralization_j = oracle_contract.functions.getCollateralization(user_j).call(config_tx())
    if collateralization_i < currentRoundPot or collateralization_j < currentRoundPot:
        print(f"Removing user {user_j} due to insufficient collateralization.")
        try:
            edges.remove((user_i, user_j))
            edges.remove((user_j, user_i))
        except Exception as e:
            pass
            #print("Reverse Not found ")
            
print("Edges after Collateralization")
edges = [list(t) for t in edges]
print(edges)
# Send the list of edges to the ROSCA smart contract
print("*** Send the list of edges to the ROSCA smart contract ***")
rosca_contract.functions.form_ROSCA(edges).transact(config_tx())
memberList = rosca_contract.functions.getMemberList().call(config_tx())
print("*** Available members in ROSCA ***")
print(memberList)