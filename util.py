

class SquadUtil:

    default_replacer = None

    @staticmethod
    def flatten_json(json_data):
        flattened_data = {}

        def flatten(data, prefix=''):
            if isinstance(data, dict):
                for key, value in data.items():
                    flatten(value, prefix + key + '.')
            elif isinstance(data, list):
                for index, value in enumerate(data):
                    flatten(value, prefix + str(index) + '.')
            else:
                flattened_data[prefix[:-1]] = data

        flatten(json_data)
        return flattened_data


    @classmethod
    def replace_nan_with(
        cls,
        __data: list[float],
        /,
        replace_with: Any = None
    ):
        """Replace NaN values with `replace_with`."""
        if replace_with is None:
            replace_with = cls.default_replacer


import os
from collections import Counter


def count_words_in_directory(directory):
    word_count = Counter()

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file is a text file
            if file.endswith('.md'):
                with open(file_path, 'r') as f:
                    content = f.read()
                    words = content.split()
                    word_count.update(words)

    return word_count





import json
from typing import List, Dict, Any, Union


def generate_dataclass_code(json_data: Dict[str, Any], class_name: str) -> str:
    code = f"from dataclasses import dataclass\n\n@dataclass\nclass {class_name}:\n"

    def generate_field_code(name: str, value: Any, indent_level: int = 1) -> str:
        indent = "    " * indent_level
        if isinstance(value, dict):
            nested_class_name = f"{name.capitalize()}Class"
            code = f"{indent}{name}: {nested_class_name}\n"
            code += generate_dataclass_code(value, nested_class_name)
        elif isinstance(value, list):
            if value and isinstance(value[0], dict):
                nested_class_name = f"{name.capitalize()}Item"
                code = f"{indent}{name}: List[{nested_class_name}]\n"
                code += generate_dataclass_code(value[0], nested_class_name)
            else:
                item_type = type(value[0]).__name__ if value else "Any"
                code = f"{indent}{name}: List[{item_type}]\n"
        else:
            code = f"{indent}{name}: {type(value).__name__}\n"
        return code

    for name, value in json_data.items():
        code += generate_field_code(name, value)

    return code


# Example usage
json_document = '''
{
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "hobbies": ["reading", "traveling"],
    "address": {
        "street": "123 Main St",
        "zipcode": "12345"
    },
    "contacts": [
        {
            "name": "Jane Smith",
            "phone": "123-456-7890"
        },
        {
            "name": "Mike Johnson",
            "phone": "987-654-3210"
        }
    ]
}
'''

json_data = json.loads(json_document)
class_name = "Person"

dataclass_code = generate_dataclass_code(json_data, class_name)
print(dataclass_code)

class Singleton(object):
    """The famous Singleton class that can only have one instance."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Create a new instance of the class if one does not already exist."""
        if cls._instance is not None:
            raise Exception("Singleton class can only have one instance.")
        cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


# Create the first instance
single = Singleton()

# Try to create the second instance
double = Singleton()
