# tests/test_template_utils.py
import os
import pytest
from promptvault.template import BaseTemplate
from promptvault import get_template, save_template, list_templates


@pytest.fixture
def setup_env(tmpdir):
    os.environ["VAULT_TYPE"] = "local"
    os.environ["VAULT_PATH"] = str(tmpdir)


def test_save_and_get_template(setup_env):
    template = BaseTemplate(template="Hello, {name}!")
    save_template(template)

    loaded_template = get_template("BaseTemplate")
    assert loaded_template.template == "Hello, {name}!"
    assert loaded_template.version == "1.0"


def test_get_template_with_version(setup_env):
    template1 = BaseTemplate(template="Hello, {name}!")
    save_template(template1)

    template2 = BaseTemplate(template="Hello, {name}! How are you?")
    template2.update_version(minor=True)
    save_template(template2)

    loaded_template = get_template("BaseTemplate", version="1.1")
    assert loaded_template.template == "Hello, {name}! How are you?"
    assert loaded_template.version == "1.1"


def test_list_templates(setup_env):
    template1 = BaseTemplate(template="Hello, {name}!")
    save_template(template1)
    template2 = BaseTemplate(template="Goodbye, {name}!")
    template2.update_version(minor=True)
    save_template(template2)
    templates = list_templates()
    assert templates == [("BaseTemplate", ["1.0", "1.1"])]


def test_get_nonexistent_template(setup_env):
    with pytest.raises(FileNotFoundError):
        get_template("NonexistentTemplate")


def test_get_nonexistent_version(setup_env):
    template = BaseTemplate(template="Hello, {name}!")
    save_template(template)

    with pytest.raises(FileNotFoundError):
        get_template("BaseTemplate", version="2.0")
