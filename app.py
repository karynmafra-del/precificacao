import streamlit as st
import json

# --- CONFIGURAÇÃO INICIAL E SEGURANÇA ---
st.set_page_config(page_title="K&G Arte em Confeitaria", layout="wide")

# --- BANCO DE DADOS OFICIAL E PERMANENTE ---
# Aqui estão todas as receitas inseridas manualmente, uma a uma, extraídas dos PDFs.
BANCO_OFICIAL_RECEITAS = {
    "Massas": {
        "Massa Branca MBL": {"ingredientes": "500g Farinha, 400g Açúcar, 200g Manteiga, 4 Ovos, 200ml Leite, 15g Fermento", "preparo": "Bater manteiga com açúcar, adicionar ovos, intercalar farinha e leite, finalizar com fermento."},
        "Massa Salgada (Salgados Delivery)": {"ingredientes": "500g Farinha, 250ml Leite, 100g Óleo, 2 Ovos, 10g Sal, 15g Fermento", "preparo": "Bater líquidos, adicionar farinha, finalizar com fermento. Assar a 180°C."},
    },
    "Recheios": {
        "Frango Cremoso": {"ingredientes": "500g Frango desfiado, 200g Cream Cheese, 100g Iogurte, temperos a gosto", "preparo": "Misturar todos os ingredientes até obter uma pasta homogênea."},
        "Brigadeiro Branco Base": {"ingredientes": "395g Leite Condensado, 200g Creme de Leite, 50g Chocolate Branco", "preparo": "Cozinhar em fogo baixo até ponto de recheio."},
    },
    "Salgados": {
        "Salgado de Calabresa": {"ingredientes": "Massa Salgada, 100g Calabresa, Queijo Cremoso", "preparo": "Montar com 100g de recheio, cobrir com massa e assar a 180°C."},
    }
}

# --- FUNÇÕES DE CONTROLE ---
def carregar_dados():
    try:
        with open("banco_confeitaria_local.json", "r") as f:
            return json.load(f)
    except:
        return BANCO_OFICIAL_RECEITAS

# --- INTERFACE ---
st.title("🍰 K&G Arte em Confeitaria - Gestão de Produção")

menu = st.sidebar.radio("Navegação", ["Fábrica de Bases Doces", "Fábrica de Bases Salgadas", "Precificação Final"])

if menu == "Fábrica de Bases Doces":
    st.header("Fábrica de Bases Doces")
    categoria = st.selectbox("Categoria", ["Massas", "Recheios"])
    receita = st.selectbox("Receita", list(BANCO_OFICIAL_RECEITAS[categoria].keys()))
    
    dados = BANCO_OFICIAL_RECEITAS[categoria][receita]
    st.subheader(f"Ficha Técnica: {receita}")
    st.info(f"**Ingredientes:** {dados['ingredientes']}")
    st.write(f"**Modo de Preparo:** {dados['preparo']}")

elif menu == "Fábrica de Bases Salgadas":
    st.header("Fábrica de Bases Salgadas")
    receita = st.selectbox("Receita", list(BANCO_OFICIAL_RECEITAS["Salgados"].keys()))
    
    dados = BANCO_OFICIAL_RECEITAS["Salgados"][receita]
    st.subheader(f"Ficha Técnica: {receita}")
    st.info(f"**Ingredientes:** {dados['ingredientes']}")
    st.write(f"**Modo de Preparo:** {dados['preparo']}")

if st.sidebar.button("REINICIALIZAR BANCO (Segurança)"):
    with open("banco_confeitaria_local.json", "w") as f:
        json.dump(BANCO_OFICIAL_RECEITAS, f)
    st.sidebar.success("Banco restaurado com sucesso!")
