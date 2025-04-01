from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """Question: {question}

Answer: Lets think step by step."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="gemma3:12b ")

chain = prompt | model

print(chain.invoke({"question": "O que é o Lang Chain?"}))