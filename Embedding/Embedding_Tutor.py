import openai
import numpy as np
import os


def open_file(filepath):
    with open(filepath, 'r', encoding='UTF-8') as infile:
        return infile.read()


openai.api_key = open_file("../openaiapikey.txt")


def gpt3_embeddings(input, engine='text-embedding-ada-002'):
    response = openai.Embedding.create(
        input=input,
        model=engine
    )
    embeddings = response['data'][0]['embedding']
    return embeddings


def similarity(v1, v2):
    return np.dot(v1, v2)


def match_class(vector_a, categories):
    max_similarity = 0
    best_category = None
    for category in categories:
        vector_b = gpt3_embeddings(category)
        sim = similarity(vector_a, vector_b)
        print(category, sim)
        if sim > max_similarity:
            max_similarity = sim
            best_category = category
    return best_category


categories = ['plant', 'reptile', 'mammal', 'fish']

a = input("Enter a name: ")
vector_a = gpt3_embeddings(a)

result = match_class(vector_a, categories)

print(result)
