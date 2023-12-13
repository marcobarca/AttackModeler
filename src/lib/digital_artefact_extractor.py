from .gpt_api_call import gpt_api_call, load_prompt
from .Node import Node
from .DigitalArtefact import DigitalArtefact, get_digital_artefacts_list
import json

DIGITAL_ARTEFACT_EXTRACTOR_PROMPT_PATH = "src/lib/prompts/digital_artefact/digital_artefact_extractor_prompt.txt"
DIGITAL_ARTEFACT_ATTRIBUTE_DIRECTORY_PATH = "src/lib/prompts/digital_artefact/attributes/"

digital_artefact_extractor_prompt = load_prompt(DIGITAL_ARTEFACT_EXTRACTOR_PROMPT_PATH)

artefact_names_list = [da.artefact_name for da in get_digital_artefacts_list()]

def process_node(node):
    """
    Process a given node by extracting digital artefacts and filling their attributes.

    Args:
        node (Node): The node to be processed.

    Returns:
        Node: The processed node with filled digital artefact attributes.
    """
    print("Processing node: " + node.node_number)
    while True:
        try:
            response = gpt_api_call(prompt=digital_artefact_extractor_prompt, input_data=node.to_json_string_with_digital_artefacts_template("[]"))

            response_list = json.loads(response)
            node_artefacts_list = []
            for artefact in response_list:
                if artefact in artefact_names_list:
                    node_artefacts_list.append(artefact)

            node_template = node.to_json_string_with_digital_artefacts_template(node_artefacts_list)
            
            new_node = Node.from_json_string(node_template)
            break  # If the code executed successfully, break out of the loop
        except ValueError as ve:
            print("\tError processing digital artefacts. Retrying...")
            # Optionally, you can add a delay before retrying
            import time
            time.sleep(1)  # Sleep for 1 second before retrying


    #If the node has no digital artefacts, return the node
    if(len(node_artefacts_list)==0):
        print("\t- Number of artefacts extracted: 0")
        print("------------------------------------------------------------")
        return new_node
    print("\t- Number of artefacts extracted: " + str(len(new_node.node_digital_artefacts)))

    new_digital_artefacts = []
    count = 1
    tot = len(new_node.node_digital_artefacts)
    for digital_artefact in new_node.node_digital_artefacts:
        attribute_prompt_path = (
            DIGITAL_ARTEFACT_ATTRIBUTE_DIRECTORY_PATH + digital_artefact.artefact_name.lower() + ".txt"
        )
        attribute_prompt = load_prompt(attribute_prompt_path)

        post_prompt_1 = "\nPlease fill the node_digital_artefact attributes (empty ones) only if they are explicitely mentioned in the node_string, otherwise leave them empty.\n"
        post_prompt_2 = "node_string: " + new_node.node_string + "\n"
        post_prompt_3 = "Here's the json to fill:\n"

        while True:
            try:
                response = gpt_api_call(prompt=attribute_prompt, input_data=post_prompt_1 + post_prompt_2 + post_prompt_3 + digital_artefact.to_json_string())
                new_digital_artefacts.append(DigitalArtefact.from_json_string(response))
                print("\t\t* digital_artefact_attributes filled (" + str(count) + "/" + str(tot) + ")")
                count += 1
                break  # If the code executed successfully, break out of the loop
            except ValueError as ve:
                print("\t\tError processing digital artefact attributes. Retrying...")
                # Optionally, you can add a delay before retrying
                import time
                time.sleep(1)  # Sleep for 1 second before retrying


    new_node.node_digital_artefacts = new_digital_artefacts
    print("------------------------------------------------------------")
    return new_node

def digital_artefact_extraction(attack):
    """
    Extracts digital artefacts from the given attack object.

    Args:
        attack (Attack): The attack object to extract digital artefacts from.

    Returns:
        Attack: The updated attack object with extracted digital artefacts.
    """
    node_list = attack.node_list
    print("------------------------------------------------------------")
    new_node_list = [process_node(node) for node in node_list]
    attack.node_list = new_node_list
    return attack
