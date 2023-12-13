import json
import networkx as nx
from .Node import Node

def load_stepModel(json_file_path, links_file_path):
    """
    Load a step model from a JSON file and a links file.

    Args:
        json_file_path (str): The path to the JSON file containing the step model data.
        links_file_path (str): The path to the links file containing the step model links.

    Returns:
        tuple: A tuple containing the following elements:
            - G (networkx.DiGraph): A directed graph representing the step model.
            - legend_labels (list): A list of labels for the edges in the graph.
            - node_list (list): A list of nodes in the graph.
            - edge_list (list): A list of edges in the graph.
    """
    # Load the JSON data from the file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Create a list of substeps
    substeps = []

    # Create a dictionary to store node techniques
    node_techniques_dict = {}

    node_list = []

    edge_list = [] 

    # Iterate through the "Steps" in the JSON data
    for step in data['Steps']:
        for substep in step['Substeps']:
            substeps.append(substep)
            node_number = substep['SubstepNumber']
            node_techniques = substep['Techniques']
            node_string = substep['SubstepString']
            node_techniques_dict[node_number] = node_techniques
            node = Node(str(node_number), node_techniques, node_string)
            node_list.append(node)

    # Sort the list of substeps based on 'SubstepNumber'
    substeps.sort(key=lambda x: x['SubstepNumber'])

    # Initialize a directed graph
    G = nx.DiGraph()

    # Iterate through the sorted substeps and create nodes and edges
    previous_node = None

    for substep in substeps:
        node_number = substep['SubstepNumber']
        node_string = substep['SubstepString']

        # Convert node_number to a string to use it as a node identifier
        node_number_str = str(node_number)

        # Add the node to the graph
        G.add_node(node_number_str, label=node_number_str)

        # If we have a previous node, add an edge from the previous node to the current node
        if previous_node is not None:
            G.add_edge(str(previous_node), node_number_str)
            edge_list.append((str(previous_node), node_number_str))  # Append edge to the list

        # Update the previous node to the current node
        previous_node = node_number

    # Create a list to store legend labels
    legend_labels = []

    with open(links_file_path, 'r') as links_file:
        for line in links_file:
            link_data = line.strip().strip('{}')
            source_node, target_node = map(float, link_data.split(','))

            # Check if source and target nodes exist in the graph before adding the edge
            if str(source_node) in G.nodes and str(target_node) in G.nodes:
                edge_label = f'{chr(len(legend_labels) + 97)}'
                G.add_edge(str(source_node), str(target_node), label=edge_label)
                legend_labels.append(f'{edge_label}. {node_techniques_dict[source_node]} -> {node_techniques_dict[target_node]}')
                edge_list.append((str(source_node), str(target_node)))  # Append edge to the list
                
    return G, legend_labels, node_list, edge_list