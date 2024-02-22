import json
import csv
import os
from jinja2 import Environment, FileSystemLoader

from openai import OpenAI
client = OpenAI()

##########
# Inputs #
##########

# Note for gpt-4-0125-preview, the maximum number of tokens is 4096
# including the prompt and the response
# 4096 tokens = approximately 1000 words
# Based on Eleni's latest prompts
# Assuming an input prompt of 200 words
# And assuming 100 words per generated prompt example
# We can expect a prompt + response designed to generate
# one new prompt in the response to take up 300 words = 1200 tokens.
# gpt-4-0125-preview costs $0.03 per 1000 tokens
# So we can expect to pay $0.036 per prompt.
# A dataset of 1000 prompts would cost $36


model = "gpt-4-0125-preview"
prompt_structure_dir = "pairs_v1"
template_file = "template_single.j2" 
prompt_context_file = "honesty.json" # ToDo: change to list
num_examples = 5 # Must be a whole number

################# 
# End of inputs #
#################

# ToDo: Automate setting up of folders for new prompts

# Constants
SRC_PATH = os.path.dirname(__file__)
DATASET_BUILDER_DIR_PATH = os.path.join(SRC_PATH, "prompts", prompt_structure_dir)

sub_dirs = ['contexts', 'dataset_generator_prompts', 'generated_dataset', 'templates']

for sub_dir in sub_dirs:
    path = os.path.join(prompt_structure_dir, sub_dir)
    if not os.path.exists(path):
        os.makedirs(path)

# Input directories and files
template_file_path = os.path.join(DATASET_BUILDER_DIR_PATH, "templates", template_file)
prompt_context, _ = os.path.splitext(prompt_context_file)
prompt_context_file_path = os.path.join(DATASET_BUILDER_DIR_PATH, "contexts", prompt_context+".json")

# Output directories and files
dataset_generator_prompt_file_path = os.path.join(DATASET_BUILDER_DIR_PATH, "dataset_generator_prompts", prompt_context+"_prompt.txt")
generated_dataset_file_path = os.path.join(DATASET_BUILDER_DIR_PATH, "generated_datasets", prompt_context+"_dataset.csv")

# Forming the prompt from the template and template material
def render_template_with_data(template_file_path, prompt_context_file_path, dataset_generator_prompt_file_path):

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

    # Render the template with the prompt_construction_options
    prompt_to_generate_dataset = template.render(prompt_construction_options)

    # Save the prompt to a file
    with open(dataset_generator_prompt_file_path, 'w') as file:
        file.write(prompt_to_generate_dataset)
    
    print(" ")
    print("Prompt:")
    print(prompt_to_generate_dataset)
    print(" ")

    prompt_to_generate_dataset = prompt_to_generate_dataset.replace('\n', ' ')

    print(" ")
    print("Prompt:")
    print(prompt_to_generate_dataset)
    print(" ")

    return prompt_to_generate_dataset

prompt = render_template_with_data(template_file_path, prompt_context_file_path, dataset_generator_prompt_file_path)

def generate_dataset_from_prompt(prompt, generated_dataset_file_path, model, num_examples):
    with open(generated_dataset_file_path, "w", newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for i in range(num_examples):
            completion = client.chat.completions.create(
                **{
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            # ToDo: Different prompts require different data processing
            # Create functions to do this in the prompts folder
            separator = "The answer is A because "
            llm_ouput = completion.choices[0].message.content.strip()
            before, match, after = llm_ouput.partition(separator)
            first_part = before + match
            second_part = after
            # Remove quote marks from each part
            # Stripping again because finding some weird white space
            # in middle of strings
            first_part_cleaned = first_part.strip().replace('"', '')
            second_part_cleaned = second_part.strip().replace('"', '')
            print("\nIteration: ", i)
            print("First part: ", first_part)
            print("Second part: ", second_part)
            writer.writerow([first_part])  # Write the first part
            writer.writerow([second_part])  # Write the second part   

generate_dataset_from_prompt(prompt, generated_dataset_file_path, model, num_examples)
