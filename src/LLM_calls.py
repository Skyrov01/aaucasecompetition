import base64
import os
import json
from ollama import chat
from ollama import ChatResponse


def generate_description(commits = None):

    with open('LLM_test.json', 'r') as file:
        params = json.load(file)['parameters']
    
    PROMPT = params['prompt_description']

    if commits == None:
        raise("err: no files or commits")
    

    for file, commits in commits.items():
        if file.startswith("src/"):  # Process only files that start with 'src/'
            file_name = file.split('/')[1]

            try:
                # Read the file
                with open(file_name, "r", encoding="utf-8") as file_stream:
                    file_content = file_stream.read()
                      
                # Append commits to the file content
                file_content = str(file_content) + str(commits) + PROMPT
                # Send the content to Ollama
                response = chat(model='llama3.2',

                            messages=[{'role': 'user', 'content': file_content}],
                            stream=False,
                                )
                print(response.message.content)
                return str(response.message.content)    
            except Exception as e:
                print(f"Error reading file {file}: {e}")


def generate_title(description = None):

    with open('LLM_test.json', 'r') as file:
        params = json.load(file)['parameters']
    
    PROMPT = params['prompt_title']

    if description == None:
        raise("err: no files or commits")
    PROMPT += description
    response = chat(model='llama3.2',

                messages=[{'role': 'user', 'content': PROMPT}],
                stream=False,
                    )
    print(response.message.content)
    return str(response.message.content)    



def generate_keyword():
    pass


def main():

    response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': '2 + 2?'}])

    print(response.message.content)

    # Print Ollama's response
    print(response["message"]["content"])





if __name__ == "__main__":
    main()