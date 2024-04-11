
from dataclasses import dataclass, field, asdict, fields
import json
import re

def register_template(cls):
    """Decorator to register template classes in the TemplateRegistry."""
    TemplateRegistry.register_class(cls)
    return cls

class TemplateRegistry:
    registry = {}

    @classmethod
    def register_class(cls, template_class):
        cls.registry[template_class.__name__] = template_class

    @classmethod
    def get_class(cls, class_name):
        print(f"Looking for class: {class_name}, available: {list(cls.registry.keys())}")
        return cls.registry.get(class_name)

@register_template
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
        class_name = data.pop('class_name', None)
        if not class_name:
            raise ValueError("JSON must contain 'class_name'")
        target_class = TemplateRegistry.get_class(class_name)
        if target_class is None:
            print(f"Warning: Template class '{class_name}' not found in the registry. Using BaseTemplate.")
            target_class = BaseTemplate

        # Handle field attributes separately
        field_data = {}
        for field in fields(target_class):
            if field.name in data:
                field_data[field.name] = data.pop(field.name)

        # Create the instance with the remaining data
        instance = target_class(**data)

        # Set the field attributes
        for name, value in field_data.items():
            setattr(instance, name, value)

        return instance

    def to_json(self) -> str:
        data = asdict(self)
        data['class_name'] = self.__class__.__name__
        return json.dumps(data, indent=2)

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

    def update_version(self, major=False, minor=False, patch=True):
        version_parts = self.version.split('.')
        major_num = int(version_parts[0])
        minor_num = int(version_parts[1]) if len(version_parts) > 1 else 0
        patch_num = int(version_parts[2]) if len(version_parts) > 2 else 0
        
        if major:
            major_num += 1
            minor_num = 0
            patch_num = 0
        elif minor:
            minor_num += 1
            patch_num = 0
        elif patch:
            patch_num += 1
        
        self.version = f"{major_num}.{minor_num}"

