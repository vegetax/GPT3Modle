import openai
import os


def open_file(filepath):
    with open(filepath, 'r', encoding='UTF-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='UTF8') as outfile:
        outfile.write(content)


openai.api_key = open_file("openaiapikey.txt")


def gpt_3(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=7,
        top_p=1,
        n=1,
        temperature=0
    )
    text = response['choices'][0]['text'].strip()
    print(text)
    return text


questions = gpt_3("how are you")
