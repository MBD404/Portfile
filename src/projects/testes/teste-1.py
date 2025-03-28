import ollama
response = ollama.chat(model='llama2-uncensored', messages=[
    {
        'role': 'user',
        'content': 'Por que o céu é azul??',
    },
])

print(response['message']['content'])