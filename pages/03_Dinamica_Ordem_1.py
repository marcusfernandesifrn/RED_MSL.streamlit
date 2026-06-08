"""
Dinâmica no Domínio do Tempo — Sistemas de Ordem 1
Disciplina: Modelagem e Sistemas Lineares
Curso: Engenharia de Energia
Instituição: IFRN — Campus Natal-Central (CNAT)
Autor: Marcus V A Fernandes · marcus.fernandes@ifrn.edu.br · v1.1
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.signal import lti, step as sc_step
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Configuração da Página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dinâmica — Sistemas de Ordem 1",
    page_icon="📈",
    layout="wide",
)

# ── Estilo global de figuras ──────────────────────────────────────────────────
plt.rcParams.update({
    "figure.dpi": 120,
    "axes.grid": True,
    "axes.titlesize": 9,
    "axes.labelsize": 8,
    "lines.linewidth": 1.6,
    "font.family": "serif",
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "grid.alpha": 0.3,
})

# ── Paleta de cores ───────────────────────────────────────────────────────────
COR = dict(
    sinal    = "royalblue",
    ref      = "steelblue",
    saida    = "crimson",
    natural  = "seagreen",
    instavel = "crimson",
    marginal = "darkorange",
    degrau   = "royalblue",
    bloco_f  = "#FFFFFF",
    bloco_e  = "#000000",
)

# ── Helpers de plotagem ───────────────────────────────────────────────────────
def estilo(ax, xlabel="t", ylabel="Amplitude"):
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.spines[["right", "top"]].set_visible(False)

def bloco(ax, x, y, w, h, txt, fc=None, ec=None, fs=8):
    fc = fc or COR["bloco_f"]; ec = ec or COR["bloco_e"]
    ax.add_patch(mpatches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.04", facecolor=fc, edgecolor=ec, lw=1.4, zorder=3))
    ax.text(x, y, txt, ha="center", va="center", fontsize=fs, zorder=4)

def seta(ax, x1, y1, x2, y2, lb="", ldy=0.09):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=COR["bloco_e"],
                        lw=1.4, shrinkA=0, shrinkB=0), zorder=2)
    if lb:
        ax.text((x1+x2)/2, (y1+y2)/2+ldy, lb, ha="center", fontsize=7.5)

# ── Funções de resposta ───────────────────────────────────────────────────────
def step_response(k_v, a_v, t_arr):
    """Resposta ao degrau de H(s)=k/(s+a): y(t)=(k/a)*(1-exp(-a*t))"""
    return (k_v / a_v) * (1.0 - np.exp(-a_v * t_arr))

def step_response_zero(k_v, a_v, b_v, t_arr):
    """Resposta ao degrau de H(s)=k*(s+b)/(s+a)"""
    sys_h = lti([k_v, k_v * b_v], [1, a_v])
    _, y = sc_step(sys_h, T=t_arr)
    return y

# ── CSS responsivo + show_fig ─────────────────────────────────────────────────
st.markdown("""
<style>
.fig-wrap {
    display: flex;
    justify-content: center;
    width: 100%;
}
.fig-wrap > div { width: 100%; }
@media (min-width: 769px) {
    .fig-wrap > div {
        width: var(--fw, 65%);
        max-width: var(--fw, 65%);
    }
}
.fig-wrap img,
.fig-wrap [data-testid="stImage"] img {
    width: 100% !important;
    height: auto !important;
}
</style>
""", unsafe_allow_html=True)

def show_fig(fig, width_frac=0.65):
    import io, base64
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=fig.get_dpi())
    plt.close(fig)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    pct = f"{int(width_frac * 100)}%"
    st.markdown(
        f'<div class="fig-wrap">'
        f'<div style="--fw:{pct}">'
        f'<img src="data:image/png;base64,{b64}" style="width:100%;height:auto;display:block;"/>'
        f'</div></div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CABEÇALHO
# ═══════════════════════════════════════════════════════════════════════════════
st.title("📈 Dinâmica no Domínio do Tempo — Sistemas de Ordem 1")
st.caption("Modelagem e Sistemas Lineares · Engenharia de Energia · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

# ── Índice ────────────────────────────────────────────────────────────────────
with st.expander("📋 Índice — clique para expandir", expanded=False):
    st.markdown(r"""
**[1. Função de Transferência de 1ª Ordem](#1-fun-o-de-transfer-ncia-de-1-ordem)**
- 1.1 Grau relativo $n^* = n - m$
- 1.2 Formas canônicas: ganho estático $k'=k/a$ e constante de tempo $\tau=1/a$
- 1.3 Diagrama de blocos e localização do polo no plano $s$

**[2. Resposta ao Degrau — Componentes e Especificações](#2-resposta-ao-degrau-componentes-e-especifica-es)**
- 2.1 Dedução analítica: componentes forçada $y_f$ e natural $y_n$
- 2.2 Especificações: $y(\infty)$, $\tau$, $T_r$, $T_{s_{2\%}}$
- 2.3 Identificação experimental dos parâmetros $a$ e $k$
- 🎛️ Explorador interativo: sliders $k$, $a$, $k_r$

**[3. Sistemas de Grau Relativo 1 — Exemplos e Efeito dos Parâmetros](#3-sistemas-de-grau-relativo-1-exemplos-e-efeito-dos-par-metros)**
- 3.1 Exemplos físicos: circuito RL, RC, massa-amortecedor, inércia-amortecedor, térmico, hidráulico
- 3.2 Efeito de $k$ (ganho estático) e de $a$ (velocidade) na resposta
- 3.3 🎛️ Explorador interativo: plano $s$ + resposta ao degrau

**[4. Sistemas de Grau Relativo 0 — Efeito do Zero](#4-sistemas-de-grau-relativo-0-efeito-do-zero)**
- 4.1 Função de transferência com zero finito: $H'(s) = k(s+b)/(s+a)$
- 4.2 Resposta ao degrau e valores notáveis $y'(0^+) = k$, $y'(\infty) = kb/a$
- 4.3 Classificação: fase mínima ($b>0$), cancelamento polo-zero ($b=a$), fase não-mínima ($b<0$)
- 🎛️ Explorador interativo: sliders $k$, $a$, $b$

**[5. Polo no Semiplano Direito — Sistema Instável](#5-polo-no-semiplano-direito-sistema-inst-vel)**
- 5.1 Resposta ao degrau: $y(t) = (k/a)(e^{+at}-1)$
- 5.2 Efeito de zero adicional sobre a velocidade de divergência
- 🎛️ Explorador interativo: slider $a$ (velocidade de divergência)

**[6. Polo na Origem — Sistema Marginalmente Estável](#6-polo-na-origem-sistema-marginalmente-est-vel)**
- 6.1 Integrador puro (malha aberta): saída rampa $y(t) = kt$
- 6.2 Estabilização por realimentação negativa: polo migra de $s=0$ para $s=-k$
- 6.3 🎛️ Explorador interativo: slider $k$ — polo MA vs. polo MF

**[7. Referências](#7-refer-ncias)**
""")

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 1 — FUNÇÃO DE TRANSFERÊNCIA DE 1ª ORDEM
# ═══════════════════════════════════════════════════════════════════════════════
st.header("1. Função de Transferência de 1ª Ordem")

st.markdown(r"""
### 1.1 Grau relativo

O **grau relativo** $n^*$ de uma função de transferência $H(s)$ é a diferença entre o
grau do denominador (número de polos, $n$) e o grau do numerador (número de zeros, $m$):

$$n^* = n - m$$

Para sistemas causais e próprios, $n^* \geq 0$.

### 1.2 Formas canônicas

Para sistemas de 1ª ordem ($n=1$, $n^*=1$), o único polo está em $s = -a$ e a função de
transferência admite três representações equivalentes:

$$H(s) = \frac{Y(s)}{X(s)} = \frac{k}{s+a} = \frac{k/a}{\dfrac{s}{a} + 1} = \frac{k'}{\tau s + 1}$$

onde $k' = k/a$ é o **ganho estático** (DC) e $\tau = 1/a$ é a **constante de tempo**.

### 1.3 Diagrama de blocos e plano $s$

O polo ocupa a posição $s = -a$ no plano complexo.

> Para $a > 0$: polo no **semiplano esquerdo** → sistema **estável** ($y(t) \to$ constante).
> Para $a < 0$: polo no **semiplano direito** → sistema **instável** ($y(t) \to \infty$).
""")

fig1, axes1 = plt.subplots(1, 2, figsize=(8.0, 2.4))

ax = axes1[0]
ax.set_xlim(0, 5); ax.set_ylim(-0.6, 0.6); ax.axis("off")
seta(ax, 0.2, 0, 1.2, 0, "X(s)")
bloco(ax, 2.5, 0, 2.3, 0.5, r"$H(s) = \dfrac{k}{s+a}$", fs=9)
seta(ax, 3.65, 0, 4.8, 0, "Y(s)")
ax.set_title("Diagrama de blocos — sistema de 1ª ordem", fontsize=8.5)

ax2 = axes1[1]
ax2.set_xlim(-3, 1.5); ax2.set_ylim(-1.5, 1.5)
ax2.axhline(0, color="k", lw=0.8); ax2.axvline(0, color="k", lw=0.8)
ax2.fill_betweenx([-1.5, 1.5], -3,   0,   alpha=0.07, color="seagreen", label="Estável (esq.)")
ax2.fill_betweenx([-1.5, 1.5],  0, 1.5,   alpha=0.07, color="crimson",  label="Instável (dir.)")
ax2.plot(-1, 0, "x", color=COR["saida"], ms=12, mew=2.5, label=r"polo $s=-a$")
ax2.text(-1, 0.22, r"$-a$", ha="center", fontsize=9, color=COR["saida"])
ax2.set_xlabel(r"$\sigma$", fontsize=8); ax2.set_ylabel(r"$j\omega$", fontsize=8)
ax2.set_title(r"Plano $s$ — localização do polo", fontsize=8.5)
ax2.legend(fontsize=7, loc="upper right")
ax2.spines[["right", "top"]].set_visible(False)
plt.tight_layout()
show_fig(fig1, 0.72)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 2 — RESPOSTA AO DEGRAU
# ═══════════════════════════════════════════════════════════════════════════════
st.header("2. Resposta ao Degrau — Componentes e Especificações")

st.markdown(r"""
### 2.1 Dedução analítica

Para entrada degrau de amplitude $k_r$, ou seja $X(s) = k_r/s$, a saída em Laplace é:

$$Y(s) = H(s)\cdot\frac{k_r}{s} = \frac{k\,k_r}{s\,(s+a)}$$

Expandindo em frações parciais e invertendo:

$$\boxed{y(t) = y_f(t) + y_n(t) = \frac{k\,k_r}{a}\bigl(1 - e^{-at}\bigr), \quad t \geq 0}$$

| Componente | Expressão | Nome alternativo |
|---|---|---|
| $y_f(t) = k\,k_r/a$ | Resposta **forçada** | Componente de estado nulo (*zero-state*) |
| $y_n(t) = -(k\,k_r/a)\,e^{-at}$ | Resposta **natural** | Componente de entrada nula (*zero-input*) |

> $y_f$ depende apenas da entrada (estado inicial zero); $y_n$ depende apenas do estado inicial.
> Para condição inicial nula, $y_n$ é determinada pelo transitório imposto pela própria entrada.

### 2.2 Especificações de desempenho

| Parâmetro | Símbolo | Fórmula |
|---|---|---|
| Valor inicial | $y(0^+)$ | $0$ |
| Valor final | $y(\infty)$ | $k\,k_r/a$ |
| Constante de tempo | $\tau$ | $1/a$ |
| Tempo de subida | $T_r$ | $\approx 2{,}2/a$ |
| Tempo de acomodação 2% | $T_{s_{2\%}}$ | $\approx 4/a$ |

> **Características:** sem ultrapassagem (*overshoot*), inclinação inicial $\dot{y}(0^+) = k\,k_r > 0$.

### 2.3 Identificação experimental

Medida a curva $y(t)$ após um degrau $k_r$ conhecido:

$$a = \frac{4}{T_{s_{2\%}}} \approx \frac{2{,}2}{T_r}, \qquad k = \frac{a\cdot y(\infty)}{k_r}$$
""")

k_val2 = 1.4; a_val2 = 0.7; kr_val2 = 1.0
t_arr2 = np.linspace(0, 12, 600)
yinf2 = k_val2 * kr_val2 / a_val2
tau2   = 1.0 / a_val2
Tr2    = 2.2 / a_val2
Ts2_2  = 4.0 / a_val2
yf2    =  yinf2 * np.ones_like(t_arr2)
yn2    = -yinf2 * np.exp(-a_val2 * t_arr2)
y2     = yf2 + yn2

fig2, axes2 = plt.subplots(1, 2, figsize=(9.5, 3.4))

ax = axes2[0]
ax.plot(t_arr2, yf2, "--", color=COR["ref"],    lw=1.4, label=r"$y_f(t)=k\,k_r/a$ (forçada)")
ax.plot(t_arr2, yn2, ":",  color=COR["natural"], lw=1.6, label=r"$y_n(t)=-(k\,k_r/a)e^{-at}$ (natural)")
ax.plot(t_arr2, y2,        color=COR["degrau"],  lw=2.0, label=r"$y(t)=y_f+y_n$")
ax.axhline(yinf2, color="gray", lw=0.8, ls="--")
ax.axvline(tau2,  color="purple", lw=0.9, ls=":")
ax.annotate(r"$\tau=1/a$", xy=(tau2, 0.63*yinf2),
            xytext=(tau2+0.7, 0.48*yinf2), fontsize=8, color="purple",
            arrowprops=dict(arrowstyle="->", color="purple", lw=0.8))
ax.text(11.5, yinf2+0.04, r"$y(\infty)$", ha="right", fontsize=8, color="gray")
estilo(ax, xlabel="t (s)")
ax.set_title(rf"Componentes — $H(s)={k_val2}/(s+{a_val2})$, degrau $k_r={kr_val2}$", fontsize=8.5)
ax.legend(fontsize=7)

ax2 = axes2[1]
ax2.plot(t_arr2, y2, color=COR["degrau"], lw=2.0)
for frac, cor, lb in [(1.00, "gray", ""), (0.98, "brown", "98%"),
                      (0.90, "olive", "90%"), (0.63, "purple", "63%"), (0.10, "olive", "10%")]:
    ax2.axhline(frac*yinf2, color=cor, lw=0.7, ls="--")
    if lb: ax2.text(12.1, frac*yinf2, lb, va="center", fontsize=7, color=cor)
for xv, cor, lb in [(tau2, "purple", r"$\tau$"), (Tr2, "olive", r"$T_r$"), (Ts2_2, "brown", r"$T_s$")]:
    ax2.axvline(xv, color=cor, lw=0.9, ls=":")
    ax2.text(xv+0.1, -0.18, lb, fontsize=8, color=cor)
estilo(ax2, xlabel="t (s)")
ax2.set_title("Especificações de desempenho", fontsize=8.5)
ax2.set_xlim(0, 12)
plt.tight_layout()
show_fig(fig2, 0.88)

# ── Explorador interativo seção 2 ─────────────────────────────────────────────
st.markdown("### 🎛️ Explorador Interativo — Resposta ao Degrau")
st.caption("Cada slider altera **um parâmetro** mantendo os demais fixos. "
           "Slider **azul** = $k$ · **vermelho** = $a$ · **verde** = $k_r$")

t_s2 = np.linspace(0, 18, 700)
k_grid2  = np.round(np.arange(0.5, 5.1, 0.5), 2)
a_grid2  = np.round(np.arange(0.2, 3.0, 0.2), 2)
kr_grid2 = np.round(np.arange(0.5, 3.1, 0.5), 2)
K2_DEF=2.0; A2_DEF=0.8; KR2_DEF=1.0
nk2=len(k_grid2); na2=len(a_grid2); nkr2=len(kr_grid2)
total2=nk2+na2+nkr2
traces2=[]

for kv in k_grid2:
    yinf=kv*KR2_DEF/A2_DEF; y=yinf*(1-np.exp(-A2_DEF*t_s2))
    traces2.append(go.Scatter(x=t_s2, y=y, mode="lines",
        line=dict(color="#1f77b4", width=2.2),
        visible=(abs(kv-K2_DEF)<1e-9), showlegend=False,
        hovertemplate=f"k={kv}, a={A2_DEF}, kr={KR2_DEF}<br>t=%{{x:.2f}}s  y=%{{y:.3f}}<extra></extra>"))

for av in a_grid2:
    yinf=K2_DEF*KR2_DEF/av; y=yinf*(1-np.exp(-av*t_s2))
    traces2.append(go.Scatter(x=t_s2, y=y, mode="lines",
        line=dict(color="#d62728", width=2.2),
        visible=(abs(av-A2_DEF)<1e-9), showlegend=False,
        hovertemplate=f"k={K2_DEF}, a={av}, kr={KR2_DEF}<br>t=%{{x:.2f}}s  y=%{{y:.3f}}<extra></extra>"))

for krv in kr_grid2:
    yinf=K2_DEF*krv/A2_DEF; y=yinf*(1-np.exp(-A2_DEF*t_s2))
    traces2.append(go.Scatter(x=t_s2, y=y, mode="lines",
        line=dict(color="#2ca02c", width=2.2),
        visible=(abs(krv-KR2_DEF)<1e-9), showlegend=False,
        hovertemplate=f"k={K2_DEF}, a={A2_DEF}, kr={krv}<br>t=%{{x:.2f}}s  y=%{{y:.3f}}<extra></extra>"))

def vis2_fn(idx): v=[False]*total2; v[idx]=True; return v
def idx_def(g, v): return int(np.where(np.isclose(g, v))[0][0])

sk2=[dict(method="update", label=str(kv),
    args=[{"visible": vis2_fn(i)},
          {"title.text": f"k={kv} | a={A2_DEF} | kr={KR2_DEF} — y(∞)={kv*KR2_DEF/A2_DEF:.2f}  τ={1/A2_DEF:.2f}s  Ts={4/A2_DEF:.2f}s"}])
    for i, kv in enumerate(k_grid2)]

sa2=[dict(method="update", label=str(av),
    args=[{"visible": vis2_fn(nk2+j)},
          {"title.text": f"k={K2_DEF} | a={av} | kr={KR2_DEF} — y(∞)={K2_DEF*KR2_DEF/av:.2f}  τ={1/av:.2f}s  Ts={4/av:.2f}s"}])
    for j, av in enumerate(a_grid2)]

skr2=[dict(method="update", label=str(krv),
    args=[{"visible": vis2_fn(nk2+na2+m)},
          {"title.text": f"k={K2_DEF} | a={A2_DEF} | kr={krv} — y(∞)={K2_DEF*krv/A2_DEF:.2f}  τ={1/A2_DEF:.2f}s  Ts={4/A2_DEF:.2f}s"}])
    for m, krv in enumerate(kr_grid2)]

fig_exp2 = go.Figure(data=traces2)
fig_exp2.update_layout(
    title=dict(text=f"k={K2_DEF} | a={A2_DEF} | kr={KR2_DEF} — y(∞)={K2_DEF*KR2_DEF/A2_DEF:.2f}  τ={1/A2_DEF:.2f}s  Ts={4/A2_DEF:.2f}s", font=dict(size=12)),
    xaxis=dict(title="t (s)"),
    yaxis=dict(title="y(t)"),
    height=460,
    margin=dict(l=60, r=20, t=60, b=140),
    template="plotly_white",
    showlegend=False,
    hovermode="x unified",
    sliders=[
        dict(active=idx_def(k_grid2, K2_DEF),
             currentvalue=dict(prefix="k = ", font=dict(size=13, color="#1f77b4"), xanchor="left"),
             pad=dict(t=10, b=0), x=0.0, y=0.26, len=1.0,
             steps=sk2, tickcolor="#1f77b4"),
        dict(active=idx_def(a_grid2, A2_DEF),
             currentvalue=dict(prefix="a = ", font=dict(size=13, color="#d62728"), xanchor="left"),
             pad=dict(t=10, b=0), x=0.0, y=0.14, len=1.0,
             steps=sa2, tickcolor="#d62728"),
        dict(active=idx_def(kr_grid2, KR2_DEF),
             currentvalue=dict(prefix="kr = ", font=dict(size=13, color="#2ca02c"), xanchor="left"),
             pad=dict(t=10, b=0), x=0.0, y=0.02, len=1.0,
             steps=skr2, tickcolor="#2ca02c"),
    ]
)
fig_exp2.add_hline(y=0, line_width=0.6, line_color="black")
st.plotly_chart(fig_exp2, use_container_width=True)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 3 — GRAU RELATIVO 1
# ═══════════════════════════════════════════════════════════════════════════════
st.header("3. Sistemas de Grau Relativo 1 — Exemplos e Efeito dos Parâmetros")

st.markdown(r"""
### 3.1 Exemplos físicos

Todos os sistemas abaixo seguem $H(s) = k/(s+a)$, com $k$ e $a$ determinados pelos parâmetros físicos:

| Domínio | Sistema ($u \to y$) | $k$ | $a$ |
|---|---|---|---|
| Elétrico | Circuito RL: $V_a \to I$ | $1/L$ | $R/L$ |
| Elétrico | Circuito RC: $V_e \to V_s$ | $1/(RC)$ | $1/(RC)$ |
| Mecânico translacional | Massa-amortecedor: $F \to v$ | $1/M$ | $B/M$ |
| Mecânico rotacional | Inércia-amortecedor: $\mathcal{T} \to \omega$ | $1/J$ | $B/J$ |
| Térmico | Câmara isolada: $\dot{Q} \to T$ | $1/C_t$ | $1/(R_t C_t)$ |
| Hidráulico | Reservatório: $Q_i \to h$ | $1/C_h$ | $1/(R_h C_h)$ |

> Nos sistemas térmico e hidráulico, $R$ e $C$ representam a resistência e a capacitância do domínio correspondente.

### 3.2 Efeito dos parâmetros na resposta ao degrau

**Variação de $k$ (polo $a$ fixo):** altera o **ganho estático** $k' = k/a$ sem afetar a velocidade de resposta ($\tau = 1/a$ invariante).

**Variação de $a$ (ganho $k$ fixo):** desloca o polo para $s = -a$. Aumentar $a$ afasta o polo da origem, reduz $\tau = 1/a$ e torna a resposta mais rápida, porém reduz $y(\infty) = k/a$.
""")

t_arr3 = np.linspace(0, 12, 600)
a_fix3=0.8; k_fix3=1.0

fig3, axes3 = plt.subplots(1, 2, figsize=(9.5, 3.2))

ax = axes3[0]
ks3=[1, 2, 3, 4, 5, 6]
colors_k3=plt.cm.viridis(np.linspace(0.15, 0.88, len(ks3)))
for kv, col in zip(ks3, colors_k3):
    ax.plot(t_arr3, step_response(kv, a_fix3, t_arr3), color=col, label=f"k={kv}")
ax.axvline(1/a_fix3, color="purple", lw=0.9, ls=":", label=rf"$\tau={1/a_fix3:.2f}$s")
ax.set_xlim(0, 12)
estilo(ax, xlabel="t (s)")
ax.set_title(rf"Variação de $k$ (polo $a={a_fix3}$ fixo)", fontsize=8.5)
ax.legend(ncol=2, fontsize=7)

ax2 = axes3[1]
a_vals3=[0.4, 0.8, 1.2, 1.6, 2.0, 2.5]
colors_a3=plt.cm.plasma(np.linspace(0.15, 0.88, len(a_vals3)))
for av, col in zip(a_vals3, colors_a3):
    ax2.plot(t_arr3, step_response(k_fix3, av, t_arr3), color=col, label=f"a={av}")
ax2.axhline(k_fix3, color="gray", lw=0.8, ls="--", label=r"$y(\infty)=k/a \to 1/a$")
ax2.set_xlim(0, 12)
estilo(ax2, xlabel="t (s)")
ax2.set_title(rf"Variação de $a$ (ganho $k={k_fix3}$ fixo)", fontsize=8.5)
ax2.legend(ncol=2, fontsize=7)
plt.tight_layout()
show_fig(fig3, 0.88)

# Diagrama polo-zero + resposta
k_v3=4.0; a_v3=0.8
y3=step_response(k_v3, a_v3, t_arr3)
yinf3=k_v3/a_v3
Ts3_idx=np.argmax(y3>=0.98*yinf3); Ts3_med=t_arr3[Ts3_idx]

fig3b, axes3b = plt.subplots(1, 2, figsize=(9.5, 3.2))
ax = axes3b[0]
ax.axhline(0, color="k", lw=0.8); ax.axvline(0, color="k", lw=0.8)
ax.fill_betweenx([-1.5, 1.5], -5, 0, alpha=0.07, color="seagreen")
ax.fill_betweenx([-1.5, 1.5],  0, 1.5, alpha=0.07, color="crimson")
ax.plot(-a_v3, 0, "x", color=COR["saida"], ms=14, mew=3, label=rf"polo $s={-a_v3}$")
ax.set_xlim(-5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.set_xlabel(r"$\sigma$", fontsize=8); ax.set_ylabel(r"$j\omega$", fontsize=8)
ax.set_title(rf"Plano $s$: $H(s)={k_v3:.0f}/(s+{a_v3})$", fontsize=8.5)
ax.spines[["right", "top"]].set_visible(False); ax.legend(fontsize=7.5)

ax2 = axes3b[1]
ax2.plot(t_arr3, y3, color=COR["degrau"], lw=2.0)
ax2.axhline(yinf3, color="gray", lw=0.8, ls="--")
ax2.axhline(0.98*yinf3, color="brown", lw=0.7, ls=":")
ax2.axvline(Ts3_med, color="brown", lw=0.9, ls=":")
ax2.axvline(1/a_v3, color="purple", lw=0.9, ls=":")
ax2.text(Ts3_med+0.1, 0.5, r"$T_{s_{2\%}}$" + f"={Ts3_med:.1f}s", color="brown", fontsize=7.5)
ax2.text(1/a_v3+0.1, 0.3, rf"$\tau={1/a_v3:.2f}$s", color="purple", fontsize=7.5)
ax2.text(11.8, yinf3+0.15, f"$y(\\infty)={yinf3:.1f}$", fontsize=7.5, ha="right")
estilo(ax2, xlabel="t (s)")
ax2.set_title("Resposta ao degrau unitário", fontsize=8.5)
plt.tight_layout()
show_fig(fig3b, 0.88)

# ── Explorador interativo seção 3 ─────────────────────────────────────────────
st.markdown("### 3.3 🎛️ Explorador Interativo — Plano $s$ + Resposta ao Degrau")
st.caption("Slider **azul** = $k$ (só amplitude muda, polo fixo) · Slider **vermelho** = $a$ (polo desloca)")

t_s3 = np.linspace(0, 15, 600)
k_grid3=np.round(np.arange(0.5, 6.1, 0.5), 2)
a_grid3=np.round(np.arange(0.2, 3.3, 0.2), 2)
K3_DEF=2.0; A3_DEF=0.8
nk3=len(k_grid3); na3=len(a_grid3)

fig_exp3=make_subplots(rows=1, cols=2, subplot_titles=("Plano s", "Resposta ao degrau unitário"))

for kv in k_grid3:
    yinf=kv/A3_DEF; y=yinf*(1-np.exp(-A3_DEF*t_s3))
    vis=(abs(kv-K3_DEF)<1e-9)
    fig_exp3.add_trace(go.Scatter(x=[-A3_DEF], y=[0], mode="markers",
        marker=dict(symbol="x", size=14, color="#d62728", line=dict(width=3, color="#d62728")),
        visible=vis, showlegend=False,
        hovertemplate=f"polo s={-A3_DEF:.2f}<extra>k={kv}</extra>"), row=1, col=1)
    fig_exp3.add_trace(go.Scatter(x=t_s3, y=y, mode="lines",
        line=dict(color="#1f77b4", width=2.2),
        visible=vis, showlegend=False,
        hovertemplate=f"k={kv},a={A3_DEF}<br>t=%{{x:.2f}}s y=%{{y:.3f}}<extra></extra>"), row=1, col=2)

for av in a_grid3:
    yinf=K3_DEF/av; y=yinf*(1-np.exp(-av*t_s3))
    vis=(abs(av-A3_DEF)<1e-9)
    fig_exp3.add_trace(go.Scatter(x=[-av], y=[0], mode="markers",
        marker=dict(symbol="x", size=14, color="#d62728", line=dict(width=3, color="#d62728")),
        visible=vis, showlegend=False,
        hovertemplate=f"polo s={-av:.2f}<extra>a={av}</extra>"), row=1, col=1)
    fig_exp3.add_trace(go.Scatter(x=t_s3, y=y, mode="lines",
        line=dict(color="#d62728", width=2.2),
        visible=vis, showlegend=False,
        hovertemplate=f"k={K3_DEF},a={av}<br>t=%{{x:.2f}}s y=%{{y:.3f}}<extra></extra>"), row=1, col=2)

def vis3_fn(grp, idx):
    v=[False]*(2*(nk3+na3))
    base=2*({"k":0,"a":nk3}[grp]+idx)
    v[base]=v[base+1]=True; return v

sk3=[dict(method="update", label=str(kv),
    args=[{"visible": vis3_fn("k", i)},
          {"title": f"k={kv},a={A3_DEF} | polo s={-A3_DEF:.2f} | y(inf)={kv/A3_DEF:.3f} tau={1/A3_DEF:.2f}s Ts={4/A3_DEF:.2f}s"}])
    for i, kv in enumerate(k_grid3)]
sa3=[dict(method="update", label=str(av),
    args=[{"visible": vis3_fn("a", j)},
          {"title": f"k={K3_DEF},a={av} | polo s={-av:.2f} | y(inf)={K3_DEF/av:.3f} tau={1/av:.2f}s Ts={4/av:.2f}s"}])
    for j, av in enumerate(a_grid3)]

fig_exp3.update_layout(
    title=dict(text=f"k={K3_DEF} | a={A3_DEF} | polo s={-A3_DEF:.2f} — y(∞)={K3_DEF/A3_DEF:.3f}  τ={1/A3_DEF:.2f}s  Ts={4/A3_DEF:.2f}s", font=dict(size=12)),
    height=460, margin=dict(l=60, r=20, t=60, b=100), template="plotly_white",
    sliders=[
        dict(active=idx_def(k_grid3, K3_DEF),
             currentvalue=dict(prefix="k = ", font=dict(size=13, color="#1f77b4"), xanchor="left"),
             pad=dict(t=10, b=0), x=0.0, y=0.14, len=1.0, steps=sk3, tickcolor="#1f77b4"),
        dict(active=idx_def(a_grid3, A3_DEF),
             currentvalue=dict(prefix="a = ", font=dict(size=13, color="#d62728"), xanchor="left"),
             pad=dict(t=10, b=0), x=0.0, y=0.02, len=1.0, steps=sa3, tickcolor="#d62728"),
    ]
)
fig_exp3.update_xaxes(title_text="σ", range=[-7, 1.5], zeroline=True, zerolinecolor="black", row=1, col=1)
fig_exp3.update_yaxes(title_text="jω", range=[-1.5, 1.5], zeroline=True, zerolinecolor="black", row=1, col=1)
fig_exp3.update_xaxes(title_text="t (s)", row=1, col=2)
fig_exp3.update_yaxes(title_text="y(t)", row=1, col=2)
fig_exp3.add_vrect(x0=-7, x1=0, fillcolor="seagreen", opacity=0.05, layer="below", line_width=0, row=1, col=1)
fig_exp3.add_vrect(x0=0, x1=1.5, fillcolor="crimson", opacity=0.05, layer="below", line_width=0, row=1, col=1)
st.plotly_chart(fig_exp3, use_container_width=True)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 4 — GRAU RELATIVO 0 / EFEITO DO ZERO
# ═══════════════════════════════════════════════════════════════════════════════
st.header("4. Sistemas de Grau Relativo 0 — Efeito do Zero")

st.markdown(r"""
### 4.1 Função de transferência com zero finito

Adicionando um zero em $s = -b$ ao sistema de 1ª ordem ($n^* = 1 - 1 = 0$):

$$H'(s) = \frac{k(s+b)}{s+a} = \frac{k\,b}{s+a} + \frac{k\,s}{s+a}$$

### 4.2 Resposta ao degrau unitário ($k_r = 1$)

$$\boxed{y'(t) = \frac{k\,b}{a} + k\!\left(1 - \frac{b}{a}\right)e^{-at}, \quad t\geq 0}$$

Valores notáveis: $\quad y'(0^+) = k$ (independe de $b$), $\quad y'(\infty) = k\,b/a$

O zero **não altera $\tau = 1/a$**, mas modifica o valor inicial e o valor final.

### 4.3 Classificação pelo sinal de $b$

| Posição do zero | Característica | Comportamento transiente |
|---|---|---|
| $b > 0$ — semiplano esquerdo | Sistema de **fase mínima** | $y'(0^+)=k>0$, $y'(\infty)=kb/a>0$; resposta mais rápida |
| $b = a$ — coincide com o polo | **Cancelamento polo-zero** | $H'(s) = k$ (ganho puro); resposta instantânea |
| $b < 0$ — semiplano direito | Sistema de **fase não-mínima** | $y'(0^+)=k>0$, mas $y'(\infty)=kb/a<0$; resposta inverte de sinal |

> **Fase não-mínima** ($b<0$): $y'(0^+)$ e $y'(\infty)$ têm sinais opostos — a saída começa subindo e termina no negativo. Esse comportamento dificulta o controle.
""")

t_arr4 = np.linspace(0, 12, 600)
k_v4=4.0; a_v4=0.8
cenarios4=[(3.0,  "b=+3 (zero esq., fase mínima)",       COR["natural"]),
            (-3.0, "b=−3 (zero dir., fase não-mínima)",   COR["saida"]),
            (0.8,  "b=a=0.8 (polo-zero cancela)",          COR["degrau"])]

fig4a, axes4a = plt.subplots(1, 3, figsize=(9.5, 3.2))
for ax, (bv, lbl, col) in zip(axes4a, cenarios4):
    y = step_response_zero(k_v4, a_v4, bv, t_arr4)
    ax.plot(t_arr4, y, color=col, lw=2.0)
    ax.axhline(y[-1], color="gray", lw=0.8, ls="--")
    ax.axhline(0, color="k", lw=0.5)
    estilo(ax, xlabel="t (s)"); ax.set_title(lbl, fontsize=8)
    ins=ax.inset_axes([0.54, 0.06, 0.44, 0.42])
    ins.axhline(0, color="k", lw=0.6); ins.axvline(0, color="k", lw=0.6)
    ins.plot(-a_v4, 0, "x", color=COR["saida"], ms=9, mew=2.0)
    ins.plot(-bv, 0, "o", color=COR["natural"], ms=7, mfc="white", mew=1.8)
    ins.set_xlim(-5, 3); ins.set_ylim(-1.2, 1.2)
    ins.set_xticks([]); ins.set_yticks([]); ins.set_title("Plano s", fontsize=7)
plt.tight_layout()
show_fig(fig4a, 0.88)

# Curvas sobrepostas
b_vals4=[-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]
colors4=plt.cm.RdYlGn(np.linspace(0.08, 0.92, len(b_vals4)))

fig4b, axes4b = plt.subplots(1, 2, figsize=(9.5, 3.2))
ax_pz4=axes4b[0]; ax_r4=axes4b[1]
ax_pz4.axhline(0, color="k", lw=0.8); ax_pz4.axvline(0, color="k", lw=0.8)
ax_pz4.fill_betweenx([-1.5, 1.5], -8, 0, alpha=0.06, color="seagreen")
ax_pz4.fill_betweenx([-1.5, 1.5],  0, 4, alpha=0.06, color="crimson")
ax_pz4.plot(-a_v4, 0, "x", color=COR["saida"], ms=14, mew=3, label="polo")
for bv, col in zip(b_vals4, colors4):
    y=step_response_zero(k_v4, a_v4, bv, t_arr4)
    ax_r4.plot(t_arr4, y, color=col, lw=1.8, label=f"b={bv:+.0f}")
    ax_pz4.plot(-bv, 0, "o", color=col, ms=8, mfc="white", mew=2.0, label=f"b={bv:+.0f}")
ax_pz4.set_xlim(-8, 4); ax_pz4.set_ylim(-1.5, 1.5)
ax_pz4.set_xlabel(r"$\sigma$", fontsize=8); ax_pz4.set_ylabel(r"$j\omega$", fontsize=8)
ax_pz4.set_title(r"Plano $s$ — zeros e polo fixo", fontsize=8.5)
ax_pz4.spines[["right", "top"]].set_visible(False); ax_pz4.legend(ncol=2, fontsize=6.5)
ax_r4.axhline(0, color="k", lw=0.5)
estilo(ax_r4, xlabel="t (s)")
ax_r4.set_title(r"Resposta ao degrau — variação de $b$", fontsize=8.5)
ax_r4.legend(ncol=2, fontsize=7)
plt.tight_layout()
show_fig(fig4b, 0.88)

# ── Explorador interativo seção 4 ─────────────────────────────────────────────
st.markdown("### 4.4 🎛️ Explorador Interativo — Sistema com Zero")
st.caption("○ = zero · × = polo · Slider **azul** = $k$ · **vermelho** = $a$ · **verde** = $b$")

t_s4 = np.linspace(0, 15, 600)
k_grid4=np.round(np.arange(0.5, 6.1, 0.5), 2)
a_grid4=np.round(np.arange(0.2, 3.3, 0.2), 2)
b_grid4=np.round(np.arange(-5.0, 5.1, 0.5), 2)
K4_DEF=2.0; A4_DEF=0.8; B4_DEF=2.0
nk4=len(k_grid4); na4=len(a_grid4); nb4=len(b_grid4)

fig_exp4=make_subplots(rows=1, cols=2, subplot_titles=("Plano s", "Resposta ao degrau"))

def add_grp4(grid, fk, fa, fb, vary, ctrace, czero):
    for val in grid:
        kv=val if vary=="k" else fk
        av=val if vary=="a" else fa
        bv=val if vary=="b" else fb
        def_val={"k":fk,"a":fa,"b":fb}[vary]
        vis=(abs(val-def_val)<1e-9)
        s_h=lti([kv, kv*bv], [1, av])
        _, y=sc_step(s_h, T=t_s4)
        fig_exp4.add_trace(go.Scatter(x=[-av], y=[0], mode="markers",
            marker=dict(symbol="x", size=14, color="#d62728", line=dict(width=3, color="#d62728")),
            visible=vis, showlegend=False,
            hovertemplate=f"polo s={-av:.2f}<extra>{vary}={val}</extra>"), row=1, col=1)
        fig_exp4.add_trace(go.Scatter(x=[-bv], y=[0], mode="markers",
            marker=dict(symbol="circle-open", size=12, color=czero, line=dict(width=2.5)),
            visible=vis, showlegend=False,
            hovertemplate=f"zero s={-bv:.2f}<extra>{vary}={val}</extra>"), row=1, col=1)
        fig_exp4.add_trace(go.Scatter(x=t_s4, y=y, mode="lines",
            line=dict(color=ctrace, width=2.2),
            visible=vis, showlegend=False,
            hovertemplate=f"k={kv},a={av},b={bv}<br>t=%{{x:.2f}}s y=%{{y:.3f}}<extra></extra>"), row=1, col=2)

add_grp4(k_grid4, K4_DEF, A4_DEF, B4_DEF, "k", "#1f77b4", "#1f77b4")
add_grp4(a_grid4, K4_DEF, A4_DEF, B4_DEF, "a", "#d62728", "#d62728")
add_grp4(b_grid4, K4_DEF, A4_DEF, B4_DEF, "b", "#2ca02c", "#2ca02c")

def vis4_fn(grp, idx):
    v=[False]*(3*(nk4+na4+nb4))
    base=3*({"k":0,"a":nk4,"b":nk4+na4}[grp]+idx)
    v[base]=v[base+1]=v[base+2]=True; return v

def mk_steps4(grid, grp, fk, fa, fb):
    steps=[]
    for i, val in enumerate(grid):
        kv=val if grp=="k" else fk
        av=val if grp=="a" else fa
        bv=val if grp=="b" else fb
        yinf=kv*bv/av if av>0 else 0
        steps.append(dict(method="update", label=str(val),
            args=[{"visible": vis4_fn(grp, i)},
                  {"title": f"{grp}={val} | polo s={-av:.2f} zero s={-bv:.2f} | y(inf)={yinf:.3f} tau={1/av:.2f}s"}]))
    return steps

fig_exp4.update_layout(
    title=dict(text=f"k={K4_DEF} | a={A4_DEF} | b={B4_DEF} — polo s={-A4_DEF:.2f}  zero s={-B4_DEF:.2f}  y(∞)={K4_DEF*B4_DEF/A4_DEF:.3f}  τ={1/A4_DEF:.2f}s", font=dict(size=12)),
    height=480, margin=dict(l=60, r=20, t=60, b=140), template="plotly_white",
    sliders=[
        dict(active=idx_def(k_grid4, K4_DEF),
             currentvalue=dict(prefix="k = ", font=dict(size=13, color="#1f77b4"), xanchor="left"),
             pad=dict(t=10, b=0), x=0.0, y=0.26, len=1.0,
             steps=mk_steps4(k_grid4, "k", K4_DEF, A4_DEF, B4_DEF), tickcolor="#1f77b4"),
        dict(active=idx_def(a_grid4, A4_DEF),
             currentvalue=dict(prefix="a = ", font=dict(size=13, color="#d62728"), xanchor="left"),
             pad=dict(t=10, b=0), x=0.0, y=0.14, len=1.0,
             steps=mk_steps4(a_grid4, "a", K4_DEF, A4_DEF, B4_DEF), tickcolor="#d62728"),
        dict(active=idx_def(b_grid4, B4_DEF),
             currentvalue=dict(prefix="b = ", font=dict(size=13, color="#2ca02c"), xanchor="left"),
             pad=dict(t=10, b=0), x=0.0, y=0.02, len=1.0,
             steps=mk_steps4(b_grid4, "b", K4_DEF, A4_DEF, B4_DEF), tickcolor="#2ca02c"),
    ]
)
fig_exp4.update_xaxes(title_text="σ", range=[-8, 4], zeroline=True, zerolinecolor="black", row=1, col=1)
fig_exp4.update_yaxes(title_text="jω", range=[-1.8, 1.8], zeroline=True, zerolinecolor="black", row=1, col=1)
fig_exp4.update_xaxes(title_text="t (s)", row=1, col=2)
fig_exp4.update_yaxes(title_text="y(t)", row=1, col=2)
fig_exp4.add_vrect(x0=-8, x1=0, fillcolor="seagreen", opacity=0.05, layer="below", line_width=0, row=1, col=1)
fig_exp4.add_vrect(x0=0, x1=4, fillcolor="crimson", opacity=0.05, layer="below", line_width=0, row=1, col=1)
st.plotly_chart(fig_exp4, use_container_width=True)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 5 — POLO NO SEMIPLANO DIREITO
# ═══════════════════════════════════════════════════════════════════════════════
st.header("5. Polo no Semiplano Direito — Sistema Instável")

st.markdown(r"""
### 5.1 Resposta ao degrau

Para polo em $s = +a$ ($a > 0$):

$$H(s) = \frac{k}{s - a} \quad\Rightarrow\quad y(t) = \frac{k}{a}\bigl(e^{+at} - 1\bigr), \quad y(0^+) = 0$$

A saída **cresce sem limite** — sistema **BIBO instável**.

### 5.2 Efeito de um zero adicional

Para $H'(s) = k(s+b)/(s-a)$, a resposta ao degrau tem $y'(0^+) = k$ e coeficiente exponencial $k(a+b)/a$:

| Zero | Coeficiente de $e^{+at}$ | Efeito |
|---|---|---|
| Sem zero | $k/a$ | Divergência padrão |
| $b > 0$ (semiplano esq.) | $k(a+b)/a > k/a$ | Diverge **mais rápido** |
| $b < 0$, $|b|< a$ | $0 < k(a+b)/a < k/a$ | Diverge **mais devagar** |
| $b = -a$ (cancela polo) | $0$ — sistema estável! | Cancelamento instável$^*$ |

> $^*$O cancelamento polo-zero instável é perigoso na prática: qualquer perturbação excita o modo instável.

> Um polo real positivo **não pode ser estabilizado** apenas por ajuste de ganho em malha aberta.
""")

t_arr5 = np.linspace(0, 6, 500)
k_v5=1.0; a_v5=0.5
cenarios5=[([k_v5], [1,-a_v5],       r"$H(s)=k/(s-a)$, sem zero"),
            ([k_v5, 3*k_v5], [1,-a_v5], r"$H'(s)=k(s+3)/(s-a)$, zero esq."),
            ([k_v5,-3*k_v5], [1,-a_v5], r"$H'(s)=k(s-3)/(s-a)$, zero dir.")]

fig5, axes5 = plt.subplots(1, 3, figsize=(9.5, 3.0))
for ax, (num, den, ttl) in zip(axes5, cenarios5):
    _, y=sc_step(lti(num, den), T=t_arr5)
    ax.plot(t_arr5, y, color=COR["instavel"], lw=2.0)
    ax.axhline(0, color="k", lw=0.6, ls="--")
    estilo(ax, xlabel="t (s)"); ax.set_title(ttl, fontsize=8)
plt.suptitle(rf"Sistemas instáveis: polo em $s=+{a_v5}$", fontsize=9, fontweight="bold")
plt.tight_layout()
show_fig(fig5, 0.85)

# ── Explorador interativo seção 5 ─────────────────────────────────────────────
st.markdown("### 5.3 🎛️ Explorador Interativo — Velocidade de Divergência")
st.caption("Slider **vermelho** = $a$ — quanto maior $a$, mais rápida a divergência (constante de tempo $1/a$)")

t_s5 = np.linspace(0, 8, 500)
a_grid5=np.round(np.arange(0.1, 2.1, 0.1), 2)
A5_DEF=0.5; k5_val=1.0

fig_exp5=make_subplots(rows=1, cols=2, subplot_titles=("Plano s (polo instável)", "Resposta ao degrau"))

for av in a_grid5:
    _, y=sc_step(lti([k5_val], [1,-av]), T=t_s5)
    vis=(abs(av-A5_DEF)<1e-9)
    fig_exp5.add_trace(go.Scatter(x=[av], y=[0], mode="markers",
        marker=dict(symbol="x", size=14, color="#d62728", line=dict(width=3, color="#d62728")),
        visible=vis, showlegend=False,
        hovertemplate=f"polo s=+{av:.2f}<extra>a={av}</extra>"), row=1, col=1)
    fig_exp5.add_trace(go.Scatter(x=t_s5, y=y, mode="lines",
        line=dict(color="#d62728", width=2.2),
        visible=vis, showlegend=False,
        hovertemplate=f"a={av}<br>t=%{{x:.2f}}s y=%{{y:.1f}}<extra></extra>"), row=1, col=2)

def vis5_fn(i): v=[False]*(2*len(a_grid5)); v[2*i]=v[2*i+1]=True; return v

steps5=[dict(method="update", label=str(av),
    args=[{"visible": vis5_fn(i)},
          {"title": f"Sistema instável: polo em s=+{av:.2f} | y(t) ∝ exp(+{av}·t)"}])
    for i, av in enumerate(a_grid5)]

fig_exp5.update_layout(
    title=dict(text=f"Sistema instável — polo em s=+{A5_DEF:.2f}  |  y(t) ∝ e^(+{A5_DEF}·t)", font=dict(size=12)),
    height=420, margin=dict(l=60, r=20, t=60, b=90), template="plotly_white",
    sliders=[dict(active=idx_def(a_grid5, A5_DEF),
                  currentvalue=dict(prefix="a = ", font=dict(size=13, color="#d62728"), xanchor="left"),
                  pad=dict(t=10, b=0), x=0.0, y=0.04, len=1.0,
                  steps=steps5, tickcolor="#d62728")]
)
fig_exp5.update_xaxes(title_text="σ", range=[-2, 3], zeroline=True, zerolinecolor="black", row=1, col=1)
fig_exp5.update_yaxes(title_text="jω", range=[-1.5, 1.5], zeroline=True, zerolinecolor="black", row=1, col=1)
fig_exp5.update_xaxes(title_text="t (s)", row=1, col=2)
fig_exp5.update_yaxes(title_text="y(t)", row=1, col=2)
fig_exp5.add_vrect(x0=-2, x1=0, fillcolor="seagreen", opacity=0.05, layer="below", line_width=0, row=1, col=1)
fig_exp5.add_vrect(x0=0, x1=3, fillcolor="crimson", opacity=0.08, layer="below", line_width=0, row=1, col=1)
st.plotly_chart(fig_exp5, use_container_width=True)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 6 — POLO NA ORIGEM
# ═══════════════════════════════════════════════════════════════════════════════
st.header("6. Polo na Origem — Sistema Marginalmente Estável")

st.markdown(r"""
### 6.1 Integrador puro (malha aberta)

Com polo em $s = 0$:

$$G(s) = \frac{k}{s} \quad\Rightarrow\quad y(t) = k\,t \quad\text{(rampa)}$$

A saída cresce sem limite mas **não exponencialmente** — sistema **marginalmente estável**
(polo no eixo imaginário). O integrador é ubíquo em sistemas de controle: motores DC,
atuadores hidráulicos e servomecanismos possuem um polo na origem.

### 6.2 Estabilização por realimentação negativa unitária

$$H(s) = \frac{G(s)}{1+G(s)} = \frac{k/s}{1+k/s} = \frac{k}{s+k}$$

O polo migra de $s=0$ para $s=-k$:

| | Malha aberta | Malha fechada |
|---|---|---|
| Polo | $s = 0$ | $s = -k$ |
| Estabilidade | Marginal | **Estável** |
| Resposta ao degrau | Rampa $k\,t$ | Exponencial; $y(\infty)=1$ |
| Constante de tempo | — | $\tau = 1/k$ |
| $T_{s_{2\%}}$ | — | $\approx 4/k$ |

Aumentar $k$ afasta o polo da origem e acelera a resposta de malha fechada.
""")

t_arr6 = np.linspace(0, 10, 600)
k_vals6=[1, 2, 3, 4, 5, 6]
colors6=plt.cm.viridis(np.linspace(0.15, 0.88, len(k_vals6)))

fig6a, axes6a = plt.subplots(1, 2, figsize=(9.5, 3.2))
ax = axes6a[0]
for kv, col in zip(k_vals6, colors6):
    ax.plot(t_arr6, kv*t_arr6, color=col, label=f"k={kv}")
ax.set_ylim(0, 28)
estilo(ax, xlabel="t (s)")
ax.set_title(r"Malha aberta $G(s)=k/s$ — saída rampa", fontsize=8.5)
ax.legend(ncol=2, fontsize=7)

ax2 = axes6a[1]
for kv, col in zip(k_vals6, colors6):
    ax2.plot(t_arr6, step_response(kv, kv, t_arr6), color=col, label=f"k={kv}")
ax2.axhline(1.0, color="gray", lw=0.8, ls="--", label=r"$y(\infty)=1$")
estilo(ax2, xlabel="t (s)")
ax2.set_title(r"Malha fechada $H(s)=k/(s+k)$", fontsize=8.5)
ax2.legend(ncol=2, fontsize=7)
plt.tight_layout()
show_fig(fig6a, 0.88)

fig6b, axes6b = plt.subplots(1, 2, figsize=(7.5, 2.8))
ax = axes6b[0]
ax.axhline(0, color="k", lw=0.8); ax.axvline(0, color="k", lw=0.8)
ax.plot(0, 0, "x", color="darkorange", ms=14, mew=3, label=r"polo $s=0$")
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1, 1)
ax.set_xlabel(r"$\sigma$", fontsize=8); ax.set_ylabel(r"$j\omega$", fontsize=8)
ax.set_title(r"Malha aberta $G(s)=k/s$", fontsize=8.5)
ax.spines[["right", "top"]].set_visible(False); ax.legend(fontsize=7.5)

ax2 = axes6b[1]
ax2.axhline(0, color="k", lw=0.8); ax2.axvline(0, color="k", lw=0.8)
ax2.fill_betweenx([-1, 1], -8, 0, alpha=0.07, color="seagreen")
for kv, col in zip(k_vals6, colors6):
    ax2.plot(-kv, 0, "x", color=col, ms=12, mew=2.5, label=f"k={kv}")
ax2.set_xlim(-8, 1); ax2.set_ylim(-1, 1)
ax2.set_xlabel(r"$\sigma$", fontsize=8); ax2.set_ylabel(r"$j\omega$", fontsize=8)
ax2.set_title(r"Malha fechada $H(s)=k/(s+k)$ — polo em $s=-k$", fontsize=8.5)
ax2.spines[["right", "top"]].set_visible(False); ax2.legend(ncol=2, fontsize=7)
plt.tight_layout()
show_fig(fig6b, 0.72)

# ── Explorador interativo seção 6 ─────────────────────────────────────────────
st.markdown("### 6.3 🎛️ Explorador Interativo — Polo MA vs. Polo MF")
st.caption("Slider **azul** = $k$ · Laranja × = polo MA (fixo na origem) · Azul × = polo MF (desloca para $s=-k$)")

t_s6 = np.linspace(0, 10, 600)
k_grid6=np.round(np.arange(0.5, 8.1, 0.5), 2)
K6_DEF=2.0

fig_exp6=make_subplots(rows=1, cols=2,
    subplot_titles=("Plano s: MA (laranja) vs MF (azul)", "Resposta ao degrau MF"))

for kv in k_grid6:
    y_mf=1.0*(1-np.exp(-kv*t_s6))
    vis=(abs(kv-K6_DEF)<1e-9)
    fig_exp6.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
        marker=dict(symbol="x", size=14, color="darkorange", line=dict(width=3, color="darkorange")),
        visible=vis, showlegend=False,
        hovertemplate="polo MA: s=0<extra></extra>"), row=1, col=1)
    fig_exp6.add_trace(go.Scatter(x=[-kv], y=[0], mode="markers",
        marker=dict(symbol="x", size=14, color="#1f77b4", line=dict(width=3, color="#1f77b4")),
        visible=vis, showlegend=False,
        hovertemplate=f"polo MF: s={-kv:.2f}<extra>k={kv}</extra>"), row=1, col=1)
    fig_exp6.add_trace(go.Scatter(x=[0, -kv], y=[0, 0], mode="lines",
        line=dict(color="gray", width=1.2, dash="dot"),
        visible=vis, showlegend=False, hoverinfo="skip"), row=1, col=1)
    fig_exp6.add_trace(go.Scatter(x=t_s6, y=y_mf, mode="lines",
        line=dict(color="#1f77b4", width=2.2),
        visible=vis, showlegend=False,
        hovertemplate=f"k={kv}<br>t=%{{x:.2f}}s y=%{{y:.3f}}<extra></extra>"), row=1, col=2)

def vis6_fn(i): v=[False]*(4*len(k_grid6)); [v.__setitem__(4*i+d, True) for d in range(4)]; return v

steps6=[dict(method="update", label=str(kv),
    args=[{"visible": vis6_fn(i)},
          {"title": f"k={kv} | Polo MA: s=0 → Polo MF: s={-kv:.2f} | tau={1/kv:.2f}s Ts={4/kv:.2f}s"}])
    for i, kv in enumerate(k_grid6)]

fig_exp6.update_layout(
    title=dict(text=f"k={K6_DEF} — Polo MA: s=0  →  Polo MF: s={-K6_DEF:.2f}  |  τ={1/K6_DEF:.2f}s  Ts={4/K6_DEF:.2f}s", font=dict(size=12)),
    height=420, margin=dict(l=60, r=20, t=60, b=90), template="plotly_white",
    sliders=[dict(active=idx_def(k_grid6, K6_DEF),
                  currentvalue=dict(prefix="k = ", font=dict(size=13, color="#1f77b4"), xanchor="left"),
                  pad=dict(t=10, b=0), x=0.0, y=0.04, len=1.0,
                  steps=steps6, tickcolor="#1f77b4")]
)
fig_exp6.update_xaxes(title_text="σ", range=[-9, 1.5], zeroline=True, zerolinecolor="black", row=1, col=1)
fig_exp6.update_yaxes(title_text="jω", range=[-1.2, 1.2], zeroline=True, zerolinecolor="black", row=1, col=1)
fig_exp6.update_xaxes(title_text="t (s)", row=1, col=2)
fig_exp6.update_yaxes(title_text="y(t)", range=[-0.05, 1.15], row=1, col=2)
fig_exp6.add_vrect(x0=-9, x1=0, fillcolor="seagreen", opacity=0.06, layer="below", line_width=0, row=1, col=1)
fig_exp6.add_hline(y=1.0, line_width=0.8, line_dash="dash", line_color="gray", row=1, col=2)
st.plotly_chart(fig_exp6, use_container_width=True)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 7 — REFERÊNCIAS
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("7. Referências", expanded=False):
    st.markdown("""
- **LATHI, B. P.; GREEN, R.** *Sinais e Sistemas Lineares*. 3ª ed. Oxford University Press, 2018.
- **DORF, R. C.; BISHOP, R. H.** *Sistemas de Controle Modernos*. 13ª ed. LTC, 2017.
- **OGATA, K.** *Engenharia de Controle Moderno*. 5ª ed. Pearson, 2014.
- **NISE, N. S.** *Engenharia de Sistemas de Controle*. 7ª ed. Wiley / LTC, 2018.
- **DE SOUZA, A. C. Z.; PINHEIRO, C. A. M.** *Introdução à Modelagem, Análise e Simulação de Sistemas Dinâmicos*. 1ª ed. Interciência, 2008.
- **CASTRUCCI, P. B. de L.; BITTAR, A.; SALES, R. M.** *Controle Automático*. 2ª ed. LTC, 2018.
""")

st.divider()

st.markdown(
    "<div style='text-align:center;color:gray;font-size:12px'>"
    "Dinâmica no Domínio do Tempo — Sistemas de Ordem 1 &nbsp;·&nbsp; Modelagem e Sistemas Lineares"
    " &nbsp;·&nbsp; Engenharia de Energia &nbsp;·&nbsp; CNAT — IFRN<br>"
    "Autor: Marcus V A Fernandes &nbsp;·&nbsp; marcus.fernandes@ifrn.edu.br"
    " &nbsp;·&nbsp; v1.1"
    "</div>",
    unsafe_allow_html=True,
)
