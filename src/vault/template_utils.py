from src.vault.vault_factory import create_vault


def get_template(template_name, version=None):
    vault = create_vault()
    return vault.load(template_name, version)


def save_template(template):
    vault = create_vault()
    vault.save(template)


def list_templates():
    vault = create_vault()
    return vault.list_templates()
