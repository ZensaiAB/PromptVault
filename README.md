# Prompt Template Management

This program provides a convenient way to manage and version prompt templates for prompt engineering projects. It allows you to create, save, retrieve, and update prompt templates easily.

## Features

- Create prompt templates using the `BaseTemplate` class or custom template classes
- Save prompt templates to a local vault with versioning support and optional folder organization
- Retrieve prompt templates from the vault by name, version, and optional folder
- Update prompt template versions (major, minor, or patch)
- List all available prompt templates in the vault
- Extend the `BaseTemplate` class to create new types of prompt templates

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ZensaiAB/PromptVault.git
   ```
2. Change directory:
   ```
   cd promptvault
   ```
3. Install the package:
   ```
   pip install .
   ```

   This will install the `PromptVault` package and its dependencies.

## Usage

### Creating a Prompt Template

To create a new prompt template, you can use the `BaseTemplate` class or define your own custom template class. Here's an example:

```python
from promptvault.template import BaseTemplate

template = BaseTemplate(template="Hello, {name}! How can I assist you today?")
```

### Saving a Prompt Template

To save a prompt template to the vault, use the `save_template` function. You can optionally specify a `vault_folder` to organize templates into different folders:

```python
from promptvault.template_utils import save_template

save_template(template)  # Save to the default location
save_template(template, vault_folder="chatbot_templates")  # Save to a specific folder
```

### Retrieving a Prompt Template

To retrieve a prompt template from the vault, use the `get_template` function. You can specify the template name, version, and optional folder:

```python
from promptvault.template_utils import get_template

retrieved_template = get_template("BaseTemplate")
retrieved_template = get_template("BaseTemplate", version="1.0.0")
retrieved_template = get_template("BaseTemplate", version="1.0.0", vault_folder="chatbot_templates")
```

### Updating a Prompt Template Version

To update the version of a prompt template, use the `update_version` method:

```python
template.update_version(minor=True)  # Increment minor version
template.update_version(major=True)  # Increment major version
template.update_version(patch=True)  # Increment patch version (default)
```

### Listing Available Prompt Templates

To list all available prompt templates in the vault, use the `list_templates` function:

```python
from promptvault.template_utils import list_templates

templates = list_templates()
print(templates)
```

### Extending the BaseTemplate Class

You can create new types of prompt templates by extending the `BaseTemplate` class. Define a new class that inherits from `BaseTemplate` and customize the `template` attribute or add any additional attributes or methods specific to that template type:

```python
<<<<<<< HEAD
from PromptVault.template import BaseTemplate
=======
from promptvault.template import BaseTemplate
from dataclasses import dataclass
>>>>>>> dev

@dataclass
class TemplateTest(BaseTemplate):
    template = "Hello, {name}!"
```

The new template class will inherit all the functionality of the `BaseTemplate` class, and you can use it in the same way as the base class. @dataclass is necessary when adding new or changing attributes. Alternative:

```python
from promptvault.template import BaseTemplate
from dataclasses import dataclass

class TemplateTest(BaseTemplate):
   pass

template = TemplateTest("Hello, {name}!")
```

### Customizing the Vault

By default, the program uses a local vault to store prompt templates. You can customize the vault location by setting the `VAULT_PATH` environment variable:

```
export VAULT_PATH="/path/to/your/vault"
```

## Examples

Here are a few examples of how to use the prompt template management program for prompt engineering:

1. Creating a prompt template for a customer support chatbot:
   ```python
   template = BaseTemplate(template="Hello, {name}! How can I assist you today? Please provide more details about your issue.")
   save_template(template, vault_folder="chatbot_templates")
   ```

2. Retrieving a prompt template for a specific version and folder:
   ```python
   retrieved_template = get_template("CustomerSupportTemplate", version="1.2.0", vault_folder="chatbot_templates")
   prompt = retrieved_template.to_prompt(name="John")
   print(prompt)
   ```

3. Updating a prompt template version after making changes:
   ```python
   template = get_template("CustomerSupportTemplate", vault_folder="chatbot_templates")
   template.template = "Hello, {name}! How can I help you today? Please describe your issue in detail."
   template.update_version(minor=True)
   save_template(template, vault_folder="chatbot_templates")
   ```

4. Creating a new prompt template class:
   ```python
   @dataclass
   class GreetingTemplate(BaseTemplate):
       template = "Hello, {name}! Welcome to our service."

   template = GreetingTemplate()
   save_template(template, vault_folder="greeting_templates")
   ```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [Apache License](LICENSE).