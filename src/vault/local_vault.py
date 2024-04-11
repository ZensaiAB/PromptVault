# local_vault.py
import os
import json
from src.vault.vault import Vault
from src.template import BaseTemplate, TemplateRegistry


class LocalVault(Vault):
    def __init__(self, vault_path):
        self.vault_path = vault_path
        os.makedirs(self.vault_path, exist_ok=True)

    def save(self, template, vault_folder=None):
        template_name = template.class_name
        version = template.version
        if vault_folder:
            template_dir = os.path.join(self.vault_path, vault_folder, template_name)
        else:
            template_dir = os.path.join(self.vault_path, template_name)
        os.makedirs(template_dir, exist_ok=True)
        file_name = f"{version}.json"
        file_path = os.path.join(template_dir, file_name)
        with open(file_path, "w") as file:
            file.write(template.to_json())

    def load(self, template_name, version=None):
        template_dir = os.path.join(self.vault_path, template_name)
        if not os.path.exists(template_dir):
            raise FileNotFoundError(
                f"Template '{template_name}' not found in the vault."
            )

        if version is None:
            versions = [f[:-5] for f in os.listdir(template_dir) if f.endswith(".json")]
            if not versions:
                raise FileNotFoundError(
                    f"No versions found for template '{template_name}'."
                )
            version = max(versions)

        file_name = f"{version}.json"
        file_path = os.path.join(template_dir, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Version '{version}' not found for template '{template_name}'."
            )

        with open(file_path, "r") as file:
            json_str = file.read()

        template_class = TemplateRegistry.get_class(template_name)
        if template_class is None:
            print(
                f"Warning: Template class '{template_name}' not found in the registry. Using BaseTemplate."
            )
            template_class = BaseTemplate

        return template_class.from_json(json_str)

    def list_templates(self):
        templates = []
        for template_name in os.listdir(self.vault_path):
            template_dir = os.path.join(self.vault_path, template_name)
            if os.path.isdir(template_dir):
                versions = [
                    f[:-5] for f in os.listdir(template_dir) if f.endswith(".json")
                ]
                templates.append((template_name, versions))
        return templates
