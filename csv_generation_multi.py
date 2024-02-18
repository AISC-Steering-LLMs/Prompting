import json
import csv
import os
from jinja2 import Environment, FileSystemLoader

from openai import OpenAI
client = OpenAI()

##########
# Inputs #
##########

model = "gpt-4-0125-preview"
template_file = "template_multi.j2"
prompt_structure_dir = "pairs_v1"
prompt_context_file = "honesty.json"
num_examples = "5" # Must be a string


################# 
# End of inputs #
#################

# ToDo: Automate setting up of folders for new prompts

# Constants
SRC_PATH = os.path.dirname(__file__)
DATASET_BUILDER_DIR_PATH = os.path.join(SRC_PATH, "prompts", prompt_structure_dir)

# Input directories and files
template_file_path = os.path.join(DATASET_BUILDER_DIR_PATH, "templates", template_file)
prompt_context, _ = os.path.splitext(prompt_context_file)
prompt_context_file_path = os.path.join(DATASET_BUILDER_DIR_PATH, "contexts", prompt_context+".json")

# Output directories and files
dataset_generator_prompt_file_path = os.path.join(DATASET_BUILDER_DIR_PATH, "dataset_generator_prompts", prompt_context+"_prompt.txt")
generated_dataset_file_path = os.path.join(DATASET_BUILDER_DIR_PATH, "generated_datasets", prompt_context+"_dataset.csv")

# Forming the prompt from the template and template material
def render_template_with_data(template_file_path,
                              prompt_context_file_path,
                              dataset_generator_prompt_file_path,
                              num_examples):

    # Set up the environment with the path to the directory containing the template
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_file_path)))

    # Now, get_template should be called with the filename only, not the path
    template = env.get_template(os.path.basename(template_file_path))
    
    # Load the prompt context
    with open(prompt_context_file_path, 'r') as file:
        prompt_construction_options = json.load(file)

    # Update the prompt context example to replace the list with the combined string
    example_text = "\n".join(prompt_construction_options["example"])
    prompt_construction_options["example"] = example_text
    prompt_construction_options["num_examples"] = num_examples

    # Render the template with the prompt_construction_options
    prompt_to_generate_dataset = template.render(prompt_construction_options)

    # Save the prompt to a file
    with open(dataset_generator_prompt_file_path, 'w') as file:
        file.write(prompt_to_generate_dataset)

    # Remove newlines from the prompt and replace with spaces
    prompt_to_generate_dataset = prompt_to_generate_dataset.replace('\n', ' ')

    return prompt_to_generate_dataset

# Generate the prompt
prompt = render_template_with_data(template_file_path,
                                   prompt_context_file_path,
                                   dataset_generator_prompt_file_path,
                                   num_examples)

# Generate the dataset by calling the OpenAI API
def generate_dataset_from_prompt(prompt, generated_dataset_file_path, model):
    completion = client.chat.completions.create(
            **{
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
    
    # cleaned_completion = completion.choices[0].message.content.strip()[3:-3]
    print(" ")
    print(completion.choices[0].message.content.strip())
    print(" ")

    # Open a file in write mode ('w') and save the CSV data
    with open(generated_dataset_file_path, 'w', newline='', encoding='utf-8') as file:
        file.write(completion.choices[0].message.content.strip())

    
# Generate the dataset
generate_dataset_from_prompt(prompt, generated_dataset_file_path, model)

