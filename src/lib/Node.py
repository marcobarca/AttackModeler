import json
from .DigitalArtefact import DigitalArtefact, get_digital_artefact

class Node:
    """
    A class representing a node in a graph.

    Attributes:
    - node_number (int): the number of the node
    - node_techniques (list): a list of techniques associated with the node
    - node_string (str): a string representing the node
    - node_digital_artefacts (list): a list of digital artefacts associated with the node

    Methods:
    - to_json_string(): returns a JSON string representation of the node object, omitting the digital artefacts
    - to_json_string_with_digital_artefacts(): returns a JSON string representation of the node object, including the digital artefacts
    - to_json_string_with_digital_artefacts_template(artefact_list): returns a JSON string representation of the node object, without filling the digital artefacts attributes
    - from_json_string(json_string): returns a Node object from a JSON string representation
    """

    def __init__(self, node_number, node_techniques, node_string, node_digital_artefacts=None):
        """
        Initializes a Node object.

        Parameters:
        - node_number (int): the number of the node
        - node_techniques (list): a list of techniques associated with the node
        - node_string (str): a string representing the node
        - node_digital_artefacts (list): a list of digital artefacts associated with the node (default: None)
        """
        self.node_number = node_number
        self.node_techniques = node_techniques
        self.node_string = node_string

        if node_digital_artefacts is None:
            self.node_digital_artefacts = []
        elif isinstance(node_digital_artefacts, list):
            self.node_digital_artefacts = node_digital_artefacts
        else:
            # Convert to a list if it's not already a list
            self.node_digital_artefacts = [node_digital_artefacts]
    
    def to_json_string(self):
        """
        Returns a JSON string representation of the node object, omitting the digital artefacts.

        Returns:
        - str: a JSON string representation of the node object
        """
        node_info = {
            "Node": {
                "node_number": self.node_number,
                "node_string": self.node_string,
                "node_techniques": self.node_techniques,
                "node_digital_artefacts": {}
            }
        }
        return json.dumps(node_info)
    
    def to_json_string_with_digital_artefacts(self):
        """
        Returns a JSON string representation of the node object, including the digital artefacts.

        Returns:
        - str: a JSON string representation of the node object
        """
        digital_artefacts_data = []

        for digital_artefact in self.node_digital_artefacts:
            digital_artefacts_data.append({digital_artefact.artefact_name: digital_artefact.artefact_attributes})

        node_info = {
            "Node": {
                "node_number": self.node_number,
                "node_string": self.node_string,
                "node_techniques": self.node_techniques,
                "node_digital_artefacts": digital_artefacts_data
            }
        }
        return json.dumps(node_info, indent=4)
    
    def to_json_string_with_digital_artefacts_template(self, artefact_list):
        """
        Returns a JSON string representation of the node object, without filling the digital artefacts attributes.

        Parameters:
        - artefact_list (list or str): a list of digital artefacts or a JSON string representation of a list of digital artefacts

        Returns:
        - str: a JSON string representation of the node object
        """
        digital_artefacts_template = []
        if(artefact_list is str):
            artefact_list = json.loads(artefact_list)
        
        if(artefact_list is not []):
            for artefact in artefact_list:
                digital_artefact = get_digital_artefact(artefact)
                if(digital_artefact is not None):
                    new_artefact = {}
                    new_artefact[artefact] = digital_artefact.artefact_attributes
                    digital_artefacts_template.append(new_artefact)

        node_info = {
            "Node": {
                "node_number": self.node_number,
                "node_string": self.node_string,
                "node_techniques": self.node_techniques,
                "node_digital_artefacts": digital_artefacts_template
            }
        }
        return json.dumps(node_info, indent=4)


    
    @classmethod
    def from_json_string(cls, json_string):
        """
        Returns a Node object from a JSON string representation.

        Parameters:
        - json_string (str): a JSON string representation of a Node object

        Returns:
        - Node: a Node object
        """
        try:
            data = json.loads(json_string)

            # Check if "Node" key is present in the JSON data
            node_data = data.get("Node", {})

            node_number = node_data.get("node_number")
            node_techniques = node_data.get("node_techniques", [])
            node_string = node_data.get("node_string", "")
            node_digital_artefacts_data = node_data.get("node_digital_artefacts", [])

            new_node_digital_artefacts = []
            
            if len(node_digital_artefacts_data) != 0:
                for artefact in node_digital_artefacts_data:
                    for artefact_name, artefact_attributes in artefact.items():
                        new_node_digital_artefacts.append(DigitalArtefact(artefact_name, artefact_attributes))

            return cls(node_number, node_techniques, node_string, new_node_digital_artefacts)
        except (json.JSONDecodeError, ValueError):
            raise ValueError("Invalid JSON content in the input string")



