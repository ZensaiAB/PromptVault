
# PromptVault

PromptVault is a Python package designed to facilitate the management and generation of prompts for language models in a structured and dynamic way. It offers a simple yet powerful interface for templating and customization of prompts, ensuring flexibility and efficiency in developing AI applications.

## Installation

To install PromptVault, simply clone the project, navigate to the root directory of the project and run:

```
pip install .
```

## Usage

The core functionality of PromptVault revolves around the `BaseTemplate` class, which allows for easy creation and manipulation of prompt templates. Here's a basic example of how to use it:

```python
from PromptVault.template import BaseTemplate

# Define a template with placeholders
template_str = "Hello, {name}! Welcome to {place}."

# Create a BaseTemplate instance
template = BaseTemplate(template=template_str)

# Generate a prompt by providing values for the placeholders
prompt = template.to_prompt(name="Alice", place="Wonderland")

print(prompt)
```

This will output:

```
Hello, Alice! Welcome to Wonderland.
```

## Features

- **Dynamic Prompt Generation**: Create and manipulate prompt templates with dynamic placeholders.
- **JSON Support**: Serialize your templates to JSON for easy storage and retrieval.
- **File Operations**: Save your templates to and load them from files directly.

## Contributing

Contributions are welcome! If you have suggestions for improvements or encounter any issues, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
