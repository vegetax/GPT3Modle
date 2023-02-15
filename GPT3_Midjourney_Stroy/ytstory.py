import os
import openai


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


openai.api_key = open_file("../openaiapikey.txt")


def gpt_3(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        top_p=1,
        n=1,
        temperature=0.7
    )
    text = response['choices'][0]['text'].strip()
    # print(text)
    return text


step = int(input("Step: "))

# # WRITE STORY
if (step <= 1):
    ytopic = input("What is your Story About:\n\n")
    plot = open_file('Prompt_WriteStory.txt').replace('<<PLOT>>', ytopic)
    _story = gpt_3(plot)
    print('\n\nStory:', _story)
    save_file('story.txt', _story)
    input("Press Enter to Continue...")


# CREATE SCENES
if (step <= 2):
    storyinput = open_file('story.txt')
    storys = open_file('Prompt_DivideIntoScenes.txt').replace(
        '<<STORY>>', storyinput)
    _scenes = gpt_3(storys)
    print('\n\nStoryscenes:', _scenes)
    save_file('scenes.txt', _scenes)

# # MIDJOURNEY PROMPTS
if (step <= 3):
    scenes = open_file('scenes.txt')
    mjprompt = open_file('Prompt_MJ.txt')
    mjprompt1 = open_file('Prompt_SceneToMJ.txt').replace(
        '<<MJP>>', mjprompt).replace('<<SCENE>>', scenes)
    mjprompt2 = gpt_3(mjprompt1)
    print('\n\nMJ-Prompts:', mjprompt2)
    save_file('MJPrompt_Scene.txt', mjprompt2)

# # MIDJOURNEY + URL PROMPT
if (step <= 4):
    url = open_file('url.txt')
    mjScene = open_file('MJPrompt_Scene.txt')
    urlmj = open_file('Prompt_InsertUrl.txt').replace(
        '<<MJP>>', mjScene).replace('<<URL>>', url)
    urlmj2 = gpt_3(urlmj)
    print('\n\nMJ-URL-Prompts:', urlmj2)
    save_file('MJPrompt_UrlScene.txt', urlmj2)

# VOICEOVER
if (step <= 5):
    storyinput = open_file('story.txt')
    narrator = open_file('Prompt_Narrator.txt').replace(
        '<<STORY>>', storyinput)
    narrator2 = gpt_3(narrator)
    print('\n\nVO Script:', narrator2)
    save_file('VoiceoverScript.txt', narrator2)
