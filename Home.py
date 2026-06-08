import streamlit as st

st.set_page_config(
    page_title="RED — Modelagem e Sistemas Lineares",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

.hero { padding: 2rem 0 1.5rem; }
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem; font-weight: 800;
    line-height: 1.15; margin-bottom: 0.4rem;
}
.hero p { font-size: 1.05rem; opacity: 0.7; max-width: 600px; }
.meta { font-size: 0.85rem; opacity: 0.6; margin-top: 0.8rem; }

.card {
    background: var(--background-color);
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 14px;
    padding: 1.2rem 1.3rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
    height: 100%;
}
.card:hover { border-color: rgba(61,142,240,0.5); }
.card-num {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; opacity: 0.5; margin-bottom: 0.4rem;
}
.card-title { font-size: 1rem; font-weight: 600; margin-bottom: 0.4rem; }
.card-desc { font-size: 0.82rem; opacity: 0.65; line-height: 1.55; margin-bottom: 0.7rem; }
.tag {
    display: inline-block; font-size: 0.7rem; padding: 2px 8px;
    border-radius: 4px; background: rgba(128,128,128,0.12);
    margin: 2px; opacity: 0.8;
}
.stat-row {
    display: flex; gap: 2rem; margin: 1.2rem 0 2rem;
    padding: 1rem 0; border-top: 1px solid rgba(128,128,128,0.15);
    border-bottom: 1px solid rgba(128,128,128,0.15);
}
.stat-item { text-align: center; }
.stat-num { font-size: 1.6rem; font-weight: 700; color: #3d8ef0; }
.stat-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.5; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>📘 Modelagem e<br>Sistemas Lineares</h1>
  <p>Material didático interativo com simulações Python, fórmulas LaTeX e exploradores de parâmetros.</p>
  <div class="meta">
    🎓 IFRN — Campus Natal-Central &nbsp;·&nbsp;
    👤 Marcus V A Fernandes &nbsp;·&nbsp;
    ✉️ marcus.fernandes@ifrn.edu.br
  </div>
</div>
<div class="stat-row">
  <div class="stat-item"><div class="stat-num">10</div><div class="stat-label">Módulos</div></div>
  <div class="stat-item"><div class="stat-num">40+</div><div class="stat-label">Exploradores</div></div>
  <div class="stat-item"><div class="stat-num">100%</div><div class="stat-label">Interativo</div></div>
  <div class="stat-item"><div class="stat-num">Python</div><div class="stat-label">Plataforma</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("### Módulos do curso")
st.caption("Selecione um módulo no menu lateral para acessar o conteúdo.")

modules = [
    ("MOD 01", "📡", "Sinais e Sistemas Lineares",
     "Definições, superposição, causalidade, estabilidade e diagramas de blocos.",
     ["Fundamentos", "Superposição", "Diagramas de blocos"]),
    ("MOD 02", "∫", "Transformada de Laplace",
     "Definição, propriedades, frações parciais, função de transferência e linearização.",
     ["Laplace", "Frações parciais", "Linearização"]),
    ("MOD 03", "📈", "Dinâmica — Sistemas de 1ª Ordem",
     "Resposta ao degrau, polos, zeros, grau relativo e sistemas instáveis.",
     ["Ordem 1", "Resposta ao degrau", "Polo/zero"]),
    ("MOD 04", "〰", "Dinâmica — Sistemas de 2ª Ordem",
     "Amortecimento ξ, frequência natural ωₙ, especificações UP, Ts, Tr.",
     ["Ordem 2", "Amortecimento", "Especificações"]),
    ("MOD 05", "📊", "Resposta em Frequência",
     "Diagramas de Bode, Nichols, margens de ganho e fase, banda passante.",
     ["Bode", "Nichols", "Filtros", "Margens"]),
    ("MOD 06", "🔄", "Realimentação — Malha Fechada",
     "Estrutura de malha fechada, erro em regime permanente, tipo do sistema.",
     ["Malha fechada", "Erro estacionário", "Tipo do sistema"]),
    ("MOD 07", "⚖️", "Estabilidade com Realimentação",
     "Critério de Routh-Hurwitz, ganho crítico e região de estabilidade.",
     ["Routh-Hurwitz", "Ganho crítico", "Polos MF"]),
    ("MOD 08", "🗺️", "Lugar Geométrico das Raízes",
     "LGR interativo, plantas de ordem superior, erro com perturbação.",
     ["LGR", "Root Locus", "Perturbação"]),
    ("MOD 09", "🌀", "Critério de Nyquist",
     "Mapeamento de contornos, princípio do argumento e margens.",
     ["Nyquist", "Estabilidade", "Margens"]),
    ("MOD 10", "🔢", "Espaço de Estados",
     "Representação interna, equações de estado, controlabilidade e observabilidade.",
     ["Estado", "Controlabilidade", "Observabilidade"]),
]

cols_per_row = 3
for row_start in range(0, len(modules), cols_per_row):
    cols = st.columns(cols_per_row)
    for col_idx, mod in enumerate(modules[row_start:row_start + cols_per_row]):
        num, icon, title, desc, tags = mod
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
        with cols[col_idx]:
            st.markdown(f"""
            <div class="card">
              <div class="card-num">{num}</div>
              <div class="card-title">{icon} {title}</div>
              <div class="card-desc">{desc}</div>
              <div>{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia · Python · Streamlit · Plotly · SciPy")
