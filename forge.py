import argparse
import datetime

import firebase_admin
from firebase_admin import firestore
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from google.auth import default

from utils import camel_to_pascal, get_user_confirmation, plural_to_singular, prompt_user

models: dict = {}
imports: set = set()

def add_imports(file_path, optional=False):
    with open(file_path, 'r') as file:
        models = file.read()


    with open(file_path, 'w') as file:
        if "datetime" in imports:
            file.write('from datetime import datetime\n')
        if optional:
            file.write(f'from typing import Optional\n')
        
        file.write(f'\nfrom pydantic import BaseModel')
        if "Field" in imports:
            file.write(", Field")
        
        file.write("\n\n\n")
        
        file.write(models)

def generate_class_code(class_name, attributes, output_file, optional=False):

    with open(output_file, 'a') as f:
        f.write(f'class {class_name}(BaseModel):\n\n') 
        for attribute, attr_type in sorted(attributes.items()):
            if optional:
                if attribute[0] == "_":
                    f.write(f'    {attribute[1:]}: Optional[{attr_type}] = Field(None, alias="{attribute}")\n')
                    imports.add("Field")
                else:
                    f.write(f'    {attribute}: Optional[{attr_type}] = None\n')
            else:
                if attribute[0] == "_":
                    f.write(f'    {attribute[1:]}: {attr_type} = Field(alias="{attribute}")\n')
                    imports.add("Field")
                else:
                    f.write(f'    {attribute}: {attr_type}\n')
        f.write('\n')
        f.write('\n')

def add_models(name:str, data: dict, output_file: str, optional=False) -> str:

    model_signature: str = "".join(sorted([f"{key}-{type(val)}" for key, val in data.items()]))

    if model_signature in models:
        return models[model_signature]
    
    model = {}

    for key, val in data.items():
        if type(val) in [bool, str, int, float, datetime]:
            model[key] = type(val).__name__
        if type(val) == DatetimeWithNanoseconds:
            model[key] = "datetime"
            imports.add("datetime")
        if type(val) == dict:
            model[key] = camel_to_pascal(f"{key}")
            add_models(camel_to_pascal(f"{key}"), val, output_file, optional)
        if type(val) in [list, tuple]:
            if len(val) > 1:
                model_type = f"list[{plural_to_singular(camel_to_pascal(f"{key}")) if type(val[0]) == dict else type(val[0]).__name__}]"
                model[key] = model_type
                if type(val[0]) == dict:
                    add_models(plural_to_singular(camel_to_pascal(f"{key}")), val[0], output_file, optional)
            else:
                model[key] = "list"

    generate_class_code(camel_to_pascal(name), model, output_file, optional)
    models[model_signature] = name

def main():
    parser = argparse.ArgumentParser()

    # Firestone document path.
    parser.add_argument("-dp", "--document_path", type=str, required=True, help="Reference firestore model path to create models.")
    # File to write pydantic code in.
    parser.add_argument("-fp", "--file_path", type=str, default="model.py", help="File path to add models in.")
    # Flags
    parser.add_argument("-o", "--optional", action='store_true', help="To make every field optional.")

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    document_path = args.document_path
    file_path = args.file_path
    optional = args.optional

    # Initialize Firestore client
    cred, project = default()
    firebase_admin.initialize_app(cred, {'projectId': project})

    prompt_user(f"\n⚠️ Current selected project is `{project}`.", "RED")

    get_user_confirmation("GRAY")

    prompt_user("\n-> Getting document from firestore.")
    data = firestore.client().document(document_path).get().to_dict()

    prompt_user("\n-> Building Models.")
    add_models(document_path.split("/")[-2], data, file_path, optional)
    
    prompt_user("\n-> Adding Dependencies.")
    add_imports(file_path, optional)

    prompt_user(f"\n-> Done. Models added to `{file_path}`.", "GREEN")
    

if __name__ == "__main__":
    main()
