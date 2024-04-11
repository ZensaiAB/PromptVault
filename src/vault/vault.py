import os
from abc import ABC, abstractmethod

class Vault(ABC):
    @abstractmethod
    def save(self, template):
        pass

    @abstractmethod
    def load(self, template_name, version=None):
        pass

    @abstractmethod
    def list_templates(self):
        pass
