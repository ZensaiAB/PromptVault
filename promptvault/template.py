import yaml
from dataclasses import dataclass, field, asdict, fields
from string import Template
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
        print(f"Registering class template: {template_class.__name__}")

    @classmethod
    def get_class(cls, class_name):
        return cls.registry.get(class_name)
    
@register_template
@dataclass
class BaseTemplate:
    template: str = field(default_factory=str)
    version: str = "1.0"  # Default version
    class_name: str = field(init=False)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        TemplateRegistry.register_class(cls)

    def __post_init__(self):
        self.class_name = self.__class__.__name__

    def to_prompt(self, **kwargs) -> str:
        """Generates the final prompt by dynamically inserting provided keyword arguments into the template."""
        template = self.template
        required_variables = self.variables
        missing_variables = [var for var in required_variables if var not in kwargs]

        if missing_variables:
            raise ValueError(
                f"Missing required arguments for template placeholders: {', '.join(missing_variables)}.\n"
                f"Expected variables are: {', '.join(required_variables)}."
            )
        sub = {}
        for req in required_variables:
            template = template.replace("{"+req+"}", "$"+req)
            sub[req] = kwargs[req]

        tpl = Template(template)
        try:
            return tpl.safe_substitute(sub)
        except KeyError as e:
            raise ValueError(
                f"An error occurred with the provided arguments: {e}."
            ) from e

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        class_name = data.pop("class_name", None)
        if not class_name:
            raise ValueError("JSON must contain 'class_name'")
        target_class = TemplateRegistry.get_class(class_name)
        if target_class is None:
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

    @classmethod
    def from_yaml(cls, yaml_str: str):
        data = yaml.safe_load(yaml_str)
        class_name = data.pop("class_name", None)
        if not class_name:
            raise ValueError("YAML must contain 'class_name'")
        target_class = TemplateRegistry.get_class(class_name)
        if target_class is None:
            target_class = BaseTemplate

        field_data = {field.name: data.pop(field.name) for field in fields(target_class) if field.name in data}
        instance = target_class(**data)
        for name, value in field_data.items():
            setattr(instance, name, value)

        return instance

    def to_json(self) -> str:
        data = asdict(self)
        data["class_name"] = self.__class__.__name__
        return json.dumps(data, indent=2)

    def to_yaml(self) -> str:
        data = asdict(self)
        data["class_name"] = self.__class__.__name__
        return yaml.dump(data, sort_keys=False, default_flow_style=False)

    @property
    def variables(self) -> list:
        pattern = re.compile(r"\{(\w+)\}")
        return list(set(pattern.findall(self.template)))

    def save_to_file(self, file_path: str, format='yaml') -> None:
        with open(file_path, "w") as file:
            if format == 'yaml':
                file.write(self.to_yaml())
            else:
                file.write(self.to_json())

    @classmethod
    def load_from_file(cls, file_path: str, format='yaml'):
        with open(file_path, "r") as file:
            content = file.read()
            if format == 'yaml':
                return cls.from_yaml(content)
            else:
                return cls.from_json(content)

    def update_version(self, major=False, minor=True):
        version_parts = self.version.split(".")
        major_num = int(version_parts[0])
        minor_num = int(version_parts[1]) if len(version_parts) > 1 else 0

        if major:
            major_num += 1
            minor_num = 0
        elif minor:
            minor_num += 1

        self.version = f"{major_num}.{minor_num}"
