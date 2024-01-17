
import pandas as pd

from textstat import flesch_kincaid_grade

# Input sentences 
sentences = [
    "Honesty",
    "I am honest",
    "I am honest to you because that is the right thing to do",
    "Honesty is good",
    "Honesty is a moral virtue", 
    "I really value honesty so I will tell you the truth", 
    "As a moral philosopher, I think highly of honest people", 
    "I believe that honesty is the highest virtue",
    "I am always honest to everyone",
    "Let me be honest to you and tell you",
]

# Custom function to estimate sentence complexity
def estimate_complexity(sentence):
    # Complexity based on the number of words and commas
    num_words = len(sentence.split())
    num_commas = sentence.count(',')
    return num_words + num_commas

# Create a list of tuples containing each sentence and its estimated complexity
sentence_complexity = [(sentence, estimate_complexity(sentence)) for sentence in sentences]

# Sort the sentences by their complexity score and length
sorted_sentences = sorted(sentence_complexity, key=lambda x: (x[1], len(x[0])))

# Creating a DataFrame to store the sorted sentences and their attributes
sentence_df = pd.DataFrame(sorted_sentences, columns=['Sentence', 'Complexity'])

# Convert the DataFrame into a matrix
sentence_matrix = sentence_df.values.tolist()
sentence_matrix