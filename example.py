from src.lib.Attack import Attack
from src.lib.digital_artefact_extractor import digital_artefact_extraction
from src.lib.sequence_analysis import sequence_analysis
from src.lib.ranking_analysis import print_attack_rankings, update_global_ranking, print_global_ranking
def main():
    # # Specify the file paths
    stepModel_path = './data/input_data/StepModel2.json'
    hidden_paths_file = './data/input_data/links.txt'
    
    # Load attack from stepModel and links file
    attack = Attack.from_stepModel(stepModel_path, hidden_paths_file)

    # Extract digital artefacts (GPT)
    #attack_with_digital_artefacts = digital_artefact_extraction(attack)

    # Save attack as pickle file
    #attack_with_digital_artefacts.save_as_pickle("bodycount", "./data/output_data")

    # Load attack (with digital artefacts) from pickle file as a NodeModel
    #attack = Attack.from_pickle("./data/output_data/bodycount.pkl")

    # # Plot the graph
    #attack.plot()

    # Save attack as NodeModel json file
    #node_model = attack.save_as_json("bodycount_nodeModel_short", "./data/output_data")


    # Print the the sequence analysis
    #report = sequence_analysis(attack)
    #print(report)

    # Print attack rankings
    #print_attack_rankings(attack)

    # Update global rankings
    update_global_ranking(attack)

    # Print the global rankings
    print_global_ranking()




if __name__ == "__main__":
    main()
