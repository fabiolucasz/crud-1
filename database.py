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
    novo_aluno = Aluno(nome="Alice", idade=50)
    session.add(novo_aluno)
    session.commit()


def alterar_dados():
    aluno = session.query(Aluno).filter(Aluno.nome == "Alice").first()

    if aluno:
        aluno.idade = 18
        session.commit()
        print("Aluno atualizado com sucesso!")
    else:
        print("Aluno não encontrado.")

# Buscar aluno para excluir
def excluir_aluno():
    aluno = session.query(Aluno).filter(Aluno.id == 2).first()

    if aluno:
        session.delete(aluno)
        session.commit()
        print("Aluno removido com sucesso!")
    else:
        print("Aluno não encontrado.")

def listar_alunos():
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        print(f"ID: {aluno.id} | Nome: {aluno.nome} | Idade: {aluno.idade}")

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

btn_novo_aluno = tk.Button(janela, text="Adicionar",
                            command=adicionar_usuario)
btn_novo_aluno.pack()

janela.mainloop()
