from langchain.document_loaders import YoutubeLoader
from llama_index import LLMPredictor, PromptHelper, SimpleDirectoryReader, GPTSimpleVectorIndex, Document, GPTListIndex
from langchain import OpenAI
import logging
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def loadYoutubeData(url):
    loader = YoutubeLoader.from_youtube_url(
        "https://www.youtube.com/watch?v=-aYsmnlET-Q&list=PLJAzFcYKyx4RX5JBq_rXbQNmUdc9Ugbv1", add_video_info=True)
    data = loader.load()
    save_file('data/%s.json' % data[0].metadata['title'], data[0].page_content)
    return data


def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 300
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 1000

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(
        temperature=0, model_name="text-davinci-003", max_tokens=num_outputs))
    prompt_helper = PromptHelper(
        max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(
        documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )

    index.save_to_disk('./index/index.json')

    # return index


if __name__ == '__main__':
    # construct_index('./data')
    # data = loadYoutubeData(
    #     'https://www.youtube.com/watch?v=-aYsmnlET-Q&list=PLJAzFcYKyx4RX5JBq_rXbQNmUdc9Ugbv1')
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query("what's the game mechanics?")
    # index = GPTListIndex(data)
    print(response)
    # # index.save_to_disk("testIndex.json")
