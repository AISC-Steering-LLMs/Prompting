import csv

from openai import OpenAI
client = OpenAI()

model = "gpt-4-0125-preview"

# Getting LLM to output additional columns
# This all needs condensing.

def ask_openai(prompt):
    completion = client.chat.completions.create(
                **{
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
    return completion.choices[0].message.content.strip()

input_file_path = "prompts/pairs_v1/generated_datasets/honesty_dataset_single.csv"
output_file_path = "prompts/pairs_v1/generated_datasets/honesty_dataset_single_labelled.csv"


with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Assuming the CSV has a header, you might want to write a new header for the output file
    writer.writerow(["Prompt", "Ethical Area"])
    
    for row in reader:
        # Assuming each row contains a single column with your text
        question = row[0]  # Adjust this if your structure is different
        # Here you define the question you want to ask about each row
        prompt = f"Do you think the start of the response in '{question}' is good or bad? Output only the word good for good, and bad for bad in single word response."
        response = ask_openai(prompt)
        # Add the OpenAI response to the row
        row.append(response)
        writer.writerow(row)



# Note we might not need to query the API for kind of lebelling
# Eg if we know the questions always go good, bad, good, bad, good etc

input_file_path = "prompts/pairs_v1/generated_datasets/honesty_dataset_single_labelled.csv"
output_file_path = "prompts/pairs_v1/generated_datasets/honesty_dataset_single_labelled_twice.csv"

with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # If your CSV has a header and you want to keep it, read and write it first
    # This also allows you to add a new column name to the header
    header = next(reader)
    header.append("OddOrEven")  # Add your new column name here
    writer.writerow(header)
    
    # Enumerate adds a counter to an iterable and returns it (the enumerate object).
    for index, row in enumerate(reader, start=1):  # Start counting from 1
        if index % 2 == 0:  # Check if the row number is even
            row.append(0)
        else:
            row.append(1)
        writer.writerow(row)