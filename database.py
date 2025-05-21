from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Criando engine e base
engine = create_engine("sqlite:///alunos.db", echo=True)
Base = declarative_base()

# Definindo o modelo (tabela)
class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    idade = Column(Integer)

# Criando tabela no banco
Base.metadata.create_all(engine)

# Criando sessão
Session = sessionmaker(bind=engine)
session = Session()

#adicionar usario
def adicionar_usuario():
    nome = entry_nome.get()
    idade = entry_idade.get()

    if nome and idade:
        novo_aluno = Aluno(nome=nome, idade=idade)
        session.add(novo_aluno)
        session.commit()

        #Deleta os campos
        entry_nome.delete(0,tk.END)
        entry_idade.delete(0,tk.END)

        listar_alunos()
    else:
        messagebox.showwarning("Aviso", "Não pode haver campo em branco!")


def alterar_dados():
    selecionado = lista.curselection()
    novo_nome = entry_nome.get()
    nova_idade = entry_idade.get()


    if selecionado and novo_nome and nova_idade:
        aluno_id = int(lista.get(selecionado).split(" | ")[0])
        aluno = session.query(Aluno).filter_by(id = aluno_id).first()
        aluno.nome = novo_nome
        aluno.idade = nova_idade
        session.commit()


        #Apaga dados
        entry_nome.delete(0,tk.END)
        entry_idade.delete(0,tk.END)

        listar_alunos()
    else:
        messagebox.showwarning("Aviso", "Selecione um usuário e preencha todas as informações!")

# Buscar aluno para excluir
def excluir_aluno():
    selecionado = lista.curselection()

    if selecionado:
        aluno_id = int(lista.get(selecionado).split(" | ")[0])
        aluno = session.query(Aluno).filter(Aluno.id == aluno_id).first()

        session.delete(aluno)
        session.commit()
        
        listar_alunos()
    else:
        messagebox.showwarning("Aviso", "Selecione o usuário que deseja excluir.")


def listar_alunos():
    lista.delete(0, tk.END)
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        lista.insert(tk.END, f"{aluno.id} | Nome: {aluno.nome} | Idade: {aluno.idade}")

#Criando a janela
import tkinter as tk

janela = tk.Tk()
janela.geometry("400x500")

#label nome e entry
label_nome = tk.Label(janela,text="Nome")
label_nome.pack()
entry_nome = tk.Entry(janela)
entry_nome.pack()

#label idade e entry
label_idade = tk.Label(janela,text="Idade")
label_idade.pack()
entry_idade = tk.Entry(janela)
entry_idade.pack()

btn_novo_aluno = tk.Button(janela, text="Adicionar", command=adicionar_usuario)
btn_novo_aluno.pack()

#Lista de alunos
lista = tk.Listbox(janela, width=50, height=15)
lista.pack()

btn_alterar = tk.Button(janela, text="Editar aluno", command=alterar_dados)
btn_alterar.pack(pady=10,padx=(90,0), side="left")

btn_excluir = tk.Button(janela, text="Excluir aluno", command=excluir_aluno)
btn_excluir.pack(pady=10,padx=(0,90), side="right")

listar_alunos()
janela.mainloop()
