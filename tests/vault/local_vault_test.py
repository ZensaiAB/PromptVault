import os
import pytest
from src.vault import LocalVault
from src.template import BaseTemplate, register_template

@pytest.fixture
def vault_path(tmpdir):
    return str(tmpdir.mkdir("vault"))

@pytest.fixture
def local_vault(vault_path):
    return LocalVault(vault_path)

@register_template
class TemplateTest(BaseTemplate):
    template = "Hello, {name}!"

class UnregisteredTemplate(BaseTemplate):
    template = "Unregistered template: {name}"

def test_save_and_load(local_vault):
    template = TemplateTest()
    local_vault.save(template)

    loaded_template = local_vault.load("TemplateTest")
    assert isinstance(loaded_template, TemplateTest)
    assert loaded_template.template == template.template
    assert loaded_template.version == template.version

def test_load_latest_version(local_vault):
    template1 = TemplateTest(version="1.0.0")
    template2 = TemplateTest(version="2.0.0")
    local_vault.save(template1)
    local_vault.save(template2)

    loaded_template = local_vault.load("TemplateTest")
    assert loaded_template.version == "2.0.0"

def test_load_specific_version(local_vault):
    template1 = TemplateTest(version="1.0.0")
    template2 = TemplateTest(version="2.0.0")
    local_vault.save(template1)
    local_vault.save(template2)

    loaded_template = local_vault.load("TemplateTest", version="1.0.0")
    assert loaded_template.version == "1.0.0"

def test_load_nonexistent_template(local_vault):
    with pytest.raises(FileNotFoundError, match="Template 'NonexistentTemplate' not found in the vault."):
        local_vault.load("NonexistentTemplate")

def test_load_nonexistent_version(local_vault):
    template = TemplateTest()
    local_vault.save(template)

    with pytest.raises(FileNotFoundError):
        local_vault.load("TemplateTest", version="999.0.0")

def test_list_templates(local_vault):
    template1 = TemplateTest(version="1.0.0")
    template2 = TemplateTest(version="2.0.0")
    local_vault.save(template1)
    local_vault.save(template2)

    templates = local_vault.list_templates()
    assert templates == [("TemplateTest", ["1.0.0", "2.0.0"])]

def test_save_and_load_base_template(local_vault):
    template = BaseTemplate(template="Test template")
    local_vault.save(template)

    loaded_template = local_vault.load("BaseTemplate")
    assert isinstance(loaded_template, BaseTemplate)
    assert loaded_template.template == template.template
    assert loaded_template.version == template.version

def test_load_unregistered_template(local_vault, capsys):
    template = UnregisteredTemplate(template="Test template")
    local_vault.save(template)

    loaded_template = local_vault.load("UnregisteredTemplate")
    assert isinstance(loaded_template, BaseTemplate)
    assert loaded_template.template == "Test template"

    captured = capsys.readouterr()
    assert "Warning: Template class 'UnregisteredTemplate' not found in the registry. Using BaseTemplate." in captured.out
