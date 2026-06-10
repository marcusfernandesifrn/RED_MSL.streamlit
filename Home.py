"""
RED — Modelagem e Sistemas Lineares
Entrypoint / Roteador principal (Streamlit ≥ 1.36 — st.navigation API)
"""

import streamlit as st

# ── Definição de páginas e navegação ─────────────────────────────────────────
# DEVE ser a primeira chamada Streamlit antes de qualquer outro comando

pages = {
    "🏠 Início": [
        st.Page("Home_content.py", title="Página Inicial", icon="📘", default=True),
    ],
    "📡 Sinais e Sistemas": [
        st.Page("pages/01_Sinais_e_Sistemas_Lineares.py",
                title="Sinais e Sistemas Lineares", icon="📡"),
    ],
    "🌀 Transformada de Laplace": [
        st.Page("pages/02_Transformada_de_Laplace.py",
                title="Transformada de Laplace", icon="🌀"),
    ],
    "📈 Dinâmica no Tempo": [
        st.Page("pages/03_Dinamica_Ordem_1.py",
                title="Sistemas de Ordem 1", icon="📈"),
        st.Page("pages/04_Dinamica_Ordem_2.py",
                title="Sistemas de Ordem 2", icon="📊"),
    ],
    "🔄 Análise com Realimentação": [
        st.Page("pages/05_Realimentacao_Malha_Fechada.py",
                title="Malha Fechada — Ordem 1 e 2", icon="🔄"),
        st.Page("pages/06_Realimentacao_LGR.py",
                title="Perturbação e LGR", icon="📍"),
    ],
    "⚖️ Estabilidade": [
        st.Page("pages/07_Estabilidade_Realimentacao.py",
                title="Critério de Routh-Hurwitz", icon="⚖️"),
    ],
    "📉 Resposta em Frequência": [
        st.Page("pages/08_Resposta_Frequencia.py",
                title="Diagramas de Bode", icon="📉"),
        st.Page("pages/09_Criterio_Nyquist.py",
                title="Critério de Nyquist", icon="🔁"),
    ],
    "🧮 Espaço de Estados": [
        st.Page("pages/10_Espaco_de_Estados.py",
                title="Análise no Espaço de Estados", icon="🧮"),
    ],
}

pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()
