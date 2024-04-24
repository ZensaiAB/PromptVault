from .vault.vault_factory import create_vault

def get_template(template_name, version=None, **kwargs):
    vault = create_vault()
    return vault.load(template_name, version, **kwargs)


def save_template(template, **kwargs):
    vault = create_vault()
    vault.save(template, **kwargs)


def list_templates(**kwargs):
    vault = create_vault()
    return vault.list_templates(**kwargs)
