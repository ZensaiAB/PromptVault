import os
import glob
from vault import BasePrompt

class PromptManager:
    def __init__(self, config_directory):
        self.config_directory = config_directory

    def load_latest_prompt(self, prompt_name) -> BasePrompt:
        """Loads the latest version of a prompt based on prompt_name."""
        files = glob.glob(os.path.join(self.config_directory, f"{prompt_name}_*.json"))
        if not files:
            raise FileNotFoundError(f"No configuration found for prompt '{prompt_name}'.")

        # Find the file with the latest version
        latest_file = max(files, key=os.path.getmtime)

        # Load the prompt from the latest file
        with open(latest_file, 'r') as file:
            json_str = file.read()

        return BasePrompt.from_json(json_str)

    def load_prompt(self, file_name) -> BasePrompt:
        """Directly loads a prompt from a specified file."""
        file_path = os.path.join(self.config_directory, file_name)
        with open(file_path, 'r') as file:
            json_str = file.read()
        
        return BasePrompt.from_json(json_str)
