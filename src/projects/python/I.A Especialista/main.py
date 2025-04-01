import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Conexão com MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="iaexpert"
)
mycursor = mydb.cursor()

# Configuração da Janela Principal
root = tk.Tk()
root.title("Gerenciador de IAs")
root.geometry("600x400")

# ---- Função para mudar de tela ----
def mudar_tela(frame):
    frame.tkraise()

# ---- Tela Inicial ----
frame_inicio = tk.Frame(root)
frame_inicio.grid(row=0, column=0, sticky="nsew")

label_titulo = tk.Label(frame_inicio, text="Bem-vindo ao Gerenciador de IAs!", font=("Arial", 14))
label_titulo.pack(pady=20)

btn_escolher = tk.Button(frame_inicio, text="Escolher IA", font=("Arial", 12), command=lambda: mudar_tela(frame_escolher))
btn_escolher.pack(pady=10)

btn_criar = tk.Button(frame_inicio, text="Criar sua IA", font=("Arial", 12), command=lambda: mudar_tela(frame_criar))
btn_criar.pack(pady=10)

btn_sair = tk.Button(frame_inicio, text="Sair", font=("Arial", 12), command=root.quit)
btn_sair.pack(pady=10)

# ---- Tela Criar IA ----
frame_criar = tk.Frame(root)
frame_criar.grid(row=0, column=0, sticky="nsew")

tk.Label(frame_criar, text="Criar uma nova IA", font=("Arial", 14)).pack(pady=10)

entry_nome = tk.Entry(frame_criar, font=("Arial", 12))
entry_nome.pack(pady=5)
entry_nome.insert(0, "Nome da IA")

especialidades = []
def adicionar_especialidade():
    espec = entry_especialidade.get()
    if espec:
        especialidades.append(espec)
        lista_espec.insert(tk.END, espec)
        entry_especialidade.delete(0, tk.END)

entry_especialidade = tk.Entry(frame_criar, font=("Arial", 12))
entry_especialidade.pack(pady=5)
btn_add_espec = tk.Button(frame_criar, text="Adicionar Especialidade", command=adicionar_especialidade)
btn_add_espec.pack(pady=5)

lista_espec = tk.Listbox(frame_criar, height=5)
lista_espec.pack(pady=5)

personalidade = tk.StringVar()
tk.Label(frame_criar, text="Escolha a Personalidade:", font=("Arial", 12)).pack(pady=5)

opcoes_personalidade = ["Séria", "Dócil", "Acadêmica", "Amigável"]
dropdown_personalidade = ttk.Combobox(frame_criar, values=opcoes_personalidade, textvariable=personalidade)
dropdown_personalidade.pack(pady=5)

def salvar_ia():
    nome = entry_nome.get()
    persona = personalidade.get()
    tudo_especialidades = ", ".join(especialidades)
    
    sql = "INSERT INTO ia (id, nome, prompt, allmsgs) VALUES (default, %s, %s, %s)"
    val = (nome, f"Você é um especialista em {tudo_especialidades}. Sua personalidade é {persona}.", "")
    mycursor.execute(sql, val)
    mydb.commit()
    
    messagebox.showinfo("Sucesso", f"IA '{nome}' criada!")
    mudar_tela(frame_inicio)

btn_salvar = tk.Button(frame_criar, text="Salvar IA", command=salvar_ia)
btn_salvar.pack(pady=10)

btn_voltar = tk.Button(frame_criar, text="Voltar", command=lambda: mudar_tela(frame_inicio))
btn_voltar.pack(pady=5)

# ---- Tela Escolher IA ----
frame_escolher = tk.Frame(root)
frame_escolher.grid(row=0, column=0, sticky="nsew")

tk.Label(frame_escolher, text="Escolha uma IA", font=("Arial", 14)).pack(pady=10)

lista_ias = tk.Listbox(frame_escolher, height=10)
lista_ias.pack(pady=5)

def carregar_ias():
    lista_ias.delete(0, tk.END)
    mycursor.execute("SELECT id, nome FROM ia")
    for ia in mycursor.fetchall():
        lista_ias.insert(tk.END, f"{ia[0]}) {ia[1]}")

def iniciar_chat():
    escolha = lista_ias.curselection()
    if escolha:
        id_ia = lista_ias.get(escolha[0]).split(")")[0]
        mycursor.execute("SELECT nome, prompt FROM ia WHERE id = %s", (id_ia,))
        ia_data = mycursor.fetchone()
        ChatIa(ia_data[0], ia_data[1])

btn_iniciar = tk.Button(frame_escolher, text="Conversar", command=iniciar_chat)
btn_iniciar.pack(pady=5)

btn_voltar2 = tk.Button(frame_escolher, text="Voltar", command=lambda: mudar_tela(frame_inicio))
btn_voltar2.pack(pady=5)

carregar_ias()

# ---- Tela de Chat ----
def ChatIa(nome, promptpronto):
    frame_chat = tk.Toplevel(root)
    frame_chat.title(f"Chat - {nome}")
    frame_chat.geometry("600x400")

    chat_area = tk.Text(frame_chat, height=15, width=70)
    chat_area.pack(pady=10)
    chat_area.insert(tk.END, f"{nome} está pronto para conversar!\n")

    entry_msg = tk.Entry(frame_chat, width=50)
    entry_msg.pack(pady=5)

    historico = []

    def enviar_msg():
        question = entry_msg.get()
        if not question.strip():
            return

        historico.append(f"Usuário: {question}")
        contexto = "\n".join(historico)

        template = """
        Contexto da conversa: {context}
        Usuário: {question}
        Resposta: {prompt}
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        model = OllamaLLM(model="gemma3:12b")
        chain = prompt | model
        resposta = chain.invoke({"context": contexto, "question": question, "prompt": promptpronto})

        chat_area.insert(tk.END, f"Você: {question}\n")
        chat_area.insert(tk.END, f"{nome}: {resposta}\n\n")

        historico.append(f"{nome}: {resposta}")
        entry_msg.delete(0, tk.END)

    btn_enviar = tk.Button(frame_chat, text="Enviar", command=enviar_msg)
    btn_enviar.pack(pady=5)

    btn_sair_chat = tk.Button(frame_chat, text="Sair do Chat", command=frame_chat.destroy)
    btn_sair_chat.pack(pady=5)

# ---- Iniciando a Tela Inicial ----
mudar_tela(frame_inicio)
root.mainloop()