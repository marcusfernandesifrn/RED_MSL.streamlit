"""
RED — Modelagem e Sistemas Lineares
streamlit_app.py — Entrypoint principal (Streamlit ≥ 1.36)
"""

import streamlit as st
from collections import defaultdict

st.set_page_config(
    page_title="RED — Modelagem e Sistemas Lineares",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS global ────────────────────────────────────────────────────────────────
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
    display: flex; gap: 2.5rem; margin: 1.4rem 0 2rem; padding: 1rem 0;
    border-top: 1px solid rgba(128,128,128,0.15);
    border-bottom: 1px solid rgba(128,128,128,0.15);
}
.stat-item { text-align: center; }
.stat-num   { font-size: 1.7rem; font-weight: 700; color: #3d8ef0; }
.stat-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.09em; opacity: 0.48; }

/* módulo card — visual apenas (clique via st.page_link sobreposto) */
.mod-card {
    border: 1.5px solid rgba(128,128,128,0.18);
    border-radius: 14px;
    padding: 1.05rem 1.15rem 0.85rem;
    transition: border-color .18s, box-shadow .18s, transform .12s;
    margin-bottom: 0;
    height: 100%;
}
.mod-card:hover {
    border-color: #3d8ef0;
    box-shadow: 0 4px 18px rgba(61,142,240,0.13);
    transform: translateY(-2px);
}
.mod-num  { font-size: 0.64rem; font-weight: 700; letter-spacing: .12em;
            text-transform: uppercase; opacity: .38; margin-bottom: .3rem; }
.mod-icon { font-size: 1.4rem; margin-bottom: .2rem; display: block; }
.mod-title{ font-size: 0.95rem; font-weight: 700; margin-bottom: .15rem; }
.mod-sub  { font-size: 0.75rem; opacity: .48; font-style: italic; margin-bottom: .3rem; }
.mod-desc { font-size: 0.79rem; opacity: .62; line-height: 1.55; margin-bottom: .5rem; }
.tag {
    display: inline-block; font-size: 0.67rem; padding: 2px 7px;
    border-radius: 4px; background: rgba(61,142,240,.10);
    color: #3d8ef0; margin: 2px 2px 0 0; font-weight: 500;
}
/* exploradores */
.exp-group-title {
    font-size: .8rem; font-weight: 700; opacity: .6;
    margin: .85rem 0 .2rem; letter-spacing: .03em;
}
.exp-grid { display: flex; flex-wrap: wrap; gap: .4rem; margin-bottom: .2rem; }
/* footer */
.page-footer {
    margin-top: 3rem; padding: 1.2rem 0 0.5rem;
    border-top: 1px solid rgba(128,128,128,.14);
    text-align: center; font-size: .79rem; opacity: .48; line-height: 1.9;
}
/* forçar page_link visual como pill */
div[data-testid="stPageLink"] a {
    display: inline-flex !important;
    align-items: center;
    gap: 0.3rem;
    background: rgba(108,71,255,.08) !important;
    border: 1px solid rgba(108,71,255,.20) !important;
    border-radius: 20px !important;
    padding: 4px 13px !important;
    font-size: .76rem !important;
    color: #6c47ff !important;
    font-weight: 500 !important;
    text-decoration: none !important;
    transition: background .15s, border-color .15s;
}
div[data-testid="stPageLink"] a:hover {
    background: rgba(108,71,255,.15) !important;
    border-color: #6c47ff !important;
}
/* page_link de card: full width, sem estilo extra */
div[data-testid="stPageLink"].card-link a {
    display: block !important;
    border-radius: 12px !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    font-size: 1rem !important;
    color: inherit !important;
}
</style>
"""

# ── Funções de página ─────────────────────────────────────────────────────────
def pagina_inicial():
    _home()

def pagina_sinais():
    import modulos.sinais_e_sistemas_lineares as m; m.run()

def pagina_laplace():
    import modulos.transformada_de_laplace as m; m.run()

def pagina_ord1():
    import modulos.dinamica_sistemas_ordem_1 as m; m.run()

def pagina_ord2():
    import modulos.dinamica_sistemas_ordem_2 as m; m.run()

def pagina_mf():
    import modulos.realimentacao_malha_fechada as m; m.run()

def pagina_lgr():
    import modulos.realimentacao_lgr as m; m.run()

def pagina_estab():
    import modulos.estabilidade_realimentacao as m; m.run()

def pagina_bode():
    import modulos.resposta_frequencia as m; m.run()

def pagina_nyquist():
    import modulos.criterio_nyquist as m; m.run()

def pagina_ss():
    import modulos.espaco_de_estados as m; m.run()

# ── Definição das páginas com url_path explícito ──────────────────────────────
PG_HOME   = st.Page(pagina_inicial, title="Página Inicial",              icon="📘", default=True, url_path="home")
PG_SINAIS = st.Page(pagina_sinais,  title="Sinais e Sistemas Lineares",  icon="📡", url_path="sinais")
PG_LAP    = st.Page(pagina_laplace, title="Transformada de Laplace",     icon="🌀", url_path="laplace")
PG_ORD1   = st.Page(pagina_ord1,    title="Sistemas de Ordem 1",         icon="📈", url_path="ordem1")
PG_ORD2   = st.Page(pagina_ord2,    title="Sistemas de Ordem 2",         icon="📊", url_path="ordem2")
PG_MF     = st.Page(pagina_mf,      title="Malha Fechada — Ordem 1 e 2", icon="🔄", url_path="malha-fechada")
PG_LGR    = st.Page(pagina_lgr,     title="Perturbação e LGR",           icon="📍", url_path="lgr")
PG_ESTAB  = st.Page(pagina_estab,   title="Critério de Routh-Hurwitz",   icon="⚖️", url_path="estabilidade")
PG_BODE   = st.Page(pagina_bode,    title="Diagramas de Bode",           icon="📉", url_path="bode")
PG_NYQ    = st.Page(pagina_nyquist, title="Critério de Nyquist",         icon="🔁", url_path="nyquist")
PG_SS     = st.Page(pagina_ss,      title="Análise no Espaço de Estados", icon="🧮", url_path="estados")

# ── Navegação ─────────────────────────────────────────────────────────────────
_nav = st.navigation(
    {
        "🏠 Início": [PG_HOME],
        "📡 Sinais e Sistemas": [PG_SINAIS],
        "🌀 Transformada de Laplace": [PG_LAP],
        "📈 Dinâmica no Tempo": [PG_ORD1, PG_ORD2],
        "🔄 Análise com Realimentação": [PG_MF, PG_LGR],
        "⚖️ Estabilidade": [PG_ESTAB],
        "📉 Resposta em Frequência": [PG_BODE, PG_NYQ],
        "🧮 Espaço de Estados": [PG_SS],
    },
    position="sidebar",
    expanded=True,
)

# ═══════════════════════════════════════════════════════════════════════════════
# CONTEÚDO DA PÁGINA INICIAL
# ═══════════════════════════════════════════════════════════════════════════════
def _home():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────────
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
    🎓 IFRN — CNAT &nbsp;·&nbsp; 🏛️ Engenharia de Energia &nbsp;·&nbsp;
    👤 Marcus V A Fernandes &nbsp;·&nbsp;
    ✉️ marcus.fernandes@ifrn.edu.br &nbsp;·&nbsp; v1.0 · 2026
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

    # ── Sobre ─────────────────────────────────────────────────────────────────
    st.markdown("### 📖 Sobre este RED")
    st.markdown("""
Este **Recurso Educacional Digital** cobre a disciplina *Modelagem e Sistemas Lineares*
do curso de Engenharia de Energia do IFRN-CNAT, com módulos progressivos — de fundamentos
de sinais até representação em espaço de estados — com ênfase em compreensão visual e
exploração paramétrica. Cada módulo combina **teoria** com equações e exemplos analíticos,
**figuras** geradas numericamente e **exploradores interativos** com controles deslizantes
e campos de entrada para observar o efeito de parâmetros em tempo real,
sem necessidade de reexecução.
""")

    # ── Índice ────────────────────────────────────────────────────────────────
    with st.expander("📋 Índice geral com acesso direto", expanded=False):
        st.markdown("##### Clique em qualquer link para ir diretamente ao conteúdo.")
        st.markdown("---")

        # Módulo 1
        st.markdown("**1 · Sinais e Sistemas Lineares**")
        st.page_link(PG_SINAIS, label="↗ Sinais e Sistemas Lineares — LCIT, convolução, diagramas de blocos, superposição", icon="📡")
        st.markdown("---")

        # Módulo 2
        st.markdown("**2 · Transformada de Laplace**")
        st.page_link(PG_LAP, label="↗ Transformada de Laplace — pares, propriedades, FT, realizações, frações parciais, linearização", icon="🌀")
        st.markdown("---")

        # Módulo 3
        st.markdown("**3 · Dinâmica no Domínio do Tempo**")
        st.page_link(PG_ORD1, label="↗ 3.1 Sistemas de Ordem 1 — degrau, polo/zero, fase mínima, integrador", icon="📈")
        st.page_link(PG_ORD2, label="↗ 3.2 Sistemas de Ordem 2 — ξ, ωn, UP%, polos complexos, zeros adicionais", icon="📊")
        st.markdown("---")

        # Módulo 4
        st.markdown("**4 · Análise de Sistemas com Realimentação**")
        st.page_link(PG_MF,  label="↗ 4.1 Malha Fechada — HMF(s), tipo do sistema, Kp/Kv/Ka, erro em regime permanente", icon="🔄")
        st.page_link(PG_LGR, label="↗ 4.2 Perturbação e LGR — ganho crítico, rejeição de perturbação, quadro 4×4", icon="📍")
        st.markdown("---")

        # Módulo 5
        st.markdown("**5 · Estabilidade de Sistemas com Realimentação**")
        st.page_link(PG_ESTAB, label="↗ Critério de Routh-Hurwitz — tabela, casos especiais, região de estabilidade", icon="⚖️")
        st.markdown("---")

        # Módulo 6
        st.markdown("**6 · Resposta em Frequência de Sistemas**")
        st.page_link(PG_BODE, label="↗ 6.1 Diagramas de Bode — fatores elementares, margens φm/Gm, Nichols, filtros Butterworth", icon="📉")
        st.page_link(PG_NYQ,  label="↗ 6.2 Critério de Nyquist — N=Z−P, desvio em polos, comparação Nyquist×Bode×LGR", icon="🔁")
        st.markdown("---")

        # Módulo 7
        st.markdown("**7 · Análise de Sistemas no Espaço de Estados**")
        st.page_link(PG_SS, label="↗ Espaço de Estados — ẋ=Ax+Bu, realizações, e^{At}, controlabilidade, observabilidade", icon="🧮")

    # ── Cards de módulos ──────────────────────────────────────────────────────
    st.markdown("### 🗂️ Módulos do curso")
    st.caption("Clique em qualquer card para acessar o módulo diretamente.")

    # (num, icon, title, subtitle, desc, tags, page_obj)
    CARDS = [
        ("MOD 01","📡","Sinais e Sistemas Lineares","",
         "Fundamentos LTI: superposição, causalidade, estabilidade BIBO, "
         "convolução e diagramas de blocos em série, paralelo e realimentação.",
         ["LCIT","Convolução","Diagramas de blocos","Superposição"], PG_SINAIS),

        ("MOD 02","🌀","Transformada de Laplace","",
         "Tabela de pares, propriedades, frações parciais e função de transferência. "
         "Realizações de sistemas e linearização por série de Taylor.",
         ["Laplace","Frações parciais","Linearização","FT"], PG_LAP),

        ("MOD 03","📈","Dinâmica no Domínio do Tempo","Sistemas de Ordem 1",
         "Resposta ao degrau: y(∞), τ, Tr, Ts. Polo/zero, fase mínima e não-mínima. "
         "Exemplos: RL, RC, massa-amortecedor, inércia, térmico, hidráulico.",
         ["Ordem 1","Degrau","Polo/Zero","Fase mínima"], PG_ORD1),

        ("MOD 03","📊","Dinâmica no Domínio do Tempo","Sistemas de Ordem 2",
         "Coeficiente ξ e frequência ωₙ. Especificações UP%, Tp, Tr, Ts. "
         "Polos e zeros adicionais com toggles ON/OFF. Sistema oscilatório.",
         ["Ordem 2","Amortecimento","UP%","Polos complexos"], PG_ORD2),

        ("MOD 04","🔄","Análise com Realimentação","Malha Fechada — Ordem 1 e 2",
         "HMF(s) = G/(1+G). Tipo do sistema e constantes Kp, Kv, Ka. "
         "Efeito de k nos polos MF e compromisso erro × amortecimento.",
         ["Malha fechada","Erro","Tipo do sistema","Polos MF"], PG_MF),

        ("MOD 04","📍","Análise com Realimentação","Perturbação e LGR",
         "Plantas de ordem superior, rejeição de perturbação e ganho crítico. "
         "LGR com quadro 4×4 de 16 sistemas e explorador N(s)/D(s).",
         ["LGR","Perturbação","Ordem superior","k_crit"], PG_LGR),

        ("MOD 05","⚖️","Estabilidade com Realimentação","Routh-Hurwitz",
         "Critério de Routh-Hurwitz com casos especiais (ε e polinômio auxiliar). "
         "4 exemplos numéricos e região de estabilidade no plano (k, a₂).",
         ["Routh-Hurwitz","k_crit","Região de estabilidade","Marginal"], PG_ESTAB),

        ("MOD 06","📉","Resposta em Frequência","Diagramas de Bode",
         "6 fatores elementares, margens φm e Gm, banda passante, pico de ressonância. "
         "Diagrama de Nichols e filtros Butterworth (PB, PA, PF, RF).",
         ["Bode","Margens","Nichols","Filtros"], PG_BODE),

        ("MOD 06","🔁","Resposta em Frequência","Critério de Nyquist",
         "Princípio do Argumento N = Z−P, contorno de Nyquist, desvio em polos. "
         "Comparação sincronizada Nyquist × Bode × LGR com marcos de fase.",
         ["Nyquist","N=Z−P","Margens","Mapeamento"], PG_NYQ),

        ("MOD 07","🧮","Espaço de Estados","",
         "Equações ẋ=Ax+Bu. Realizações CCF/OCF, matriz e^{At} via Cayley-Hamilton. "
         "Controlabilidade Wc, observabilidade Wo e conversores FT↔SS.",
         ["Estado","Controlabilidade","Observabilidade","e^{At}"], PG_SS),
    ]

    for row_start in range(0, len(CARDS), 3):
        cols = st.columns(3, gap="medium")
        for ci, card in enumerate(CARDS[row_start:row_start+3]):
            num, icon, title, sub, desc, tags, page_obj = card
            tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
            sub_html  = f'<div class="mod-sub">↳ {sub}</div>' if sub else ""
            with cols[ci]:
                # Visual do card
                st.markdown(f"""
<div class="mod-card">
  <div class="mod-num">{num}</div>
  <span class="mod-icon">{icon}</span>
  <div class="mod-title">{title}</div>
  {sub_html}
  <div class="mod-desc">{desc}</div>
  <div style="margin-top:.4rem">{tags_html}</div>
</div>""", unsafe_allow_html=True)
                # Link clicável nativo do Streamlit logo abaixo do card
                st.page_link(page_obj, label=f"Abrir {title}" + (f" — {sub}" if sub else ""),
                             use_container_width=True)

    # ── Exploradores ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🎛️ Exploradores interativos")
    st.markdown(
        "Os **exploradores** são o diferencial deste RED — controles deslizantes, "
        "menus de seleção e campos de entrada com atualização em tempo real, "
        "sem necessidade de reexecução."
    )

    # (label, page_obj)
    EXP_GROUPS = [
        ("📡 Sinais e Sistemas", PG_SINAIS, [
            "Operações com sinais — deslocamento, escala, inversão",
        ]),
        ("🌀 Transformada de Laplace", PG_LAP, [
            "Linearização por Taylor — ordem 1 a 5",
        ]),
        ("📈 Dinâmica — Ordem 1", PG_ORD1, [
            "Resposta ao degrau — k, a, kr",
            "Plano s + degrau — k e a",
            "Sistema com zero — k, a, b",
            "Sistema instável — velocidade de divergência",
            "Polo MA vs. MF — integrador com realimentação",
        ]),
        ("📊 Dinâmica — Ordem 2", PG_ORD2, [
            "Regimes de amortecimento — ξ, ωn",
            "Plano s + especificações — ξ, ωn",
            "Efeito de ξ, ωn e k",
            "Parâmetros σ e ωd — polos complexos diretos",
            "Polo e zero adicionais — toggles ON/OFF",
            "Sistema oscilatório — k → ωn = √k",
        ]),
        ("🔄 Realimentação — MF", PG_MF, [
            "Tipo do sistema, entrada e ganho k",
            "Planta 1ª ordem — entrada, k e atraso",
            "Planta 2ª ordem — entrada, k e atraso",
        ]),
        ("📍 Realimentação — LGR", PG_LGR, [
            "Estabilidade de ordem superior — k e atraso",
            "Seguimento vs. rejeição de perturbação",
            "LGR interativo — N(s)/D(s) e k_max livre",
        ]),
        ("⚖️ Estabilidade", PG_ESTAB, [
            "Polos MF em função de k — 🟢/🟡/🔴",
            "Região de estabilidade — plano (k, a₂)",
        ]),
        ("📉 Bode", PG_BODE, [
            "6 fatores elementares — tabs com slider",
            "Margens φm e Gm — insira N(s)/D(s)",
            "Bode 1ª ordem — k e a",
            "Bode 2ª ordem — k, ξ, ωn",
            "Nichols — ξ múltiplos com multiselect",
            "Filtros Butterworth — tipo e ordem (1–10)",
            "Explorador geral — ωc, φm, Gm automáticos",
        ]),
        ("🔁 Nyquist", PG_NYQ, [
            "Efeito do ganho K — curva 🟢/🟡/🔴",
            "Nyquist × Bode × LGR — marcos sincronizados",
            "Explorador Nyquist — P, N, Z, φm, Gm",
        ]),
        ("🧮 Espaço de Estados", PG_SS, [
            "Explorador SS — insira A, B, C, D",
            "Conversor FT → SS",
            "Conversor SS → FT",
        ]),
    ]

    half = (len(EXP_GROUPS) + 1) // 2
    col_l, col_r = st.columns(2)
    for col, grupo in zip([col_l, col_r], [EXP_GROUPS[:half], EXP_GROUPS[half:]]):
        with col:
            for gtitle, page_obj, items in grupo:
                st.markdown(f'<p class="exp-group-title">{gtitle}</p>',
                            unsafe_allow_html=True)
                for item in items:
                    st.page_link(page_obj, label=item, use_container_width=False)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="page-footer">
  Modelagem e Sistemas Lineares &nbsp;·&nbsp;
  Engenharia de Energia &nbsp;·&nbsp; CNAT — IFRN<br>
  Autor: Marcus V A Fernandes &nbsp;·&nbsp;
  marcus.fernandes@ifrn.edu.br &nbsp;·&nbsp; v1.0 · 2026
</div>
""", unsafe_allow_html=True)


# ── Executa ───────────────────────────────────────────────────────────────────
_nav.run()
