# %%
"""Generate .csv training data programmatically."""


import csv
from textwrap import dedent

import openai



# %%
# Fix constants.
MODEL = "gpt-4-0125-preview"


# %%
# Topical prompts.
topical = []
topical.append(
    dedent(
        """
        Can you please write a prompt about honesty exactly in the following structure but with different content? You should only give one sentence after the "because" in your explanation for each one. You must continue both of the prompts, the first time with "A because" and the second time with "B because". Here's an example: 
        How should you approach honesty in your daily life? A. Definitely by lying and deceiving whenever it benefits you!, B. Always be truthful and transparent in your interactions. 
        You pick: A because 
        How should you approach honesty in your daily life? A. Definitely by lying and deceiving whenever it benefits you!, B. Always be truthful and transparent in your interactions.
        You pick: B because 
        """
    )
)

# %%
# Call
with open("pairs.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["Prompts"])
    for topic in topical:
        for i in range(100):
            completion = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": f"{topic}"
                    }
                ],
                seed=i,
            )
            writer.writerow([completion["choices"][0]["message"]["content"].strip().replace("\n", "")])
