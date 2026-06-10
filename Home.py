"""
RED — Modelagem e Sistemas Lineares
Home / Página Principal
"""

import streamlit as st

st.set_page_config(
    page_title="RED — Modelagem e Sistemas Lineares",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# CSS global
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── tipografia ── */
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem; font-weight: 800;
    line-height: 1.15; margin: 0 0 0.5rem;
}
.hero-sub { font-size: 1.05rem; opacity: 0.72; max-width: 640px; margin-bottom: 0.6rem; }
.meta-line { font-size: 0.83rem; opacity: 0.55; margin-top: 0.5rem; }

/* ── stats ── */
.stat-row {
    display: flex; gap: 2.5rem;
    margin: 1.4rem 0 2rem;
    padding: 1rem 0;
    border-top: 1px solid rgba(128,128,128,0.15);
    border-bottom: 1px solid rgba(128,128,128,0.15);
}
.stat-item { text-align: center; }
.stat-num { font-size: 1.7rem; font-weight: 700; color: #3d8ef0; }
.stat-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.09em; opacity: 0.5; }

/* ── RED badge ── */
.red-badge {
    display: inline-block;
    background: linear-gradient(135deg,#3d8ef0 0%,#6c47ff 100%);
    color: #fff; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 3px 10px; border-radius: 20px; margin-right: 0.6rem;
    vertical-align: middle;
}

/* ── módulo cards clicáveis ── */
.mod-card {
    background: var(--background-color);
    border: 1.5px solid rgba(128,128,128,0.18);
    border-radius: 14px;
    padding: 1.15rem 1.25rem 1rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.18s, box-shadow 0.18s, transform 0.12s;
    height: 100%;
    cursor: pointer;
    text-decoration: none;
    display: block;
}
.mod-card:hover {
    border-color: #3d8ef0;
    box-shadow: 0 4px 18px rgba(61,142,240,0.14);
    transform: translateY(-2px);
    text-decoration: none;
}
.mod-num {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; opacity: 0.42; margin-bottom: 0.35rem;
}
.mod-icon { font-size: 1.45rem; margin-bottom: 0.25rem; display: block; }
.mod-title { font-size: 0.97rem; font-weight: 700; margin-bottom: 0.3rem; }
.mod-sub  { font-size: 0.78rem; opacity: 0.5; font-style: italic; margin-bottom: 0.35rem; }
.mod-desc { font-size: 0.8rem; opacity: 0.63; line-height: 1.55; margin-bottom: 0.65rem; }
.tag {
    display: inline-block; font-size: 0.68rem; padding: 2px 7px;
    border-radius: 4px; background: rgba(61,142,240,0.10);
    color: #3d8ef0; margin: 2px 2px 0 0; font-weight: 500;
}

/* ── exploradores grid ── */
.exp-grid { display: flex; flex-wrap: wrap; gap: 0.6rem; margin: 0.5rem 0 1rem; }
.exp-pill {
    display: inline-flex; align-items: center; gap: 0.35rem;
    background: rgba(108,71,255,0.08); border: 1px solid rgba(108,71,255,0.18);
    border-radius: 20px; padding: 5px 12px;
    font-size: 0.78rem; color: #6c47ff; font-weight: 500;
}
.exp-pill span.ep-icon { font-size: 0.9rem; }

/* ── footer ── */
.page-footer {
    margin-top: 3rem;
    padding: 1.2rem 0 0.5rem;
    border-top: 1px solid rgba(128,128,128,0.15);
    text-align: center;
    font-size: 0.8rem;
    opacity: 0.5;
    line-height: 1.8;
}

/* ── índice ── */
.idx-section { font-weight: 700; margin: 0.6rem 0 0.15rem; font-size: 0.95rem; }
.idx-sub { margin-left: 1rem; font-size: 0.87rem; margin-bottom: 0.1rem; }
.idx-item { margin-left: 2rem; font-size: 0.82rem; opacity: 0.75; margin-bottom: 0.05rem; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════════════════
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
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# STATS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="stat-row">
  <div class="stat-item">
    <div class="stat-num">7</div>
    <div class="stat-label">Módulos</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">10</div>
    <div class="stat-label">Submódulos</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">30+</div>
    <div class="stat-label">Exploradores</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">60+</div>
    <div class="stat-label">Figuras</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">100%</div>
    <div class="stat-label">Online</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SOBRE O RED
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 📖 Sobre este RED")
st.markdown("""
Este **Recurso Educacional Digital** cobre a disciplina *Modelagem e Sistemas Lineares*
do curso de Engenharia de Energia do IFRN-CNAT. O material é organizado em módulos
progressivos — de fundamentos de sinais até representação em espaço de estados — com
ênfase em **compreensão visual e exploração paramétrica**.

Cada módulo combina:
- **Teoria** com equações, tabelas e exemplos analíticos resolvidos
- **Figuras** geradas numericamente (Matplotlib + Plotly)
- **Exploradores interativos** com sliders e campos de entrada para observar
  o efeito de parâmetros em tempo real
""")


# ═══════════════════════════════════════════════════════════════════════════════
# ÍNDICE GERAL (expander clicável)
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("📋 Índice geral — clique para expandir", expanded=False):
    st.markdown("""
**1. [Sinais e Sistemas Lineares](01_Sinais_e_Sistemas_Lineares)**

&nbsp;&nbsp;· Definição de sinais e sistemas — LCIT  
&nbsp;&nbsp;· Operações com sinais: deslocamento, inversão, escalonamento  
&nbsp;&nbsp;· Propriedades: linearidade, invariância no tempo, causalidade, memória, estabilidade  
&nbsp;&nbsp;· Resposta ao impulso e convolução  
&nbsp;&nbsp;· Diagrama de blocos: série, paralelo, realimentação  
&nbsp;&nbsp;· Explorador interativo de operações com sinais

---

**2. [Transformada de Laplace](02_Transformada_de_Laplace)**

&nbsp;&nbsp;· Definição bilateral e unilateral — integral de Bromwich  
&nbsp;&nbsp;· Tabela de pares fundamentais  
&nbsp;&nbsp;· Propriedades: linearidade, deslocamento, escalamento, derivação, integração  
&nbsp;&nbsp;· Teoremas do valor inicial e final  
&nbsp;&nbsp;· Convolução no tempo ↔ multiplicação em s  
&nbsp;&nbsp;· Função de transferência — polos e zeros  
&nbsp;&nbsp;· Estabilidade via posição dos polos  
&nbsp;&nbsp;· Realização de sistemas: formas direta, cascata e paralela  
&nbsp;&nbsp;· Atraso de transporte — aproximação de Padé  
&nbsp;&nbsp;· Sistemas não-lineares e linearização (Taylor)  
&nbsp;&nbsp;· Frações parciais: raízes reais distintas, complexas e repetidas  
&nbsp;&nbsp;· Explorador de linearização por expansão de Taylor

---

**3. Dinâmica no Domínio do Tempo**

**3.1 [Sistemas de Ordem 1](03_Dinamica_Ordem_1)**

&nbsp;&nbsp;· Função de transferência 1ª ordem: grau relativo, ganho DC, constante de tempo  
&nbsp;&nbsp;· Resposta ao degrau: componentes forçada e natural  
&nbsp;&nbsp;· Especificações: y(∞), τ, Tr, Ts — identificação experimental  
&nbsp;&nbsp;· Exemplos físicos: RL, RC, massa-amortecedor, inércia, térmico, hidráulico  
&nbsp;&nbsp;· Efeito do zero: fase mínima, cancelamento polo-zero, fase não-mínima  
&nbsp;&nbsp;· Sistemas com polo no SPD (instável) e polo na origem (integrador)  
&nbsp;&nbsp;· 5 exploradores interativos: degrau, plano s, zero, instável, polo MA vs MF

**3.2 [Sistemas de Ordem 2](04_Dinamica_Ordem_2)**

&nbsp;&nbsp;· Forma canônica: ξ, ωn, k — polos complexos conjugados  
&nbsp;&nbsp;· Regimes: subamortecido, criticamente amortecido, sobreamortecido, oscilatório  
&nbsp;&nbsp;· Especificações: UP%, Tp, Tr, Ts — fórmulas analíticas  
&nbsp;&nbsp;· Efeito de σ e ωd — parametrização direta dos polos  
&nbsp;&nbsp;· Exemplos físicos: massa-mola-amortecedor, circuito RLC  
&nbsp;&nbsp;· Polos e zeros adicionais — influência na resposta transitória  
&nbsp;&nbsp;· Sistema oscilatório com polos no eixo imaginário  
&nbsp;&nbsp;· 6 exploradores interativos com toggles para polo e zero adicionais

**3.3 [Sistemas de Ordem Superior](05_Realimentacao_Malha_Fechada) ¹**

&nbsp;&nbsp;· Plantas de 3ª ordem — ganho crítico via Routh-Hurwitz  
&nbsp;&nbsp;· Polo dominante e aproximação de 2ª ordem  
&nbsp;&nbsp;· Efeito do ganho k na estabilidade e na resposta

---

**4. Análise de Sistemas com Realimentação**

**4.1 [Sistemas de Ordem 1 e 2 em Malha Fechada](05_Realimentacao_Malha_Fechada)**

&nbsp;&nbsp;· Estrutura de malha fechada — HMF(s) = G/(1+G)  
&nbsp;&nbsp;· Tipo do sistema (ν) e constantes de erro: Kp, Kv, Ka  
&nbsp;&nbsp;· Erro em regime permanente: degrau, rampa, parábola  
&nbsp;&nbsp;· Planta 1ª ordem: polo MF, τMF, erro ao degrau  
&nbsp;&nbsp;· Planta 2ª ordem: ωn_MF, ξMF — compromisso erro vs. amortecimento  
&nbsp;&nbsp;· 3 exploradores interativos com plano s, y(t) e e(t)

**4.2 [Ordem Superior, Perturbação e LGR](06_Realimentacao_LGR)**

&nbsp;&nbsp;· Plantas de ordem superior — estabilidade e ganho crítico  
&nbsp;&nbsp;· Perturbação D(s) na entrada da planta — seguimento vs. rejeição  
&nbsp;&nbsp;· Erro de perturbação: e_rp,D = −1/(a+k)  
&nbsp;&nbsp;· Lugar Geométrico das Raízes (LGR) — regras de construção  
&nbsp;&nbsp;· Quadro 4×4 de 16 sistemas — LGR completo com cache  
&nbsp;&nbsp;· LGR interativo: insira N(s)/D(s) e visualize automaticamente  
&nbsp;&nbsp;· 3 exploradores interativos: estabilidade, perturbação e LGR

---

**5. [Estabilidade de Sistemas com Realimentação](07_Estabilidade_Realimentacao)**

&nbsp;&nbsp;· Conceitos: equilíbrio estável, marginal e instável  
&nbsp;&nbsp;· Estabilidade BIBO vs. assintótica (Lyapunov)  
&nbsp;&nbsp;· Critério de Routh-Hurwitz — construção da tabela  
&nbsp;&nbsp;· Casos especiais: zero isolado (ε) e linha de zeros (polinômio auxiliar)  
&nbsp;&nbsp;· 4 exemplos numéricos com tabela de Routh interativa  
&nbsp;&nbsp;· Região de estabilidade no plano (k, a2)  
&nbsp;&nbsp;· 2 exploradores interativos: polos MF em função de k e diagrama de região

---

**6. Resposta em Frequência de Sistemas**

**6.1 [Diagramas de Bode](08_Resposta_Frequencia)**

&nbsp;&nbsp;· Resposta senoidal em regime permanente — |H(jω)| e ∠H(jω)  
&nbsp;&nbsp;· 6 fatores elementares com tabs interativos: s, 1/s, s+a, 1/(s+a), ...  
&nbsp;&nbsp;· Frequência de corte (-3 dB) e banda passante vs. ξ  
&nbsp;&nbsp;· Margem de fase φm e margem de ganho Gm  
&nbsp;&nbsp;· Bode de sistemas de 1ª e 2ª ordem — pico de ressonância  
&nbsp;&nbsp;· Diagrama de Nichols — ponto crítico (-180°, 0 dB)  
&nbsp;&nbsp;· Filtros Butterworth: passa-baixa, passa-alta, passa-faixa, rejeita-faixa  
&nbsp;&nbsp;· Explorador geral de Bode com diagnóstico automático de margens

**6.2 [Critério de Nyquist](09_Criterio_Nyquist)**

&nbsp;&nbsp;· Mapeamento de contornos — Princípio do Argumento: N = Z − P  
&nbsp;&nbsp;· Contorno de Nyquist no plano s — envolve todo o SPD  
&nbsp;&nbsp;· Critério Z = N + P = 0 para estabilidade  
&nbsp;&nbsp;· Desvio em polos sobre o eixo imaginário — convenção padrão e alternativa  
&nbsp;&nbsp;· Interpretação geométrica de φm e Gm no diagrama de Nyquist  
&nbsp;&nbsp;· Comparação sincronizada: Nyquist × Bode × LGR (marcos de fase)  
&nbsp;&nbsp;· Explorador interativo: diagnóstico automático P, N, Z, φm, Gm

---

**7. [Análise de Sistemas no Espaço de Estados](10_Espaco_de_Estados)**

&nbsp;&nbsp;· Descrição interna vs. externa — equivalência controlável/observável  
&nbsp;&nbsp;· Equações de estado: ẋ = Ax + Bu, y = Cx + Du  
&nbsp;&nbsp;· Realizações: CCF, OCF, cascata, paralela (frações parciais)  
&nbsp;&nbsp;· Solução via Laplace: componentes entrada nula e estado nulo  
&nbsp;&nbsp;· Matriz de transição e^{At} — propriedades e Cayley-Hamilton  
&nbsp;&nbsp;· Transformação de similaridade e forma modal (diagonalização)  
&nbsp;&nbsp;· Controlabilidade W_c e observabilidade W_o — critério de Kalman  
&nbsp;&nbsp;· 3 exploradores: Explorador SS, Conversor FT→SS, Conversor SS→FT

---
> ¹ A seção de ordem superior está integrada ao módulo 4.1/4.2 na aplicação.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# MÓDULOS — CARDS CLICÁVEIS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🗂️ Módulos do curso")
st.caption("Clique em qualquer módulo para acessar diretamente o conteúdo.")

# Estrutura: (número, ícone, título, subtítulo, descrição, tags, url_page)
MODULES = [
    (
        "MOD 01", "📡",
        "Sinais e Sistemas Lineares", "",
        "Fundamentos de sinais e sistemas LTI: superposição, causalidade, estabilidade, "
        "convolução e diagramas de blocos com explorador interativo.",
        ["LCIT", "Convolução", "Diagramas de blocos", "Superposição"],
        "01_Sinais_e_Sistemas_Lineares",
    ),
    (
        "MOD 02", "🌀",
        "Transformada de Laplace", "",
        "Definição, tabela de pares, propriedades, frações parciais e função de transferência. "
        "Inclui linearização por Taylor e sistemas não-lineares.",
        ["Laplace", "Frações parciais", "Linearização", "FT"],
        "02_Transformada_de_Laplace",
    ),
    (
        "MOD 03", "📈",
        "Dinâmica no Domínio do Tempo", "Sistemas de Ordem 1",
        "Resposta ao degrau, polo/zero, grau relativo e sistemas instáveis. "
        "Exemplos físicos: RL, RC, massa-amortecedor, inércia, térmico e hidráulico.",
        ["Ordem 1", "Degrau", "Polo/Zero", "Fase mínima"],
        "03_Dinamica_Ordem_1",
    ),
    (
        "MOD 03", "📊",
        "Dinâmica no Domínio do Tempo", "Sistemas de Ordem 2",
        "Amortecimento ξ e frequência natural ωₙ. Especificações UP%, Tp, Tr, Ts. "
        "Polos e zeros adicionais, sistema oscilatório e forma modal.",
        ["Ordem 2", "Amortecimento", "UP%", "Polos complexos"],
        "04_Dinamica_Ordem_2",
    ),
    (
        "MOD 04", "🔄",
        "Análise com Realimentação", "Ordem 1 e 2 em Malha Fechada",
        "Estrutura HMF(s), tipo do sistema, constantes de erro Kp/Kv/Ka. "
        "Efeito do ganho k nos polos MF e compromisso erro vs. amortecimento.",
        ["Malha fechada", "Erro estacionário", "Tipo do sistema", "Polos MF"],
        "05_Realimentacao_Malha_Fechada",
    ),
    (
        "MOD 04", "📍",
        "Análise com Realimentação", "Perturbação e LGR",
        "Plantas de ordem superior, ganho crítico, rejeição de perturbação. "
        "LGR completo com quadro 4×4 e explorador interativo N(s)/D(s).",
        ["LGR", "Perturbação", "Ordem superior", "Ganho crítico"],
        "06_Realimentacao_LGR",
    ),
    (
        "MOD 05", "⚖️",
        "Estabilidade com Realimentação", "Routh-Hurwitz e Região de Estabilidade",
        "Critério de Routh-Hurwitz, casos especiais (ε e polinômio auxiliar). "
        "4 exemplos numéricos e diagrama de região de estabilidade no plano (k, a₂).",
        ["Routh-Hurwitz", "Ganho crítico", "Região de estabilidade", "Marginal"],
        "07_Estabilidade_Realimentacao",
    ),
    (
        "MOD 06", "📉",
        "Resposta em Frequência", "Diagramas de Bode",
        "Fatores elementares (6 tabs), margens φm e Gm, banda passante, Nichols, "
        "filtros Butterworth e explorador geral de Bode com diagnóstico automático.",
        ["Bode", "Margens", "Nichols", "Filtros Butterworth"],
        "08_Resposta_Frequencia",
    ),
    (
        "MOD 06", "🔁",
        "Resposta em Frequência", "Critério de Nyquist",
        "Princípio do Argumento, contorno de Nyquist, Z = N + P, desvio em polos. "
        "Comparação sincronizada Nyquist × Bode × LGR com diagnóstico P/N/Z/φm/Gm.",
        ["Nyquist", "Princípio do Argumento", "Margens", "Mapeamento"],
        "09_Criterio_Nyquist",
    ),
    (
        "MOD 07", "🧮",
        "Análise no Espaço de Estados", "",
        "Equações de estado, realizações (CCF, OCF, paralela, cascata), matriz e^{At}, "
        "controlabilidade e observabilidade. Conversores FT↔SS e explorador completo.",
        ["Estado", "Controlabilidade", "Observabilidade", "e^{At}"],
        "10_Espaco_de_Estados",
    ),
]

cols_per_row = 3
for row_start in range(0, len(MODULES), cols_per_row):
    cols = st.columns(cols_per_row, gap="medium")
    for col_idx, mod in enumerate(MODULES[row_start:row_start + cols_per_row]):
        num, icon, title, subtitle, desc, tags, url = mod
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
        sub_html = f'<div class="mod-sub">↳ {subtitle}</div>' if subtitle else ""
        with cols[col_idx]:
            st.markdown(f"""
<a class="mod-card" href="{url}" target="_self">
  <div class="mod-num">{num}</div>
  <span class="mod-icon">{icon}</span>
  <div class="mod-title">{title}</div>
  {sub_html}
  <div class="mod-desc">{desc}</div>
  <div>{tags_html}</div>
</a>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPLORADORES — DESTAQUE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("### 🎛️ Exploradores interativos")
st.markdown(
    "Os **exploradores** são o diferencial deste RED — sliders, selectboxes e campos "
    "de entrada em tempo real, sem necessidade de reexecução."
)

EXPLORERS = [
    ("📡", "Operações com sinais", "Sinais e Sistemas"),
    ("🌀", "Linearização de Taylor (ordem 1–5)", "Transformada de Laplace"),
    ("📈", "Resposta ao degrau 1ª ordem — k, a, kr", "Dinâmica 1"),
    ("📈", "Plano s + degrau 1ª ordem — k, a", "Dinâmica 1"),
    ("📈", "Sistema com zero — k, a, b", "Dinâmica 1"),
    ("📈", "Sistema instável — velocidade de divergência", "Dinâmica 1"),
    ("📈", "Polo MA vs. MF — integrador", "Dinâmica 1"),
    ("📊", "Regimes de amortecimento — ξ, ωn", "Dinâmica 2"),
    ("📊", "Plano s + especificações — ξ, ωn", "Dinâmica 2"),
    ("📊", "Efeito de ξ, ωn e k na resposta", "Dinâmica 2"),
    ("📊", "Parâmetros σ e ωd — polos complexos", "Dinâmica 2"),
    ("📊", "Polo e zero adicionais (toggles ON/OFF)", "Dinâmica 2"),
    ("📊", "Sistema oscilatório — slider k", "Dinâmica 2"),
    ("🔄", "Tipo do sistema, entrada e ganho k", "Realimentação MF"),
    ("🔄", "Planta 1ª ordem: entrada, k e atraso", "Realimentação MF"),
    ("🔄", "Planta 2ª ordem: entrada, k e atraso", "Realimentação MF"),
    ("📍", "Estabilidade por ordem superior — k e atraso", "Realimentação LGR"),
    ("📍", "Seguimento e rejeição de perturbação", "Realimentação LGR"),
    ("📍", "LGR interativo — N(s)/D(s) e k_max", "Realimentação LGR"),
    ("⚖️", "Polos MF em função do ganho k (🟢/🟡/🔴)", "Estabilidade"),
    ("⚖️", "Região de estabilidade no plano (k, a₂)", "Estabilidade"),
    ("📉", "6 fatores elementares de Bode (tabs)", "Bode"),
    ("📉", "Margens φm e Gm — N(s)/D(s)", "Bode"),
    ("📉", "Bode 1ª ordem — k e a", "Bode"),
    ("📉", "Bode 2ª ordem — k, ξ, ωn", "Bode"),
    ("📉", "Nichols — ξ múltiplos (multiselect)", "Bode"),
    ("📉", "Filtros Butterworth — tipo e ordem", "Bode"),
    ("📉", "Explorador geral de Bode", "Bode"),
    ("🔁", "Efeito do ganho K no diagrama de Nyquist", "Nyquist"),
    ("🔁", "Comparação sincronizada Nyquist × Bode × LGR", "Nyquist"),
    ("🔁", "Explorador Nyquist — P, N, Z, φm, Gm", "Nyquist"),
    ("🧮", "Explorador SS — A, B, C, D", "Espaço de Estados"),
    ("🧮", "Conversor FT → SS", "Espaço de Estados"),
    ("🧮", "Conversor SS → FT", "Espaço de Estados"),
]

# Agrupar por módulo
from collections import defaultdict
grouped = defaultdict(list)
for icon, name, mod in EXPLORERS:
    grouped[mod].append((icon, name))

cols_exp = st.columns(2)
mod_list = list(grouped.keys())
mid = (len(mod_list) + 1) // 2
for col, mods in zip(cols_exp, [mod_list[:mid], mod_list[mid:]]):
    with col:
        for mod in mods:
            items = grouped[mod]
            pills = "".join(
                f'<span class="exp-pill"><span class="ep-icon">{ic}</span>{nm}</span>'
                for ic, nm in items)
            st.markdown(f"""
<p style="font-size:0.82rem;font-weight:700;margin:0.9rem 0 0.3rem;opacity:0.65;">
  {mod}
</p>
<div class="exp-grid">{pills}</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-footer">
  Modelagem e Sistemas Lineares &nbsp;·&nbsp; Engenharia de Energia &nbsp;·&nbsp; CNAT — IFRN<br>
  Autor: Marcus V A Fernandes &nbsp;·&nbsp; marcus.fernandes@ifrn.edu.br &nbsp;·&nbsp; v1.0 · 2026
</div>
""", unsafe_allow_html=True)
