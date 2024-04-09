import json
import re
from dataclasses import dataclass, asdict, field

@dataclass
class BasePrompt:
    template: str = field(default_factory=str)
    version: str = "1.0"  # Default version
    class_name: str = field(init=False)

    def __post_init__(self):
        self.class_name = self.__class__.__name__

    def generate_prompt(self, **kwargs) -> str:
        """Generates the final prompt by dynamically inserting provided keyword arguments into the template."""
        return self.template.format(**kwargs)

    @classmethod
    def from_json(cls, json_str: str):
        """Creates an instance of the class from a JSON string."""
        data = json.loads(json_str)
        # Dynamically get the class from globals() based on class_name
        target_class = globals()[data['class_name']]
        return target_class(**data)

    def to_json(self) -> str:
        """Serializes the instance to a JSON string."""
        return json.dumps(asdict(self), indent=2)

    @property
    def variables(self) -> list:
        """Returns a list of unique variable names that can be set in the template."""
        pattern = re.compile(r"\{(\w+)\}")
        return list(set(pattern.findall(self.template)))

    def save_to_file(self, file_path: str) -> None:
        """Saves the instance to a JSON file."""
        with open(file_path, "w") as file:
            file.write(self.to_json())

    @classmethod
    def load_from_file(cls, file_path: str):
        """Loads an instance from a JSON file."""
        with open(file_path, "r") as file:
            json_str = file.read()
        return cls.from_json(json_str)
