from dataclasses import dataclass, field, asdict
import json
import re

@dataclass
class BaseTemplate:
    template: str = field(default_factory=str)
    version: str = "1.0"  # Default version
    class_name: str = field(init=False)

    def __post_init__(self):
        self.class_name = self.__class__.__name__

    def to_prompt(self, **kwargs) -> str:
        """Generates the final prompt by dynamically inserting provided keyword arguments into the template."""
        # Check if all required variables are present in kwargs
        required_variables = self.variables
        missing_variables = [var for var in required_variables if var not in kwargs]

        if missing_variables:
            # Inform the user about the missing variables
            raise ValueError(f"Missing required arguments for template placeholders: {', '.join(missing_variables)}.\n"
                            f"Expected variables are: {', '.join(required_variables)}.")

        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            # This handles cases where there's a typo or mismatch in variable names,
            # though it should be largely preempted by the above check.
            raise ValueError(f"An error occurred with the provided arguments: {e}.") from e

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        target_class = globals()[data['class_name']]
        return target_class(**data)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @property
    def variables(self) -> list:
        pattern = re.compile(r"\{(\w+)\}")
        return list(set(pattern.findall(self.template)))

    def save_to_file(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            file.write(self.to_json())

    @classmethod
    def load_from_file(cls, file_path: str):
        with open(file_path, "r") as file:
            json_str = file.read()
        return cls.from_json(json_str)
