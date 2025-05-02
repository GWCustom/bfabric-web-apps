from bfabric import Bfabric

def get_user_input():
    """Prompt user for necessary inputs."""
    
    systems = {"TEST": "TEST", "PROD": "PRODUCTION"}

    technologies = {
        "TEST": {
            "1": "Genomics / Transcriptomics",
            "2": "Proteomics",
            "4": "Metabolomics / Biophysics",
            "6": "General",
            "10": "Bioinformatics"
        },
        "PRODUCTION": {
            "1": "Genomics / Transcriptomics",
            "2": "Proteomics",
            "4": "Metabolomics / Biophysics",
            "6": "General",
            "10": "Bioinformatics"
        }
    }

    # Get system input
    system = input("In which system do you want to create the app? (Type 'TEST' for the test system or 'PROD' for the production system): ").strip().upper()
    
    while system not in systems:
        print("Invalid input! Please enter 'TEST' or 'PROD'.")
        system = input("Enter system (TEST/PROD): ").strip().upper()

    selected_system = systems[system]  # Map input to full system name

    # Display technology options based on selected system
    print("\nAvailable Technologies:")
    for key, value in technologies[selected_system].items():
        print(f"{key}: {value}")

    # Get technology ID from user
    technologyid = input("\nEnter the number corresponding to your chosen application type: ").strip()
    
    while technologyid not in technologies[selected_system]:
        print("Invalid technology ID! Please select a valid number from the list.")
        technologyid = input("Enter a valid technology ID: ").strip()

    # Get remaining inputs
    name = input("Enter app name: ")
    weburl = input("Enter web URL: ")
    description = input("Enter description: ")

    return {
        "system": selected_system,
        "name": name,
        "weburl": weburl,
        "type": "WebApp",
        "technologyid": technologyid,
        "supervisorid": "2446",
        "enabled": True,
        "valid": True,
        "hidden": False,
        "description": description
    }

def create_app_in_bfabric():
    """Create an app in B-Fabric using user inputs."""
    # Get user input for parameters
    user_input = get_user_input()

    # Determine configuration environment based on user input
    config_env = user_input.pop("system")

    # Initialize Bfabric instance
    bfabric = Bfabric.from_config(config_env=config_env)

    # Set endpoint for app creation
    endpoint = "application"

    # Make API call to save the app
    try:
        result = bfabric.save(endpoint=endpoint, obj=user_input)
        print("App created successfully:", result)
    except Exception as e:
        print("Failed to create app:", str(e))

if __name__ == "__main__":
    create_app_in_bfabric()
