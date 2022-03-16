from collections import defaultdict
import csv
class Graph():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight
        
graph = Graph()

edges = []
coords = {}
nodes=[]
with open('C:/users/emred/downloads/Karachi_Edgelist.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
         edges.append((row['START_NODE'],row['END_NODE'],row['LENGTH']))
         if (row['XCoord'],row['YCoord']) not in coords:
             coords[row['START_NODE']] = (row['XCoord'],row['YCoord']) 

for edge in edges:
    graph.add_edge(*edge)
    
def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            #print(type(graph.weights[(current_node, next_node)]))
            #print(type(weight_to_current_node))
            weight = float(graph.weights[(current_node, next_node)]) + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

for k in range(len(dijsktra(graph, "21", "45"))):
    nodes.append(coords[dijsktra(graph, "21", "45")[k]])    

print(dijsktra(graph, "21", "45"))
print(nodes)