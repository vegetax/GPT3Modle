import openai
import os


def open_file(filepath):
    with open(filepath, 'r', encoding='UTF-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='UTF8') as outfile:
        outfile.write(content)


openai.api_key = open_file("../openaiapikey.txt")


def gpt_3(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        top_p=1,
        n=1,
        temperature=0
    )
    text = response['choices'][0]['text'].strip()
    # print(text)
    return text


# 第一步：输入文章，找到问题
info = open_file("input.txt")
prompt1 = open_file("prompt1.txt").replace('<<FEED>>', info)
print(prompt1)
questions = gpt_3(prompt1)
print(questions)
save_file("questions.txt", questions)

# 第二步：回答问题
questions2 = open_file("questions.txt")
prompt2 = open_file("prompt2.txt").replace(
    '<<FEED>>', info).replace('<<QS>>', questions2)
print(prompt2)
answers = gpt_3(prompt2)
print(answers)
save_file('answers.txt', answers)
