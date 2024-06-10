# Copyright 2023 Euan Steven
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- encoding: utf-8 -*-
# ========== parse.py ==========
# Author : Euan Steven
# Date Created : 17/12/2023
# Date Modified : 17/12/2023
# Version : 1.5
# License : Apache 2.0
# Description : Parse Recipe Text using OpenAI API
# =============================

# ========== Module Imports ==========

print("[OK] PARSER - Importing Modules")
# Built-in Modules
import os

# Third-party Modules
import requests

print("[OK] PARSER - Imported Modules")

# ========== OpenAI API Request ==========

headers = {
    'Authorization': 'API_KEY',
    'Content-Type': 'application/json',
}

def api_request(recipe_text):
    json_data = {
        'model': 'MODEL',
        'max_tokens': 10000,
        'messages': [
            {
                'role': 'system',
                'content': 'Hi.',
            },
            {
                'role': 'user',
                'content': f'Separate the Recipe Name, Ingredients, and Method to different headings. Make sure to remove any text that is not related to the recipe, such as nutritional information, tips, yeild, and no Notes at the end, etc.\n\n{recipe_text}',
            },
        ],
    }

    json_data['text'] = recipe_text

    try:
        response = requests.post('https://api.pawan.krd/v1/chat/completions', headers=headers, json=json_data)
        response.raise_for_status()

        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# ========== Parse and Save Recipe ==========

def parse_and_save_recipe(recipe_number, response_content, output_folder_path):
    # Find the positions of 'Recipe:', 'Ingredients:', and 'Method:' in the response content
    recipe_name_start = response_content.find('Recipe Name: ')
    ingredients_start = response_content.find('Ingredients:', recipe_name_start)
    method_start = response_content.find('Method:', ingredients_start)

    # Check if all headings are found
    if ingredients_start == -1 or method_start == -1 or recipe_name_start == -1:
        print(f"[ERROR] PARSER - Couldn't find 'Ingredients' or 'Method' in response for Recipe {recipe_number}. Skipping.")
        return

    # Extract the recipe name based on the positions found
    recipe_name = response_content[recipe_name_start + len('Recipe Name: '):ingredients_start].strip()

    # Extract ingredients and method as before
    ingredients = response_content[ingredients_start + len('Ingredients:'):method_start].strip()
    method = response_content[method_start + len('Method:'):].strip()

    # Create the 'parsed' folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Save to a file with the recipe name and number as the title
    output_filename = f'{recipe_name}_parsed.txt'
    output_filepath = os.path.join(output_folder_path, output_filename)

    with open(output_filepath, 'w') as output_file:
        output_file.write(f"Recipe: {recipe_name}\n\n")
        output_file.write(f"Ingredients:\n{ingredients}\n\n")
        output_file.write(f"Method:\n{method}\n")

# ========== Main Program ==========

def main():
    print("[OK] PARSER - Opening Files")

    # Specify the path to the "/text" and "/parsed" folders
    input_folder_path = 'scanned'
    output_folder_path = 'parsed'

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder_path, filename)

            print(f"[OK] PARSER - Processing {filename}")

            with open(input_file_path, 'r') as file:
                file_content = file.read()

            # Split content into recipes based on '=========='
            recipes = file_content.split('==========\n')

            for i, recipe_text in enumerate(recipes):
                # Skip empty strings
                if not recipe_text.strip():
                    continue

                print(f"[OK] PARSER - Processing Recipe {i+1}")
                # Send the recipe text to OpenAI API
                response_content = api_request(recipe_text)
                print("[OK] PARSER - Response Received")

                if response_content:
                    # Parse and save the recipe content to the output folder
                    print("[OK] PARSER - Saving Recipe")
                    parse_and_save_recipe(i+1, response_content, output_folder_path)
                    print("[OK] PARSER - Recipe Saved")

    return output_folder_path

if __name__ == "__main__":
    main()
