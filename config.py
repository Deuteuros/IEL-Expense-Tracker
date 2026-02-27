import json
import os

CONFIG_FILE = "config.json"

def get_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def update_config(key, value):
    config = get_config()
    config[key] = value
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def is_consent_given():
    config = get_config()
    return config.get("consent_accepted", False)
