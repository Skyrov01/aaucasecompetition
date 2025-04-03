import base64
import os
import json
import ollama

def main():
    with open('LLM_test.json', 'r') as file:
        params = json.load(file)['parameters']
    
    PROMPT = params['prompt']

    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': PROMPT}],
        stream=False,
    )

    response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': '2 + 2?'}])

    print(response.message.content)


if __name__ == "__main__":
    main()
