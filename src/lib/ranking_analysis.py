import json

GLOBAL_RANKING_PATH = "data/output_data/global_ranking.json"

def calculate_technique_ranking(attack):
    """
    Calculates the technique ranking based on the given attack.

    Args:
        attack (Attack): The attack sequence to analyze.

    Returns:
        str: A string containing information about the technique ranking.
    """
    technique_frequency = {}

    for node in attack.node_list:
        if isinstance(node.node_techniques, list):
            techniques = node.node_techniques
        elif isinstance(node.node_techniques, str):
            techniques = [node.node_techniques]
        else:
            # Handle other types if necessary
            continue

        for technique in techniques:
            technique_frequency[technique] = technique_frequency.get(technique, 0) + 1

    sorted_ranking = sorted(technique_frequency.items(), key=lambda x: x[1], reverse=True)

    ranking_string = "* TECHNIQUE RANKING:\n"
    for rank, (technique, frequency) in enumerate(sorted_ranking, start=1):
        ranking_string += f"{rank}. {technique}: {frequency} occurrences\n"

    return ranking_string


def calculate_artefact_technique_ranking(attack):
    """
    Calculates the ranking of technique-digital_artefact pairs based on the given attack.

    Args:
        attack (Attack): The attack sequence to analyze.

    Returns:
        str: A string containing information about the technique-digital_artefact pair ranking.
    """
    artefact_technique_frequency = {}

    for node in attack.node_list:
        if isinstance(node.node_techniques, list):
            techniques = node.node_techniques
        elif isinstance(node.node_techniques, str):
            techniques = [node.node_techniques]
        else:
            # Handle other types if necessary
            continue

        if techniques:
            technique = techniques[0]
            for da in node.node_digital_artefacts:
                pair = (da.artefact_name, technique)
                artefact_technique_frequency[pair] = artefact_technique_frequency.get(pair, 0) + 1

    sorted_ranking = sorted(artefact_technique_frequency.items(), key=lambda x: x[1], reverse=True)

    ranking_string = "* TECHNIQUE-DIGITAL_ARTEFACT Pair Ranking:\n"
    for rank, ((artefact, technique), frequency) in enumerate(sorted_ranking, start=1):
        ranking_string += f"{rank}.{technique} - {artefact}: {frequency} occurrences\n"

    return ranking_string

def print_attack_rankings(attack):
    """
    Calculates and prints both the technique and artefact-technique rankings.

    Args:
        attack (Attack): The attack sequence to analyze.
    """
    technique_ranking_result = calculate_technique_ranking(attack)
    artefact_technique_ranking_result = calculate_artefact_technique_ranking(attack)

    print("### Technique Ranking ###")
    print(technique_ranking_result)

    print("### Technique-Digital_Artefact Pair Ranking ###")
    print(artefact_technique_ranking_result)

def load_global_ranking():
    """
    Loads the global ranking from a file or initializes it if the file is not found.

    Returns:
        dict: The global ranking dictionary.
    """
    try:
        with open(GLOBAL_RANKING_PATH, "r") as file:
            global_ranking = json.load(file)
    except FileNotFoundError:
        global_ranking = {"technique_ranking": None, "artefact_technique_ranking": None, "attack_count": 0}
    except json.JSONDecodeError:
        global_ranking = {"technique_ranking": None, "artefact_technique_ranking": None, "attack_count": 0}
    return global_ranking

def save_global_ranking(global_ranking):
    """
    Saves the global ranking to a file.

    Args:
        global_ranking (dict): The global ranking dictionary.
    """
    with open(GLOBAL_RANKING_PATH, "w") as file:
        json.dump(global_ranking, file)

def update_global_ranking(attack):
    """
    Updates the global ranking based on the given attack.

    Args:
        attack (Attack): The attack sequence to update the global ranking.
    """
    global_ranking = load_global_ranking()

    global_ranking["technique_ranking"] = calculate_technique_ranking(attack)
    global_ranking["artefact_technique_ranking"] = calculate_artefact_technique_ranking(attack)
    global_ranking["attack_count"] += 1

    save_global_ranking(global_ranking)

def format_technique_ranking(technique_ranking_result, attack_count):
    """
    Formats the technique ranking result in a user-friendly way.

    Args:
        technique_ranking_result (str): The raw technique ranking string.
        attack_count (int): The number of attacks the ranking is based on.

    Returns:
        str: A user-friendly formatted technique ranking string.
    """
    formatted_ranking = f"### Technique Ranking (Based on {attack_count} attacks) ###\n"
    formatted_ranking += technique_ranking_result
    return formatted_ranking

def format_artefact_technique_ranking(artefact_technique_ranking_result, attack_count):
    """
    Formats the artefact-technique pair ranking result in a user-friendly way.

    Args:
        artefact_technique_ranking_result (str): The raw artefact-technique pair ranking string.
        attack_count (int): The number of attacks the ranking is based on.

    Returns:
        str: A user-friendly formatted artefact-technique pair ranking string.
    """
    formatted_ranking = f"### Technique-Digital_Artefact Pair Ranking (Based on {attack_count} attacks) ###\n"
    formatted_ranking += artefact_technique_ranking_result
    return formatted_ranking

def print_global_ranking():
    """
    Prints the current global ranking in a user-friendly format.
    """
    global_ranking = load_global_ranking()
    formatted_technique_ranking = format_technique_ranking(global_ranking["technique_ranking"], global_ranking["attack_count"])
    formatted_artefact_technique_ranking = format_artefact_technique_ranking(global_ranking["artefact_technique_ranking"], global_ranking["attack_count"])

    print("### Global Rankings ###")
    print(formatted_technique_ranking)
    print(formatted_artefact_technique_ranking)