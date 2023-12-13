import networkx as nx

def neighbor_searcher(node_number, edge_list, node_list_numbers):
    """
    Given a node number and a list of edges, returns a list of the node's neighbors.

    Args:
        node_number (int): The node number to search for neighbors.
        edge_list (list): A list of edges, where each edge is a tuple of two node numbers.
        node_list_numbers (list): A list of integers representing the node numbers of the nodes in the attack sequence.

    Returns:
        list: A list of integers representing the node numbers of the neighbors.
    """

    next_node_number = 0
    for x in node_list_numbers:
        if x > node_number:
            next_node_number = x
            break


    neighbor_set = set()
    for edge in edge_list:
        if edge[0] == node_number and edge[1] != node_number and edge[1] != next_node_number:
            neighbor_set.add(edge[1])
    neighbor_list = list(neighbor_set)
    return neighbor_list


def sequence_analysis(attack):
    """
    Analyzes the given attack sequence and returns a string containing information about each node and its neighbors.

    Parameters:
    attack (Attack): The attack sequence to analyze.

    Returns:
    str: A string containing information about each node and its neighbors.
    """
    node_list = attack.node_list
    edge_list = attack.edge_list
    neighbors_analytics = ""

    node_list_numbers = [node.node_number for node in node_list]

    for node in node_list:
        node_number = node.node_number
        neighbor_list = neighbor_searcher(node_number, edge_list, node_list_numbers)
        neighbor_node_list = []

        if len(neighbor_list) != 0:
            for neighbor in neighbor_list:
                for node2 in node_list:
                    if node2.node_number == neighbor:
                        neighbor_node_list.append(node2)

        neighbors_analytics += "--------------------------------------------------------------------------------\n"
        neighbors_analytics += f"Node: {node.node_number}\n"
        neighbors_analytics += f"\t* String: {node.node_string}\n"
        
        # Check if Techniques is a list or a string
        if isinstance(node.node_techniques, list):
            neighbors_analytics += f"\t* Technique: {', '.join(node.node_techniques)}\n"
        else:
            neighbors_analytics += f"\t* Technique: {node.node_techniques}\n"

        neighbors_analytics += f"\t* Digital Artefacts:\n"
        
        if len(node.node_digital_artefacts) == 0:
            neighbors_analytics += "\t\t- No digital artefacts\n"
        
        for da in node.node_digital_artefacts:
            neighbors_analytics += f"\t\t- {da.artefact_name} | Attributes: {da.artefact_attributes}\n"

        if len(neighbor_node_list) == 0:
            neighbors_analytics += "\t* No Hidden Neighbors\n"
        else:
            neighbors_analytics += "\t* Hidden Neighbors:\n"
            for neighbor in neighbor_node_list:
                neighbors_analytics += f"\t\t- Node: {neighbor.node_number}\n"
                neighbors_analytics += f"\t\t\t* String: {neighbor.node_string}\n"
                neighbors_analytics += f"\t\t\t* Technique: {neighbor.node_techniques[0]}\n"
                neighbors_analytics += f"\t\t\t* Digital Artefacts:\n"
                if(len(neighbor.node_digital_artefacts) == 0):
                    neighbors_analytics += "\t\t- No digital artefacts\n"
                for da in neighbor.node_digital_artefacts:
                    neighbors_analytics += f"\t\t\t\t- {da.artefact_name} | Attributes: {da.artefact_attributes}\n"

    return neighbors_analytics