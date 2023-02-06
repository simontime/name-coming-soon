import json, os

# Server registry file name
REGISTRY_FILE_NAME = "data/server_registry.json"

registry = {}

# Checks if the registry file exists
def file_exists():
    return os.path.exists(REGISTRY_FILE_NAME)

# Loads registry from file
def load_registry_from_file():
    global registry

    with open(REGISTRY_FILE_NAME) as file:
        registry = json.load(file)

# Saves registry to file
def save_registry_to_file():
    global registry

    with open(REGISTRY_FILE_NAME, "w") as file:
        json.dump(registry, file)

# Adds or changes a guild's channel in the server registry
def add_to_registry(guild, channel):
    global registry

    registry[guild] = channel

# Removes a guild from the server registry
def remove_from_registry(guild):
    global registry

    # Return False if guild not in registry
    if guild not in registry:
        return False

    # Remove guild from registry
    del registry[guild]

    return True
