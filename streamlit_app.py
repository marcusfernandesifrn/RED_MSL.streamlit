"""
RED — Modelagem e Sistemas Lineares
streamlit_app.py — Entrypoint principal (Streamlit ≥ 1.36 — st.navigation com funções)

IMPORTANTE: este arquivo deve se chamar streamlit_app.py no repositório.
Deletar a pasta pages/ inteiramente.
"""

import streamlit as st
from collections import defaultdict

st.set_page_config(
    page_title="RED — Modelagem e Sistemas Lineares",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# CSS global (injetado uma vez pelo roteador)
# ═══════════════════════════════════════════════════════════════════════════════
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.55rem; font-weight: 800;
    line-height: 1.18; margin: 0 0 0.5rem;
}
.hero-sub { font-size: 1.03rem; opacity: 0.72; max-width: 640px; margin-bottom: 0.55rem; }
.meta-line { font-size: 0.82rem; opacity: 0.52; margin-top: 0.4rem; }

.red-badge {
    display: inline-block;
    background: linear-gradient(135deg,#3d8ef0 0%,#6c47ff 100%);
    color: #fff; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 3px 10px; border-radius: 20px;
    margin-right: 0.5rem; vertical-align: middle;
}
.stat-row {
    display: flex; gap: 2.5rem;
    margin: 1.4rem 0 2rem; padding: 1rem 0;
    border-top: 1px solid rgba(128,128,128,0.15);
    border-bottom: 1px solid rgba(128,128,128,0.15);
}
.stat-item { text-align: center; }
.stat-num  { font-size: 1.7rem; font-weight: 700; color: #3d8ef0; }
.stat-label{ font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.09em; opacity: 0.48; }

.mod-card {
    display: block;
    background: var(--background-color);
    border: 1.5px solid rgba(128,128,128,0.18);
    border-radius: 14px;
    padding: 1.1rem 1.2rem 0.95rem;
    margin-bottom: 0.75rem;
    transition: border-color .18s, box-shadow .18s, transform .12s;
    text-decoration: none !important;
    color: inherit !important;
    height: 100%;
}
.mod-card:hover {
    border-color: #3d8ef0;
    box-shadow: 0 4px 18px rgba(61,142,240,0.13);
    transform: translateY(-2px);
}
.mod-num  { font-size: 0.64rem; font-weight: 700; letter-spacing: 0.12em;
            text-transform: uppercase; opacity: 0.38; margin-bottom: 0.3rem; }
.mod-icon { font-size: 1.4rem; margin-bottom: 0.2rem; display: block; }
.mod-title{ font-size: 0.95rem; font-weight: 700; margin-bottom: 0.2rem; }
.mod-sub  { font-size: 0.75rem; opacity: 0.48; font-style: italic; margin-bottom: 0.3rem; }
.mod-desc { font-size: 0.79rem; opacity: 0.62; line-height: 1.55; margin-bottom: 0.6rem; }
.tag {
    display: inline-block; font-size: 0.67rem; padding: 2px 7px;
    border-radius: 4px; background: rgba(61,142,240,0.10);
    color: #3d8ef0; margin: 2px 2px 0 0; font-weight: 500;
}
.exp-group-title {
    font-size: 0.8rem; font-weight: 700; opacity: 0.6;
    margin: 0.85rem 0 0.25rem; letter-spacing: 0.03em;
}
.exp-grid  { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-bottom: 0.3rem; }
.exp-pill  {
    display: inline-flex; align-items: center; gap: 0.3rem;
    background: rgba(108,71,255,0.08);
    border: 1px solid rgba(108,71,255,0.18);
    border-radius: 20px; padding: 4px 11px;
    font-size: 0.76rem; color: #6c47ff; font-weight: 500;
}
.page-footer {
    margin-top: 3rem; padding: 1.2rem 0 0.5rem;
    border-top: 1px solid rgba(128,128,128,0.14);
    text-align: center; font-size: 0.79rem;
    opacity: 0.48; line-height: 1.9;
}
</style>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# PÁGINA INICIAL
# ═══════════════════════════════════════════════════════════════════════════════
def pagina_inicial():
    st.markdown(_CSS, unsafe_allow_html=True)

    st.markdown("""
<div class="hero">
  <h1>📘 Modelagem e<br>Sistemas Lineares</h1>
  <p class="hero-sub">
    <span class="red-badge">RED</span>
    Recurso Educacional Digital — material didático interativo com exploradores
    de parâmetros, simulações numéricas e fórmulas LaTeX para o curso de
    Engenharia de Energia do IFRN-CNAT.
  </p>
  <p class="meta-line">
    🎓 IFRN — Campus Natal-Central (CNAT) &nbsp;·&nbsp;
    🏛️ Engenharia de Energia &nbsp;·&nbsp;
    👤 Marcus V A Fernandes &nbsp;·&nbsp;
    ✉️ marcus.fernandes@ifrn.edu.br &nbsp;·&nbsp;
    v1.0 · 2026
  </p>
</div>
<div class="stat-row">
  <div class="stat-item"><div class="stat-num">7</div><div class="stat-label">Módulos</div></div>
  <div class="stat-item"><div class="stat-num">10</div><div class="stat-label">Submódulos</div></div>
  <div class="stat-item"><div class="stat-num">34</div><div class="stat-label">Exploradores</div></div>
  <div class="stat-item"><div class="stat-num">60+</div><div class="stat-label">Figuras</div></div>
  <div class="stat-item"><div class="stat-num">100%</div><div class="stat-label">Online</div></div>
</div>
""", unsafe_allow_html=True)

    # ── Sobre ────────────────────────────────────────────────────────────────
    st.markdown("### 📖 Sobre este RED")
    st.markdown("""
Este **Recurso Educacional Digital** cobre a disciplina *Modelagem e Sistemas Lineares*
do curso de Engenharia de Energia do IFRN-CNAT. O material é organizado em módulos
progressivos — de fundamentos de sinais até representação em espaço de estados — com
ênfase em compreensão visual e exploração paramétrica.

Cada módulo combina **teoria** com equações e exemplos analíticos, **figuras** geradas
numericamente e **exploradores interativos** com sliders e campos de entrada para observar
o efeito de parâmetros em tempo real, sem necessidade de reexecução.
""")

    # ── Índice ────────────────────────────────────────────────────────────────
    with st.expander("📋 Índice geral — clique para expandir", expanded=False):
        st.markdown("""
**1 · Sinais e Sistemas Lineares** `📡`

&nbsp;&nbsp;&nbsp;· Definição de sinais e sistemas LTI — LCIT  
&nbsp;&nbsp;&nbsp;· Operações: deslocamento, inversão, escalonamento  
&nbsp;&nbsp;&nbsp;· Propriedades: linearidade, invariância, causalidade, memória, estabilidade  
&nbsp;&nbsp;&nbsp;· Resposta ao impulso e convolução  
&nbsp;&nbsp;&nbsp;· Diagrama de blocos: série, paralelo, realimentação  
&nbsp;&nbsp;&nbsp;· Explorador de operações com sinais

---
**2 · Transformada de Laplace** `🌀`

&nbsp;&nbsp;&nbsp;· Definição bilateral e unilateral — tabela de pares e propriedades  
&nbsp;&nbsp;&nbsp;· Convolução no tempo ↔ multiplicação em s  
&nbsp;&nbsp;&nbsp;· Função de transferência — polos, zeros, estabilidade  
&nbsp;&nbsp;&nbsp;· Realizações: direta, cascata, paralela e aproximação de Padé  
&nbsp;&nbsp;&nbsp;· Sistemas não-lineares e linearização por série de Taylor  
&nbsp;&nbsp;&nbsp;· Frações parciais: raízes reais, complexas e repetidas  
&nbsp;&nbsp;&nbsp;· Explorador de linearização (ordem 1 a 5)

---
**3 · Dinâmica no Domínio do Tempo**

**3.1 · Sistemas de Ordem 1** `📈`

&nbsp;&nbsp;&nbsp;· Grau relativo, ganho DC k/a, constante de tempo τ = 1/a  
&nbsp;&nbsp;&nbsp;· Resposta ao degrau: componentes forçada e natural; y(∞), Tr, Ts  
&nbsp;&nbsp;&nbsp;· Exemplos físicos: RL, RC, massa-amortecedor, inércia, térmico, hidráulico  
&nbsp;&nbsp;&nbsp;· Efeito do zero: fase mínima, cancelamento, fase não-mínima  
&nbsp;&nbsp;&nbsp;· Polo no SPD (instável) e polo na origem (integrador)  
&nbsp;&nbsp;&nbsp;· 5 exploradores interativos

**3.2 · Sistemas de Ordem 2** `📊`

&nbsp;&nbsp;&nbsp;· Forma canônica: ξ, ωn, k — regimes de amortecimento  
&nbsp;&nbsp;&nbsp;· Especificações: UP%, Tp, Tr, Ts — fórmulas analíticas  
&nbsp;&nbsp;&nbsp;· Parametrização direta por σ e ωd  
&nbsp;&nbsp;&nbsp;· Exemplos físicos: massa-mola-amortecedor, circuito RLC  
&nbsp;&nbsp;&nbsp;· Polos e zeros adicionais com toggles ON/OFF  
&nbsp;&nbsp;&nbsp;· 6 exploradores interativos

---
**4 · Análise de Sistemas com Realimentação**

**4.1 · Ordem 1 e 2 em Malha Fechada** `🔄`

&nbsp;&nbsp;&nbsp;· HMF(s) = G/(1+G) — tipo do sistema, Kp, Kv, Ka  
&nbsp;&nbsp;&nbsp;· Erro em regime permanente: degrau, rampa, parábola  
&nbsp;&nbsp;&nbsp;· Planta 1ª e 2ª ordem: efeito do ganho k nos polos MF  
&nbsp;&nbsp;&nbsp;· 3 exploradores com plano s, y(t) e e(t)

**4.2 · Perturbação e LGR** `📍`

&nbsp;&nbsp;&nbsp;· Plantas de ordem superior — ganho crítico via Routh  
&nbsp;&nbsp;&nbsp;· Perturbação D(s) — e_rp,D = −1/(a+k)  
&nbsp;&nbsp;&nbsp;· LGR — quadro 4×4 de 16 sistemas e explorador interativo  
&nbsp;&nbsp;&nbsp;· 3 exploradores interativos

---
**5 · Estabilidade de Sistemas com Realimentação** `⚖️`

&nbsp;&nbsp;&nbsp;· Critério de Routh-Hurwitz: zero isolado (ε) e linha de zeros  
&nbsp;&nbsp;&nbsp;· 4 exemplos numéricos com tabela de Routh interativa  
&nbsp;&nbsp;&nbsp;· Região de estabilidade no plano (k, a₂)  
&nbsp;&nbsp;&nbsp;· 2 exploradores interativos

---
**6 · Resposta em Frequência de Sistemas**

**6.1 · Diagramas de Bode** `📉`

&nbsp;&nbsp;&nbsp;· 6 fatores elementares com tabs individuais  
&nbsp;&nbsp;&nbsp;· Margens φm e Gm, banda passante e pico de ressonância  
&nbsp;&nbsp;&nbsp;· Nichols, filtros Butterworth e explorador geral de Bode

**6.2 · Critério de Nyquist** `🔁`

&nbsp;&nbsp;&nbsp;· Princípio do Argumento N = Z−P, contorno de Nyquist  
&nbsp;&nbsp;&nbsp;· Comparação sincronizada Nyquist × Bode × LGR  
&nbsp;&nbsp;&nbsp;· Explorador: diagnóstico automático P, N, Z, φm, Gm

---
**7 · Análise de Sistemas no Espaço de Estados** `🧮`

&nbsp;&nbsp;&nbsp;· Equações de estado: ẋ=Ax+Bu, y=Cx+Du  
&nbsp;&nbsp;&nbsp;· Realizações CCF, OCF, cascata, paralela  
&nbsp;&nbsp;&nbsp;· Matriz e^{At}: propriedades, Cayley-Hamilton, forma modal  
&nbsp;&nbsp;&nbsp;· Controlabilidade Wc e observabilidade Wo  
&nbsp;&nbsp;&nbsp;· 3 exploradores: SS, FT→SS, SS→FT
""")

    # ── Cards de módulos ──────────────────────────────────────────────────────
    st.markdown("### 🗂️ Módulos do curso")
    st.caption("Selecione um módulo no menu lateral ou clique num card para acessar.")

    MODULES = [
        ("MOD 01","📡","Sinais e Sistemas Lineares","",
         "Fundamentos de sinais e sistemas LTI: superposição, causalidade, estabilidade BIBO, "
         "convolução e diagramas de blocos em série, paralelo e realimentação.",
         ["LCIT","Convolução","Diagramas de blocos","Superposição"],
         "Sinais_e_Sistemas_Lineares"),
        ("MOD 02","🌀","Transformada de Laplace","",
         "Definição, tabela de pares, propriedades e frações parciais. "
         "Função de transferência, realizações de sistemas e linearização por Taylor.",
         ["Laplace","Frações parciais","Linearização","FT"],
         "Transformada_de_Laplace"),
        ("MOD 03","📈","Dinâmica no Domínio do Tempo","Sistemas de Ordem 1",
         "Resposta ao degrau: y(∞), τ, Tr, Ts. Efeito de polo/zero. "
         "Exemplos físicos (RL, RC, mecânico, térmico). Fase mínima e não-mínima.",
         ["Ordem 1","Degrau","Polo/Zero","Fase mínima"],
         "Dinamica_Ordem_1"),
        ("MOD 03","📊","Dinâmica no Domínio do Tempo","Sistemas de Ordem 2",
         "Coeficiente ξ, frequência ωₙ e especificações UP%, Tp, Tr, Ts. "
         "Polos e zeros adicionais com toggle ON/OFF. Sistema oscilatório.",
         ["Ordem 2","Amortecimento","UP%","Polos complexos"],
         "Dinamica_Ordem_2"),
        ("MOD 04","🔄","Análise com Realimentação","Malha Fechada — Ordem 1 e 2",
         "HMF(s) = G/(1+G). Tipo do sistema e constantes de erro Kp, Kv, Ka. "
         "Efeito de k nos polos MF e compromisso erro × amortecimento.",
         ["Malha fechada","Erro","Tipo do sistema","Polos MF"],
         "Realimentacao_Malha_Fechada"),
        ("MOD 04","📍","Análise com Realimentação","Perturbação e LGR",
         "Plantas de ordem superior, rejeição de perturbação e e_rp,D = −1/(a+k). "
         "LGR com quadro 4×4 de 16 sistemas e explorador interativo N(s)/D(s).",
         ["LGR","Perturbação","Ordem superior","k_crit"],
         "Realimentacao_LGR"),
        ("MOD 05","⚖️","Estabilidade com Realimentação","Critério de Routh-Hurwitz",
         "Critério de Routh-Hurwitz com casos especiais (ε e polinômio auxiliar). "
         "4 exemplos numéricos com tabela interativa e região de estabilidade.",
         ["Routh-Hurwitz","k_crit","Região de estabilidade","Marginal"],
         "Estabilidade_Realimentacao"),
        ("MOD 06","📉","Resposta em Frequência","Diagramas de Bode",
         "6 fatores elementares, margens φm e Gm, banda passante e pico de ressonância. "
         "Diagrama de Nichols e filtros Butterworth (PB, PA, PF, RF).",
         ["Bode","Margens","Nichols","Filtros"],
         "Resposta_Frequencia"),
        ("MOD 06","🔁","Resposta em Frequência","Critério de Nyquist",
         "Princípio do Argumento N = Z−P. Contorno de Nyquist, desvio em polos e margens. "
         "Comparação sincronizada Nyquist × Bode × LGR com marcos de fase.",
         ["Nyquist","N=Z−P","Margens","Mapeamento"],
         "Criterio_Nyquist"),
        ("MOD 07","🧮","Espaço de Estados","",
         "Equações ẋ=Ax+Bu. Realizações CCF/OCF. Matriz e^{At} via Cayley-Hamilton. "
         "Controlabilidade Wc e observabilidade Wo. Conversores FT↔SS.",
         ["Estado","Controlabilidade","Observabilidade","e^{At}"],
         "Espaco_de_Estados"),
    ]

    for row_start in range(0, len(MODULES), 3):
        cols = st.columns(3, gap="medium")
        for ci, mod in enumerate(MODULES[row_start:row_start+3]):
            num,icon,title,sub,desc,tags,_ = mod
            tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
            sub_html  = f'<div class="mod-sub">↳ {sub}</div>' if sub else ""
            with cols[ci]:
                st.markdown(f"""
<div class="mod-card">
  <div class="mod-num">{num}</div>
  <span class="mod-icon">{icon}</span>
  <div class="mod-title">{title}</div>
  {sub_html}
  <div class="mod-desc">{desc}</div>
  <div style="margin-top:0.5rem">{tags_html}</div>
</div>""", unsafe_allow_html=True)

    # ── Exploradores ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🎛️ Exploradores interativos")
    st.markdown(
        "Os **exploradores** são o diferencial deste RED — sliders, selectboxes e campos de "
        "entrada com atualização em tempo real, sem necessidade de reexecução."
    )

    EXPLORERS = [
        ("📡 Sinais e Sistemas",[("📡","Operações com sinais — deslocamento, escala, inversão")]),
        ("🌀 Transformada de Laplace",[("🌀","Linearização por Taylor — ordem 1 a 5")]),
        ("📈 Dinâmica — Ordem 1",[
            ("📈","Resposta ao degrau — k, a, kr"),
            ("📈","Plano s + degrau — k e a"),
            ("📈","Sistema com zero — k, a, b"),
            ("📈","Sistema instável — velocidade de divergência"),
            ("📈","Polo MA vs. MF — integrador com realimentação"),
        ]),
        ("📊 Dinâmica — Ordem 2",[
            ("📊","Regimes de amortecimento — ξ, ωn"),
            ("📊","Plano s + especificações — ξ, ωn"),
            ("📊","Efeito de ξ, ωn e k"),
            ("📊","Parâmetros σ e ωd — polos complexos diretos"),
            ("📊","Polo e zero adicionais — toggles ON/OFF"),
            ("📊","Sistema oscilatório — k → ωn = √k"),
        ]),
        ("🔄 Realimentação — MF",[
            ("🔄","Tipo do sistema, entrada e ganho k"),
            ("🔄","Planta 1ª ordem — entrada, k e atraso"),
            ("🔄","Planta 2ª ordem — entrada, k e atraso"),
        ]),
        ("📍 Realimentação — LGR",[
            ("📍","Estabilidade de ordem superior — k e atraso"),
            ("📍","Seguimento vs. rejeição de perturbação"),
            ("📍","LGR interativo — N(s)/D(s) e k_max livre"),
        ]),
        ("⚖️ Estabilidade",[
            ("⚖️","Polos MF em função de k — 🟢/🟡/🔴"),
            ("⚖️","Região de estabilidade — plano (k, a₂)"),
        ]),
        ("📉 Bode",[
            ("📉","6 fatores elementares — tabs com slider"),
            ("📉","Margens φm e Gm — insira N(s)/D(s)"),
            ("📉","Bode 1ª ordem — k e a"),
            ("📉","Bode 2ª ordem — k, ξ, ωn"),
            ("📉","Nichols — ξ múltiplos com multiselect"),
            ("📉","Filtros Butterworth — tipo e ordem (1–10)"),
            ("📉","Explorador geral — ωc, φm, Gm automáticos"),
        ]),
        ("🔁 Nyquist",[
            ("🔁","Efeito do ganho K — curva escala 🟢/🟡/🔴"),
            ("🔁","Nyquist × Bode × LGR — marcos sincronizados"),
            ("🔁","Explorador Nyquist — P, N, Z, φm, Gm"),
        ]),
        ("🧮 Espaço de Estados",[
            ("🧮","Explorador SS — insira A, B, C, D"),
            ("🧮","Conversor FT → SS"),
            ("🧮","Conversor SS → FT"),
        ]),
    ]

    half = (len(EXPLORERS)+1)//2
    col_l, col_r = st.columns(2)
    for col, grupo in zip([col_l,col_r],[EXPLORERS[:half],EXPLORERS[half:]]):
        with col:
            for gtitle, items in grupo:
                pills="".join(
                    f'<span class="exp-pill"><span>{ic}</span> {nm}</span>'
                    for ic,nm in items)
                st.markdown(
                    f'<p class="exp-group-title">{gtitle}</p>'
                    f'<div class="exp-grid">{pills}</div>',
                    unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="page-footer">
  Modelagem e Sistemas Lineares &nbsp;·&nbsp;
  Engenharia de Energia &nbsp;·&nbsp;
  CNAT — IFRN<br>
  Autor: Marcus V A Fernandes &nbsp;·&nbsp;
  marcus.fernandes@ifrn.edu.br &nbsp;·&nbsp;
  v1.0 · 2026
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PÁGINAS — importações lazy (só quando a página é executada)
# ═══════════════════════════════════════════════════════════════════════════════
def pagina_sinais():
    import modulos.sinais_e_sistemas_lineares as m; m  # noqa — executa o módulo

def pagina_laplace():
    import modulos.transformada_de_laplace as m; m  # noqa

def pagina_ord1():
    import modulos.dinamica_sistemas_ordem_1 as m; m  # noqa

def pagina_ord2():
    import modulos.dinamica_sistemas_ordem_2 as m; m  # noqa

def pagina_mf():
    import modulos.realimentacao_malha_fechada as m; m  # noqa

def pagina_lgr():
    import modulos.realimentacao_lgr as m; m  # noqa

def pagina_estab():
    import modulos.estabilidade_realimentacao as m; m  # noqa

def pagina_bode():
    import modulos.resposta_frequencia as m; m  # noqa

def pagina_nyquist():
    import modulos.criterio_nyquist as m; m  # noqa

def pagina_ss():
    import modulos.espaco_de_estados as m; m  # noqa


# ═══════════════════════════════════════════════════════════════════════════════
# ROTEADOR PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
_pages = {
    "🏠 Início": [
        st.Page(pagina_inicial, title="Página Inicial", icon="📘", default=True),
    ],
    "📡 Sinais e Sistemas": [
        st.Page(pagina_sinais, title="Sinais e Sistemas Lineares", icon="📡"),
    ],
    "🌀 Transformada de Laplace": [
        st.Page(pagina_laplace, title="Transformada de Laplace", icon="🌀"),
    ],
    "📈 Dinâmica no Tempo": [
        st.Page(pagina_ord1, title="Sistemas de Ordem 1", icon="📈"),
        st.Page(pagina_ord2, title="Sistemas de Ordem 2", icon="📊"),
    ],
    "🔄 Análise com Realimentação": [
        st.Page(pagina_mf,  title="Malha Fechada — Ordem 1 e 2", icon="🔄"),
        st.Page(pagina_lgr, title="Perturbação e LGR",           icon="📍"),
    ],
    "⚖️ Estabilidade": [
        st.Page(pagina_estab, title="Critério de Routh-Hurwitz", icon="⚖️"),
    ],
    "📉 Resposta em Frequência": [
        st.Page(pagina_bode,   title="Diagramas de Bode",    icon="📉"),
        st.Page(pagina_nyquist, title="Critério de Nyquist", icon="🔁"),
    ],
    "🧮 Espaço de Estados": [
        st.Page(pagina_ss, title="Análise no Espaço de Estados", icon="🧮"),
    ],
}

pg = st.navigation(_pages, position="sidebar", expanded=True)
pg.run()
