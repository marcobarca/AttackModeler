import json
import re
import os

# Define the path to the digital artefacts list file
DIGITAL_ARTEFACT_LIST_PATH = "src/input_data/digital_artefacts.txt"

ATTRIBUTES_PROMPT_DIRECTORY = "src/lib/prompts/digital_artefact/attributes/"


class DigitalArtefact:
    """
    A class representing a digital artefact.

    Attributes:
    - artefact_name (str): The name of the digital artefact.
    - artefact_attributes (dict): A dictionary containing the attributes of the digital artefact.
    """

    def __init__(self, artefact_name, artefact_attributes=None):
        """
        Initializes a DigitalArtefact object.

        Parameters:
        - artefact_name (str): The name of the digital artefact.
        - artefact_attributes (dict): A dictionary containing the attributes of the digital artefact.
        """
        self.artefact_name = artefact_name

        # Initialize artefact_attributes as an empty list or with the provided data
        if artefact_attributes is None:
            self.artefact_attributes = {}
        elif isinstance(artefact_attributes, dict):
            self.artefact_attributes = artefact_attributes
        else:
            # Convert to a dict if it's not already a dict
            self.artefact_attributes = {artefact_attributes}

    def to_json_string(self):
        """
        Converts the DigitalArtefact object to a JSON string.

        Returns:
        - str: A JSON string representing the DigitalArtefact object.
        """
        # Create a dictionary representing the digital artefact
        artefact_dict = {
            "artefact_name": self.artefact_name,
            "artefact_attributes": self.artefact_attributes
        }
        # Convert the dictionary to a nicely formatted JSON string
        return json.dumps(artefact_dict)

    @classmethod
    def from_json_string(cls, input_str):
        """
        Creates a DigitalArtefact object from a JSON string.

        Parameters:
        - input_str (str): A JSON string representing a DigitalArtefact object.

        Returns:
        - DigitalArtefact: A DigitalArtefact object created from the JSON string.
        """
        # Use regular expressions to locate and extract the JSON portion
        json_match = re.search(r'\{.*\}', input_str)
        if json_match:
            json_str = json_match.group(0)
            # Parse the JSON string into a dictionary
            data = json.loads(json_str)
            # Extract the artefact_name and artefact_attributes from the dictionary
            artefact_name = data.get("artefact_name", "")
            artefact_attributes = data.get("artefact_attributes", [])
            return cls(artefact_name, artefact_attributes)
        else:
            # Handle the case where no JSON data was found
            raise ValueError("No valid JSON data found in the input string")

# Create a list to store digital artefacts
digital_artefacts_list = []

# Define a function to load digital artefacts from a file
def load_digital_artefacts_list():
    """
    Load the list of digital artifacts from a file and return it as a list of DigitalArtefact objects.

    Returns:
        list: A list of DigitalArtefact objects.
    """
    # Initialize the list to store digital artifacts
    digital_artefacts_list = []

    # Define a function to extract attributes from a line
    def extract_attributes(line):
        attributes = {}
        parts = line.split('(')
        if len(parts) > 1:
            attribute_str = parts[1].strip(')\n ')
            attributes_list = attribute_str.split(', ')
            for attribute in attributes_list:
                key, value = attribute.split('=')
                attributes[key.strip()] = value.strip('", ')
        return attributes

    # Load the list of Digital Artefacts from the file
    try:
        with open(DIGITAL_ARTEFACT_LIST_PATH, "r") as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespaces
                if line:  # Check if the line is not empty
                    parts = line.split(' ')
                    artefact_name = parts[0]
                    artefact_attributes = extract_attributes(line)
                    digital_artefacts_list.append(DigitalArtefact(artefact_name, artefact_attributes))  # Store as a tuple
    except Exception as e:
        print(f"An error occurred during the digital_artefacts_list loading: {e}")

    return digital_artefacts_list  # Return the list of digital artifacts

# Define a function to print the digital artefacts list
def print_digital_artefacts_list():
    """
    Prints all the digital artefacts in the digital_artefacts_list.
    For each artefact, it prints the artefact name and all its attributes.
    """
    # Print all the fields of each artefact
    for artefact in digital_artefacts_list:
        print(f"Artefact Name: {artefact.artefact_name}")
        for attributes in artefact.artefact_attributes:
            for key, value in attributes.items():
                print(f"\t{key}: {value}")
        print()  # Add an empty line to separate artefacts

# Define a function to generate prompts for each digital artefact
import os

def prompt_generator(artefact):
    """
    Generates a prompt file for a given digital artefact and its attributes.

    Args:
        artefact (DigitalArtefact): The digital artefact to generate a prompt for.

    Returns:
        None
    """
    # Create the directory if it doesn't exist
    os.makedirs(ATTRIBUTES_PROMPT_DIRECTORY, exist_ok=True)

    # Define the file path for the artefact
    prompt_file_path = os.path.join(ATTRIBUTES_PROMPT_DIRECTORY, f"{artefact.artefact_name}.txt")

    pre_prompt = "Considering the following digital artefact and its attributes:\n"

    # Check if the file already exists
    if not os.path.exists(prompt_file_path):
        # Create a new prompt file for the artefact
        with open(prompt_file_path, "w") as prompt_file:
            prompt_file.write(pre_prompt)
            prompt_file.write(f"Artefact Name: {artefact.artefact_name}\n")
            prompt_file.write(f"Attributes:\n")
            for attributes in artefact.artefact_attributes:
                for key, value in attributes.items():
                    prompt_file.write(f"\t- {key}\n")



def get_digital_artefacts_list():
    """
    Returns a list of digital artefacts by loading them from a data source.
    """
    return load_digital_artefacts_list()

def get_digital_artefact(artefact_name):
    """
    Returns a digital artefact object with the given name, or None if not found.

    Args:
        artefact_name (str): The name of the digital artefact to retrieve.

    Returns:
        DigitalArtefact or None: The digital artefact object with the given name, or None if not found.
    """
    digital_artefacts_list = get_digital_artefacts_list()
    for artefact in digital_artefacts_list:
        if artefact.artefact_name == artefact_name:
            return artefact
    return None

load_digital_artefacts_list()
for artefact in digital_artefacts_list:
    prompt_generator(artefact)
