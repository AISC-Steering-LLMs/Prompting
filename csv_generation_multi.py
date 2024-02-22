import json
import csv
import os
from jinja2 import Environment, FileSystemLoader
import math
import time

from openai import OpenAI
client = OpenAI()



##########
# Inputs #
##########

# Note for gpt-4-0125-preview, the maximum number of tokens is 4096
# including the prompt and the response
# Based on Eleni's latest prompts
# Assuming an input prompt of 200 words = 250 tokens
# And assuming 50 tokens per generated prompt example we want in the response
# We can expect to generate a maximum of (4096-250)/50 = 3846/50 = 76.92
# So something like 75 generated examples per prompt is the max we can ask for in one go.
# 250 prompt tokens = 200 * 0.01/1000 = $0.0025
# 3846 completion tokens = 3846 * 0.03/1000 = $0.11538
# So the total cost is $0.11788 per 75 prompts.
# If we wanted to generate 1000 prompts, it would cost $1.5718
# Please check your prompts work with ChatGPT before generating a large dataset using the API

model = "gpt-4-0125-preview"
template_file = "template_multi.j2"
prompt_structure_dir = "pairs_v1"
prompt_context_file = "honesty.json"
num_examples_per_prompt = "75" # Must be a whole number inside quote marks.
total_num_examples = 1000

################# 
# End of inputs #
#################


# Constants
SRC_PATH = os.path.dirname(__file__)
DATASET_BUILDER_DIR_PATH = os.path.join(SRC_PATH, "prompts", prompt_structure_dir)


# Number of interations of the prompt to generate the entire dataset
num_iterations = math.ceil(total_num_examples/int(num_examples_per_prompt))

# Create relevant subdirectories if they don't exist
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
log_file_path = os.path.join(DATASET_BUILDER_DIR_PATH, "generated_datasets", prompt_context+"_log.txt")

# Forming the prompt from the template and template material
def render_template_with_data(template_file_path,
                              prompt_context_file_path,
                              dataset_generator_prompt_file_path,
                              num_examples_per_prompt):

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
    prompt_construction_options["num_examples"] = num_examples_per_prompt

    # Render the template with the prompt_construction_options
    prompt_to_generate_dataset = template.render(prompt_construction_options)

    # Save the prompt to a file
    with open(dataset_generator_prompt_file_path, 'w') as file:
        file.write(prompt_to_generate_dataset)

    # Remove newlines from the prompt and replace with spaces
    prompt_to_generate_dataset = prompt_to_generate_dataset.replace('\n', ' ')

    # Save the prompt to a file
    with open(dataset_generator_prompt_file_path, 'w') as file:
        file.write(prompt_to_generate_dataset)

    return prompt_to_generate_dataset



# Generate the dataset by calling the OpenAI API
def generate_dataset_from_prompt(prompt,
                                 generated_dataset_file_path,
                                 model,
                                 log_file_path,
                                 i):
    completion = client.chat.completions.create(
            **{
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
    
    completion_words = completion.choices[0].message.content.strip()

    # cleaned_completion = completion.choices[0].message.content.strip()[3:-3]
    print(" ")
    print(completion_words)
    print(" ")

    # Open a file in write mode ('w') and save the CSV data
    with open(generated_dataset_file_path+"_"+str(i), 'w', newline='', encoding='utf-8') as file:
        file.write(completion_words)

    num_words_in_prompt = count_words_in_string(prompt)
    num_words_in_completion = count_words_in_string(completion_words)
    total_words = num_words_in_prompt + num_words_in_completion

    num_tokens_in_prompt = completion.usage.prompt_tokens
    num_tokens_in_completion = completion.usage.completion_tokens
    total_tokens = num_tokens_in_prompt + num_tokens_in_completion

    prompt_cost = num_tokens_in_prompt*0.01/1000
    completion_cost = num_tokens_in_completion*0.03/1000
    total_cost = prompt_cost + completion_cost
    
    tokens_per_prompt_word = num_words_in_prompt/num_tokens_in_prompt
    tokens_per_completion_word = num_words_in_completion/num_tokens_in_completion

    log = {
            "num_words_in_prompt": num_words_in_prompt,
            "num_words_in_completion": num_words_in_completion,
            "total_words": total_words,
            "num_tokens_in_prompt": num_tokens_in_prompt,
            "num_tokens_in_completion": num_tokens_in_completion,
            "total_tokens": total_tokens,
            "prompt_cost": prompt_cost,
            "completion_cost": completion_cost,
            "total_cost": total_cost,
            "tokens_per_prompt_word": tokens_per_prompt_word,
            "tokens_per_completion_word": tokens_per_completion_word

    }

    for k, v in log.items():
        print(k, v)
    print(" ")

    with open(log_file_path, 'w') as file:
        file.write(json.dumps(log, indent=4))

def count_words_in_string(input_string):
    words = input_string.split()
    return len(words)   

start_time = time.time()

# Generate the prompt
prompt = render_template_with_data(template_file_path,
                                   prompt_context_file_path,
                                   dataset_generator_prompt_file_path,
                                   num_examples_per_prompt,
                                   )

# Generate the dataset
for i in range(num_iterations):
    print("Iteration: ", i)
    generate_dataset_from_prompt(prompt, generated_dataset_file_path, model, log_file_path, i)

end_time = time.time()

elapsed_time = end_time - start_time
print(f"The code took {elapsed_time} seconds to run.")