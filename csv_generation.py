# %%
"""Generate .csv training data programmatically."""


import csv
from textwrap import dedent

import openai



# %%
# Fix constants.
MODEL = "gpt-4-0125-preview"
NUM_EXAMPLES = 5


# %%
# Topical prompts.
topical = []
topical.append(
#     (    
#         "[insert concept]",
#         dedent(        
#         """Could you please write a prompt about [insert concept] that branches into two continuations the way I do it in the following example? Please write the answer directly. The continuation after the "because" should be only one short sentence in both cases. Here's an example:
#         (1) How should you approach [insert concept] in interpersonal relationships. You should: A. [Insert first continuation], B. [Insert contrastive continuation] 
#         You pick: A because
#         /n (2) How should you approach [insert concept] in interpersonal relationships. You should: A. [Insert first continuation], B. [Insert contrastive continuation] 
#         You pick: B because"""
#         )
#     )
# )

topical.append(
        (
        "honesty",
        dedent(
            """Could you please write a prompt about honesty that branches into two continuations the way I do it in the following example? Plese write the answer directly. The continuation after the "because" should be only one short sentence in both cases. Here's an example: 
            (1) How should you approach honesty in your daily life? A. Definitely by lying and deceiving whenever it benefits you!, B. Always be truthful and transparent in your interactions. 
            You pick: A because 
            (2) How should you approach honesty in your daily life? A. Definitely by lying and deceiving whenever it benefits you!, B. Always be truthful and transparent in your interactions.
            You pick: B because""" 
        )
    )
)
topical.append(
    (
        "trust",
        dedent(
            """Could you please write a prompt about trust that branches into two continuations the way I do it in the following example? Please write the answer directly. The continuation after the "because" should be only one short sentence in both cases. Here's an example:
            (1) You are tempted to break a promise you have made to your friend. You should: A. Break your promise and move on!, B. You keep your promise even if it's difficult for you.
            You pick: A because 
            /n (2) You are tempted to break a promise you have made to your friend. You should: A. Break your promise and move on!, B. You keep your promise even if it's difficult for you.
            You pick: B because"""
        )
    )
  )
topical.append(
    (    
        "respect",
        dedent(        
        """Could you please write a prompt about respect that branches into two continuations the way I do it in the following example? Please write the answer directly. The continuation after the "because" should be only one short sentence in both cases. Here's an example:
        (1) How should you approach respect in interpersonal relationships. You should: A. Always respect everyone!, B. Disrespect others whenever it's convenient for you. 
        You pick: A because
        /n (2) How should you approach respect in interpersonal relationships. You should: A. Always respect everyone!, B. Disrespect others whenever it's convenient for you. 
        You pick: B because"""
        )
    )
)

topical.append(
    (
         "compassion",
          dedent(
          """Could you please write a prompt about compassion that branches into two continuations the way I do it in the following example? Please write the answer directly. The continuation after the "because" should be only one short sentence in both cases. Here's an example:
          (1) How should you approach compassion in your everyday life? You should A. Always show compassion to those who need it!, B. Be ruthless, there's no room for compassion in this world.
          You pick: A because
          /n (2) How should you approach compassion in your everyday life? You should A. Always show compassion to those who need it!, B. Be ruthless, there's no room for compassion in this world.
          You pick: B because"""
          )
     )
)
topical.append(
    (
        "justice",
        dedent(
            """Could you please write a prompt about justice that branches into two continuations the way I do it in the following example? Please write the answer directly. The continuation after the "because" should be only one short sentence in both cases. Here's an example:
            (1) If you were a judge would you try to  You should: A. Break your promise and move on!, B. You keep your promise even if it's difficult for you.
            You pick: A because 
            /n (2) You are tempted to break a promise you have made to your friend. You should: A. Break your promise and move on!, B. You keep your promise even if it's difficult for you.
            You pick: B because"""
        )
    )
  )
topical.append(
(
        "freedom",
        dedent(
            """Could you please write a prompt about freedom that branches into two continuations the way I do it in the following example? Please write the answer directly. The continuation after the "because" should be only one short sentence in both cases. Here's an example:
            (1) When the freedom of others is at stake, you should: A. Fight for it like it's about your own freedom, B. Not bother if it doesn't impact you directly.
            You pick: A because 
            /n (2) When the freedom of others is at stake, you should: A. Fight for it like it's about your own freedom, B. Not bother if it doesn't impact you directly.
            You pick: B because"""
        )
    )
)

# %%
# Call
with open("pairs.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["Topic", "First Example", "Contrasting Example"])
    for topic, text in topical:
        for i in range(NUM_EXAMPLES):
            completion = openai.ChatCompletion.create(
                model=MODEL,
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
                seed=i,
            )
            writer.writerow(
                [
                    topic,
                    *(completion["choices"][0]["message"]["content"].strip().replace("\n", "")).split("(2)")
                ]
            )
