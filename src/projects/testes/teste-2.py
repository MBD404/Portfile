import pdfkit
import ollama
import re

# Configurar o wkhtmltopdf (caminho do executável)
config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe") 

def gerar_pdf():
    autor = str(input("Digite seu nome : "))
    titulo = str(input("Digite o titulo do seu pdf : "))
    prompt = str(input("Escreva sobre o que você gostaria de escrever : "))

    response = ollama.chat(model='deepseek-r1:8b', messages=[
        {
            'role': 'user',
            'content': f"""
            use todo seu potencial para estudos academicos para formular melhor resposta,
            Baseado nesse prompt aqui " { prompt } ".

            Lembre-se que você deve respeitar as seguintes normas...
            isso é importante e não deve ser desrespeitado!!! o texto deve ser construído em um padrão html,
            com <h1> para titulos <b> para palavras em negrito <p> para parágrafos, seu trabalho é apenas 
            construir esse texto e não comentar comentários futeis apenas construir esse texto com formato html

            lembre-se de não escrever ```html pra começar e nem terminar com ``` pois pode haver erros durante o processo

            """,
        },
    ])
    resposta = response['message']['content']
    filtro(resposta,autor,titulo)

def filtro(resposta,autor,titulo):
        
        textofinal = re.sub(r'<think>.*?</think>', '', resposta, flags=re.DOTALL)
        print(textofinal)
        Criarpdf(autor,titulo,textofinal)
def Criarpdf(autor,titulo,textofinal):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: "Times New Roman", Times, serif; }}
                h1 {{ color: #0066cc; text-align: center; }}
                h2 {{ color: #333; }}
                p {{ line-height: 1.6; }}
            </style>
        </head>
        <body>
            <h1>{titulo}</h1>
            <hr>
            {textofinal}
            <hr>
            <p>Autor: {autor}</p>
        </body>
        </html>
        """
    pdfkit.from_string(
           html,
            titulo+".pdf",
            configuration=config,
            options={"encoding": "UTF-8"}  # Força a codificação UTF-8
        )
    print("PDF gerado com sucesso!")

gerar_pdf()
