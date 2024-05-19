import pytest
from promptvault.template import BaseTemplate, TemplateRegistry, register_template
from dataclasses import dataclass


@register_template
@dataclass
class PromptTest(BaseTemplate):
    extra_field: str = "Extra Data"


# Fixture for reusable BaseTemplate instance
@pytest.fixture
def sample_template():
    return BaseTemplate(template="Hello, {name}!")


# Test initialization and attribute correctness
def test_initialization():
    bt = BaseTemplate(template="Hello, {name}!", version="1.1")
    assert bt.template == "Hello, {name}!"
    assert bt.version == "1.1"
    assert bt.class_name == "BaseTemplate"


# Test successful prompt generation
def test_to_prompt_success(sample_template):
    assert sample_template.to_prompt(name="Alice") == "Hello, Alice!"


# Test handling missing required variables
def test_to_prompt_missing_variable(sample_template):
    with pytest.raises(ValueError) as e:
        sample_template.to_prompt()
    assert "Missing required arguments for template placeholders" in str(e.value)


# Test the extraction of variables
def test_variables_extraction(sample_template):
    assert sample_template.variables == ["name"]


# Test JSON serialization and deserialization
def test_json_serialization():
    bt = BaseTemplate(template="Goodbye, {name}.", version="1.2")
    json_str = bt.to_json()
    new_bt = BaseTemplate.from_json(json_str)
    assert new_bt.template == "Goodbye, {name}."
    assert new_bt.version == "1.2"
    assert new_bt.class_name == "BaseTemplate"


# Test YAML serialization and deserialization
def test_yaml_serialization():
    bt = BaseTemplate(template="Goodbye, {name}.", version="1.2")
    yaml_str = bt.to_yaml()
    new_bt = BaseTemplate.from_yaml(yaml_str)
    assert new_bt.template == "Goodbye, {name}."
    assert new_bt.version == "1.2"
    assert new_bt.class_name == "BaseTemplate"


# Test saving to and loading from a JSON file
def test_save_load_json_file(tmp_path, sample_template):
    file_path = tmp_path / "template.json"
    sample_template.save_to_file(str(file_path), format='json')
    loaded_template = BaseTemplate.load_from_file(str(file_path), format='json')
    assert loaded_template.template == sample_template.template
    assert loaded_template.version == sample_template.version
    assert loaded_template.class_name == sample_template.class_name


# Test saving to and loading from a YAML file
def test_save_load_yaml_file(tmp_path, sample_template):
    file_path = tmp_path / "template.yaml"
    sample_template.save_to_file(str(file_path), format='yaml')
    loaded_template = BaseTemplate.load_from_file(str(file_path), format='yaml')
    assert loaded_template.template == sample_template.template
    assert loaded_template.version == sample_template.version
    assert loaded_template.class_name == sample_template.class_name


# Fixture for reusable PromptTest instance
@pytest.fixture
def test_prompt():
    return PromptTest(template="Hello, {name}!")


# Test that the class is correctly registered
def test_class_registration():
    registered_class = TemplateRegistry.get_class("PromptTest")
    assert registered_class is PromptTest


def test_subclass_json_serialization(test_prompt):
    json_str = test_prompt.to_json()
    print(json_str)
    loaded_prompt = PromptTest.from_json(json_str)
    assert isinstance(loaded_prompt, PromptTest)
    assert loaded_prompt.template == "Hello, {name}!"
    assert loaded_prompt.extra_field == "Extra Data"
    assert loaded_prompt.class_name == "PromptTest"


def test_subclass_yaml_serialization(test_prompt):
    yaml_str = test_prompt.to_yaml()
    print(yaml_str)
    loaded_prompt = PromptTest.from_yaml(yaml_str)
    assert isinstance(loaded_prompt, PromptTest)
    assert loaded_prompt.template == "Hello, {name}!"
    assert loaded_prompt.extra_field == "Extra Data"
    assert loaded_prompt.class_name == "PromptTest"
