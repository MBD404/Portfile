import pdfkit
import ollama
import re
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from tkinter import PhotoImage
import time


# Configurar o wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

class PDFGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de PDF Acadêmico")
        self.root.geometry("600x500")
        
        self.create_widgets()
    
    def create_widgets(self):

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        

        tk.Label(self.main_frame, text="Gerador de PDF Acadêmico", font=("Arial", 16, "bold")).pack(pady=10)
        

        tk.Label(self.main_frame, text="Nome do Autor:").pack(anchor="w")
        self.autor_entry = tk.Entry(self.main_frame, width=50)
        self.autor_entry.pack(pady=5)
        
        tk.Label(self.main_frame, text="Título do PDF:").pack(anchor="w", pady=(10,0))
        self.titulo_entry = tk.Entry(self.main_frame, width=50)
        self.titulo_entry.pack(pady=5)
        
        tk.Label(self.main_frame, text="Prompt (assunto do PDF):").pack(anchor="w", pady=(10,0))
        self.prompt_text = tk.Text(self.main_frame, width=50, height=10)
        self.prompt_text.pack(pady=5)
        

        self.gerar_btn = tk.Button(self.main_frame, text="Gerar PDF", command=self.iniciar_processo)
        self.gerar_btn.pack(pady=20)
        

        self.loading_frame = tk.Frame(self.root)
        
        self.loading_label = tk.Label(self.loading_frame, text="Gerando PDF...", font=("Arial", 14))
        self.loading_label.pack(pady=20)
        
        self.progress = ttk.Progressbar(self.loading_frame, mode='indeterminate')
        self.progress.pack(pady=10, fill="x", padx=50)
        
        self.back_btn = tk.Button(self.loading_frame, text="Voltar", command=self.voltar_tela_principal, state="disabled")
        self.back_btn.pack(pady=20)
    
    def iniciar_processo(self):
        # Obter valores dos campos
        autor = self.autor_entry.get()
        titulo = self.titulo_entry.get()
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        
        # Validar campos
        if not autor or not titulo or not prompt:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
            return
        
        # Esconder frame principal e mostrar loading
        self.main_frame.pack_forget()
        self.loading_frame.pack(pady=50, fill="both", expand=True)
        self.progress.start(10)
        
        # Iniciar thread para gerar PDF (para não travar a interface)
        thread = threading.Thread(
            target=self.gerar_pdf_thread,
            args=(autor, titulo, prompt),
            daemon=True
        )
        thread.start()
    
    def gerar_pdf_thread(self, autor, titulo, prompt):
        try:
            # Chamar a função original de gerar PDF
            response = ollama.chat(model='gemma3:12b', messages=[
                {
                    'role': 'user',
                    'content': f"""
                    use todo seu potencial para estudos academicos para formular melhor resposta,
                    Baseado nesse prompt aqui " { prompt } ".

                    Lembre-se que você deve respeitar as seguintes normas...
                    isso é importante e não deve ser desrespeitado!!! o texto deve ser construído em um padrão html,
                    com <h1> para titulos <b> para palavras em negrito <p> para parágrafos, seu trabalho é apenas 
                    construir esse texto e não comentar comentários futeis apenas construir esse texto com formato html
                    """,
                },
            ])
            
            resposta = response['message']['content']
            textofinal = re.sub(r'<think>.*?</think>', '', resposta, flags=re.DOTALL)
            
            # Gerar o PDF
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
                options={"encoding": "UTF-8"}
            )
            
            # Atualizar interface na thread principal
            self.root.after(0, self.concluir_processo)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}"))
            self.root.after(0, self.voltar_tela_principal)
    

    def concluir_processo(self):
        self.progress.stop()
        self.progress.pack_forget()  
        self.loading_label.config(text="PDF gerado com sucesso!")

        self.loading_frame.config(bg="#e8f5e9") 
        self.loading_label.config(bg="#e8f5e9")
        
        self.back_btn.config(
            state="normal",
            bg="#4caf50", 
            fg="white",
            activebackground="#2e7d32", 
            activeforeground="white"
        )
    
    def voltar_tela_principal(self):
        self.loading_frame.pack_forget()
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.loading_label.config(text="Gerando PDF...")
        self.back_btn.config(state="disabled")
        self.loading_frame.config(bg=self.root.cget("bg"))
        self.loading_label.config(bg=self.root.cget("bg"))
        self.back_btn.config(bg="SystemButtonFace", fg="black", 
                            activebackground="SystemButtonFace", activeforeground="black")
        self.progress.pack(pady=10, fill="x", padx=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFGeneratorApp(root)
    root.mainloop()