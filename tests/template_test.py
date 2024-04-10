import pytest
from src.template import BaseTemplate
import json
import os

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
    assert sample_template.variables == ['name']

# Test JSON serialization and deserialization
def test_json_serialization():
    bt = BaseTemplate(template="Goodbye, {name}.", version="1.2")
    json_str = bt.to_json()
    new_bt = BaseTemplate.from_json(json_str)
    assert new_bt.template == "Goodbye, {name}."
    assert new_bt.version == "1.2"
    assert new_bt.class_name == "BaseTemplate"

# Test saving to and loading from a file
def test_save_load_file(tmp_path, sample_template):
    file_path = tmp_path / "template.json"
    sample_template.save_to_file(str(file_path))
    loaded_template = BaseTemplate.load_from_file(str(file_path))
    assert loaded_template.template == sample_template.template
    assert loaded_template.version == sample_template.version
    assert loaded_template.class_name == sample_template.class_name
