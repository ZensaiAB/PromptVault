import os
from .local_vault import LocalVault


def create_vault():
    vault_type = os.getenv("VAULT_TYPE", "local")
    if vault_type == "local":
        vault_path = os.getenv("VAULT_PATH", "templates")
        return LocalVault(vault_path)
    elif vault_type == "remote":
        # Implement RemoteVault and instantiate it here
        raise NotImplementedError("RemoteVault is not implemented yet.")
    else:
        raise ValueError(f"Invalid vault type: {vault_type}")
