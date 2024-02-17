# %%
"""Generate .csv training data programmatically."""


import csv
from textwrap import dedent

from openai import OpenAI
client = OpenAI()


# Fix constants.
MODEL = "gpt-4-0125-preview"
NUM_EXAMPLES = 5


with open("pairs.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["Topic", "First Example", "Contrasting Example"])
    for topic, text in topical:
        for i in range(NUM_EXAMPLES):
            completion = client.chat.completions.create(model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": f"{text}"
                }
            ],
            seed=i)
            writer.writerow(
                [
                    topic,
                    *(completion.choices[0].message.content.strip().replace("\n", "")).split("(2)")
                ]
            )

# Stages
# Forming the prompt from the template and template material

