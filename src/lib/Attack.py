import os
import pickle
from .stepModel_loader import load_stepModel
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 
import networkx as nx
import json


class Attack:
    def __init__(self, G, node_list, edge_list, legend_labels):
        """
        Initialize an Attack object with a graph (G), node and edge lists, and legend labels

        Args:
        - G: a NetworkX graph object
        - node_list: a list of Node objects
        - edge_list: a list of Edge objects
        - legend_labels: a list of strings representing the labels for the legend
        """
        self.G = G
        self.node_list = node_list
        self.edge_list = edge_list
        self.legend_labels = legend_labels

    @classmethod
    def from_stepModel(cls, stepModel_path, links_file_path):
        """
        Load a step model and associated data from JSON and links files

        Args:
        - stepModel_path: a string representing the path to the step model JSON file
        - links_file_path: a string representing the path to the links file

        Returns:
        - an Attack object
        """
        G, legend_labels, node_list, edge_list = load_stepModel(stepModel_path, links_file_path)
        return cls(G, node_list, edge_list, legend_labels)

    @classmethod
    def from_pickle(cls, pickle_file_path):
        """
        Load an Attack object from a pickle file

        Args:
        - pickle_file_path: a string representing the path to the pickle file

        Returns:
        - an Attack object
        """
        with open(pickle_file_path, "rb") as file:
            attack = pickle.load(file)
        return cls(attack.G, attack.node_list, attack.edge_list, attack.legend_labels)

    def __reduce__(self):
        """
        Specify how the object should be serialized and deserialized

        Returns:
        - a tuple containing the class and its arguments
        """
        return (self.__class__, (self.G, self.node_list, self.edge_list, self.legend_labels))

    def save_as_pickle(self, attack_name, output_directory):
        """
        Save an attack object to a pickle file

        Args:
        - attack_name: a string representing the name of the attack
        - output_directory: a string representing the path to the output directory
        """
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        attack_file_path = os.path.join(output_directory, attack_name + ".pkl")
        with open(attack_file_path, "wb") as file:
            pickle.dump(self, file)

    def save_as_json(self, filename, output_directory):
        """
        Save an attack object to a JSON file (NodeModel)

        Args:
        - filename: a string representing the name of the JSON file
        - output_directory: a string representing the path to the output directory

        Returns:
        - a dictionary representing the JSON data
        """
        attack = self

        nodes = []

        for node in attack.node_list:
            node_extracted = json.loads(node.to_json_string_with_digital_artefacts())
            nodes.append(node_extracted)

        json_data = {
            "Nodes": nodes
        }

        json_file_path = os.path.join(output_directory, filename + ".json")
        with open(json_file_path, "w") as file:
            json.dump(json_data, file)
        return json_data

    def plot(self):
        """
        Print the attack as a graph
        """
        G = self.G
        legend_labels = self.legend_labels

        plt.figure(figsize=(8, 8))

        pos = nx.circular_layout(G)
        labels = nx.get_node_attributes(G, 'label')

        handles = [mpatches.Patch(color='red', label=label) for label in legend_labels]

        plt.legend(handles=handles, title='Legend', bbox_to_anchor=(0, 0.05), loc='upper left')

        edge_labels = nx.get_edge_attributes(G, 'label')

        node_color = 'lightblue'
        node_alpha = 0.4

        edge_color = 'red'

        nx.draw(G, pos, with_labels=True, node_size=1000, node_color=node_color, alpha=node_alpha, font_size=10, labels=labels, edge_color=edge_color, width=1.0, connectionstyle="arc3, rad=0")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_weight='bold')

        plt.show()

