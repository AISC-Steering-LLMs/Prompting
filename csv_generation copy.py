import json
import csv
import os
from jinja2 import Environment, FileSystemLoader

from openai import OpenAI
client = OpenAI()

# Fix constants.
MODEL = "gpt-4-0125-preview"


def load_examples_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def render_template_with_data(template_path, prompt_construction_path, concept):
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))
    prompt_construction_options = load_examples_from_json(prompt_construction_path)
    prompt_construction_choice = prompt_construction_options[concept]
    example_text = "\n".join(prompt_construction_choice["example"])  # Using a newline character as the separator
    # Update the item dictionary to replace the list with the combined string
    prompt_construction_choice["example"] = example_text
    prompt_to_generate_dataset = template.render(prompt_construction_choice)
    with open('prompt.txt', 'w') as file:
        file.write(prompt_to_generate_dataset)
    return prompt_to_generate_dataset

def generate_dataset_from_prompt(prompt, csv_file_path):
    completion = client.chat.completions.create(model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": f"{prompt}"
                }
            ]
    )
    # with open(csv_file_path, "w") as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Topic", "Completion"])
    #     writer.writerow(
    #         [
    #             "honesty", completion
    #             *(completion.choices[0].message.content.strip().replace("\n", "")).split("(2)")
    #         ]
    #     )

    # Open a file in write mode ('w') and save the CSV data
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        file.write(completion.choices[0].message.content.strip())
        

# Inputs
concept = "honesty"
template_folder = 'prompts/pairs_v1'
template_path = os.path.join(template_folder, 'template.j2')
prompt_construction_path = os.path.join(template_folder, 'examples.json')
csv_file_path = template_folder+'/prompts.csv'

prompt = render_template_with_data(template_path, prompt_construction_path, concept)
generate_dataset_from_prompt(prompt, csv_file_path)

# Now we need to be able to add other columns to the .csv

