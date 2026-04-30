import streamlit as st
import sqlite3
import random

st.set_page_config(page_title="Sorteio Futebol", layout="wide")

st.title("⚽ Sorteio de Times")

# --- BANCO ---
conn = sqlite3.connect("jogadores.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS jogadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    posicao TEXT,
    ativo INTEGER DEFAULT 1
)
""")
conn.commit()

# --- CADASTRO ---
st.subheader("Cadastrar jogador")

nome = st.text_input("Nome do jogador")
posicao = st.selectbox("Posição", ["Goleiro", "Zagueiro", "Meio", "Atacante"])

if st.button("Adicionar jogador"):
    if nome:
        c.execute("INSERT INTO jogadores (nome, posicao) VALUES (?, ?)", (nome, posicao))
        conn.commit()
        st.success("Jogador adicionado!")

# --- LISTA ---
st.subheader("Jogadores")

c.execute("SELECT * FROM jogadores")
jogadores = c.fetchall()

ativos = []

for j in jogadores:
    presente = st.checkbox(f"{j[1]} ({j[2]})", value=True, key=j[0])
    if presente:
        ativos.append((j[1], j[2]))

# --- SORTEIO ---
def sortear():
    posicoes = {"Goleiro": [], "Zagueiro": [], "Meio": [], "Atacante": []}

    for nome, pos in ativos:
        posicoes[pos].append(nome)

    for p in posicoes:
        random.shuffle(posicoes[p])

    t1, t2 = [], []

    for p in posicoes:
        lista = posicoes[p]
        meio = len(lista)//2
        t1 += lista[:meio]
        t2 += lista[meio:]

    return t1, t2

if st.button("🎲 Sortear Times"):
    t1, t2 = sortear()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Time 1")
        for j in t1:
            st.write(j)

    with col2:
        st.subheader("Time 2")
        for j in t2:
            st.write(j)
