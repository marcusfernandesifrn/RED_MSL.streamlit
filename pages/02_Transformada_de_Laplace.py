"""
Transformada de Laplace
Disciplina: Modelagem e Sistemas Lineares
Curso: Engenharia de Energia
Instituição: IFRN — Campus Natal-Central (CNAT)
Autor: Marcus V A Fernandes · marcus.fernandes@ifrn.edu.br · v1.0
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.signal import lti, step as sc_step
from scipy.integrate import solve_ivp
import sympy as sp
from sympy import (symbols, oo, exp, cos, sin, sqrt, latex,
                   DiracDelta, Heaviside, apart, inverse_laplace_transform,
                   laplace_transform, Rational)

# ── Configuração da Página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Transformada de Laplace",
    page_icon="📡",
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
    polo_esq = "seagreen",
    polo_dir = "crimson",
    polo_img = "darkorange",
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

def ponto(ax, x, y):
    ax.plot(x, y, "o", color=COR["bloco_e"], ms=4, zorder=5)

# ── Helpers de diagramas de blocos ────────────────────────────────────────────
def _blk(ax, x, y, w, h, txt, fs=8.5):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x-w/2, y-h/2), w, h, boxstyle="round,pad=0.04",
        facecolor=COR["bloco_f"], edgecolor=COR["bloco_e"], lw=1.4, zorder=3))
    ax.text(x, y, txt, ha="center", va="center", fontsize=fs, zorder=4)

def _arr(ax, x1, y1, x2, y2, lb="", ldy=0.12):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=COR["bloco_e"],
                        lw=1.3, shrinkA=0, shrinkB=0), zorder=2)
    if lb:
        ax.text((x1+x2)/2, (y1+y2)/2+ldy, lb, ha="center", fontsize=8)

def _lin(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color=COR["bloco_e"], lw=1.3, zorder=2)

def _dot(ax, x, y):
    ax.plot(x, y, "o", color=COR["bloco_e"], ms=4, zorder=5)

def _som(ax, x, y, r=0.22):
    ax.add_patch(mpatches.Circle((x, y), r, fc="white",
                  ec=COR["bloco_e"], lw=1.3, zorder=3))
    ax.text(x, y, r"$\Sigma$", ha="center", va="center", fontsize=9, zorder=4)

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
st.title("📡 Transformada de Laplace")
st.caption("Modelagem e Sistemas Lineares · Engenharia de Energia · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

# ── Índice ────────────────────────────────────────────────────────────────────
with st.expander("📋 Índice — clique para expandir", expanded=False):
    st.markdown(r"""
**[1. Definição da Transformada de Laplace](#1-defini-o-da-transformada-de-laplace)**
- 1.1 Transformada bilateral
- 1.2 Transformada unilateral (mais usada em sistemas)
- 1.3 Transformada inversa (integral de Bromwich)
- 1.4 Linearidade

**[2. Tabela de Transformadas](#2-tabela-de-transformadas-de-laplace)**
- Pares fundamentais: $\delta(t)$, $u(t)$, $t^n$, $e^{-at}$, $\sin$, $\cos$, formas amortecidas

**[3. Propriedades da Transformada](#3-propriedades-da-transformada-de-laplace)**
- Linearidade, deslocamento no tempo/frequência, escalamento
- Derivação e integração no tempo
- Teoremas do valor inicial e valor final

**[4. Convolução](#4-convolu-o)**
- 4.1 Convolução no tempo $\leftrightarrow$ multiplicação em $s$
- 4.2 Multiplicação no tempo $\leftrightarrow$ convolução em $s$
- Relação com resposta ao impulso e função de transferência

**[5. Função de Transferência](#5-fun-o-de-transfer-ncia)**
- 5.1 Forma geral — pólos e zeros
- 5.2 Obtenção a partir de EDO (CI nulas)
- Mapa de pólos e zeros

**[6. Estabilidade via Função de Transferência](#6-estabilidade-via-fun-o-de-transfer-ncia)**
- Critério BIBO pela localização dos pólos
- Estável, marginalmente estável e instável
- Critério de Routh-Hurwitz (introdução)

**[7. Realização de Sistemas](#7-realiza-o-de-sistemas)**
- 7.1 Forma direta (canônica)
- 7.2 Realização em cascata
- 7.3 Realização em paralelo
- 7.4 Atraso de transporte — aproximação de Padé
- 7.5 Exemplo numérico completo

**[8. Sistemas Não-Lineares e Linearização](#8-sistemas-n-o-lineares-e-lineariza-o)**
- 8.1 Classificação: não-linearidades de magnitude (saturação, zona morta, relé, atrito, folga, histerese, quantizador)
- 8.2 Não-linearidades de frequência (caos, batimento, arrasto, Duffing, Van der Pol, ressonância)
- 8.3 Linearização pelo método de Taylor (expansão interativa por ordem)

**[9. Resposta no Domínio do Tempo](#9-resposta-no-dom-nio-do-tempo)**
- 9.1 Procedimento geral (aplicar $\mathcal{L}$, resolver, inverter)
- Funções próprias e impróprias — divisão polinomial

**[10. Frações Parciais — Raízes Reais Distintas](#10-fra-es-parciais-ra-zes-reais-distintas)**
- Método de Heaviside
- Exemplos 01, 02 e 03

**[11. Frações Parciais — Raízes Complexas Conjugadas](#11-fra-es-parciais-ra-zes-complexas-conjugadas)**
- Forma via resíduos complexos e forma direta (recomendada)
- Exemplos 04 e 05

**[12. Frações Parciais — Raízes Reais Repetidas](#12-fra-es-parciais-ra-zes-reais-repetidas)**
- Cálculo por derivadas sucessivas de $G(s)$
- Exemplo 06

**[13. Referências](#13-refer-ncias)**
""")

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 1 — DEFINIÇÃO
# ═══════════════════════════════════════════════════════════════════════════════
st.header("1. Definição da Transformada de Laplace")

st.markdown(r"""
A **Transformada de Laplace** representa um sinal $x(t)$ como superposição de exponenciais
complexas $e^{st}$, com $s = \sigma + j\omega$ (**frequência complexa**). Converte equações
diferenciais em equações algébricas no domínio $s$, complementando a análise temporal.

### 1.1 Transformada Bilateral

Válida para todo $t \in (-\infty, +\infty)$, sinais causais e não causais:

$$\mathcal{L}_b[x(t)] = X(s) = \int_{-\infty}^{+\infty} x(t)\,e^{-st}\,dt$$

### 1.2 Transformada Unilateral

Restrita a sinais causais ($x(t) = 0$ para $t < 0$). É o caso mais usado em análise de sistemas:

$$X(s) = \int_{0^-}^{\infty} x(t)\,e^{-st}\,dt$$

O limite inferior $0^-$ permite incorporar condições iniciais descontínuas em $t=0$ sem tratamento especial.

### 1.3 Transformada Inversa

Recupera $x(t)$ a partir de $X(s)$ pela integral de Bromwich, onde $c$ é escolhido para garantir convergência:

$$x(t) = \mathcal{L}^{-1}[X(s)] = \frac{1}{2\pi j} \int_{c-j\infty}^{c+j\infty} X(s)\,e^{st}\,ds$$

Na prática, a inversão é feita por **tabelas de pares** e **frações parciais** (§10–12).

### 1.4 Linearidade

A transformada é linear: para quaisquer constantes $k_1, k_2$,

$$k_1 x_1(t) + k_2 x_2(t) \;\overset{\mathcal{L}}{\longleftrightarrow}\; k_1 X_1(s) + k_2 X_2(s)$$
""")

# Gráfico: comportamento de e^(st)
t_v = np.linspace(0, 5, 1000)
casos_s = [
    (0,    0,  r"$s=0$ (constante)",            COR["sinal"]),
    (0.5,  0,  r"$\sigma>0,\omega=0$ (crescente)", COR["instavel"]),
    (-0.5, 0,  r"$\sigma<0,\omega=0$ (decrescente)", COR["natural"]),
    (0,    4,  r"$\sigma=0$ (senoide pura)",     COR["marginal"]),
    (-0.5, 4,  r"$\sigma<0$ (amortecida)",       COR["saida"]),
]
fig1, axs1 = plt.subplots(1, 5, figsize=(9.5, 2.4))
fig1.suptitle(r"Comportamento de $e^{st}$ para diferentes $s = \sigma + j\omega$",
              fontsize=9, fontweight="bold")
for ax, (sig, omg, titulo, cor) in zip(axs1, casos_s):
    y = np.exp(sig * t_v) * np.cos(omg * t_v)
    ax.plot(t_v, np.clip(y, -3, 3), color=cor, lw=1.6)
    ax.set_title(titulo, fontsize=7)
    ax.set_xlabel("t", fontsize=7)
    ax.set_ylim(-3, 3)
    ax.spines[["right", "top"]].set_visible(False)
plt.tight_layout()
show_fig(fig1, 0.85)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 2 — TABELA
# ═══════════════════════════════════════════════════════════════════════════════
st.header("2. Tabela de Transformadas de Laplace")

st.markdown(r"""
Pares fundamentais (transformada unilateral, $t \geq 0$, $a > 0$, $\omega > 0$):

| $x(t)$ | $X(s)$ |
|:---|:---|
| $\delta(t)$ | $1$ |
| $u(t)$ | $\dfrac{1}{s}$ |
| $t\,u(t)$ | $\dfrac{1}{s^2}$ |
| $t^n u(t)$ | $\dfrac{n!}{s^{n+1}}$ |
| $e^{-at}u(t)$ | $\dfrac{1}{s+a}$ |
| $t\,e^{-at}u(t)$ | $\dfrac{1}{(s+a)^2}$ |
| $t^{n-1}e^{-at}u(t)$ | $\dfrac{(n-1)!}{(s+a)^n}$ |
| $\sin(\omega t)\,u(t)$ | $\dfrac{\omega}{s^2+\omega^2}$ |
| $\cos(\omega t)\,u(t)$ | $\dfrac{s}{s^2+\omega^2}$ |
| $e^{-at}\sin(\omega t)\,u(t)$ | $\dfrac{\omega}{(s+a)^2+\omega^2}$ |
| $e^{-at}\cos(\omega t)\,u(t)$ | $\dfrac{s+a}{(s+a)^2+\omega^2}$ |

> O par $t^{n-1}e^{-at}u(t)$ é fundamental para inverter frações com pólos repetidos (§12).
""")

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 3 — PROPRIEDADES
# ═══════════════════════════════════════════════════════════════════════════════
st.header("3. Propriedades da Transformada de Laplace")

st.markdown(r"""
| Propriedade | Teorema |
|:---|:---|
| **Linearidade** | $\mathcal{L}[k_1 x_1+k_2 x_2] = k_1 X_1(s)+k_2 X_2(s)$ |
| **Deslocamento no tempo** | $\mathcal{L}[x(t-T)u(t-T)] = e^{-sT}X(s),\quad T>0$ |
| **Deslocamento na frequência** | $\mathcal{L}[e^{-at}x(t)] = X(s+a)$ |
| **Escalamento temporal** | $\mathcal{L}[x(at)] = \dfrac{1}{a}X\!\left(\dfrac{s}{a}\right),\quad a>0$ |
| **Derivação no tempo** | $\mathcal{L}\!\left[x^{(n)}(t)\right] = s^n X(s) - \displaystyle\sum_{k=0}^{n-1} s^{n-1-k}\,x^{(k)}(0^-)$ |
| **Integração no tempo** | $\mathcal{L}\!\left[\int_0^t x(\tau)\,d\tau\right] = \dfrac{X(s)}{s}$ |
| **Valor inicial** | $x(0^+) = \lim_{s\to\infty} s\,X(s)$ |
| **Valor final** | $x(\infty) = \lim_{s\to 0} s\,X(s)$ |

> **Derivação com CI nulas:** se $x^{(k)}(0^-)=0$, então $\mathcal{L}[x^{(n)}] = s^n X(s)$ —
> propriedade que transforma EDOs em equações algébricas.

> **Condição do teorema do valor final:** $sX(s)$ deve ser analítica no semiplano direito
> e no eixo imaginário. Não se aplica a sinais que crescem ou oscilam em regime permanente.
""")

# Verificação gráfica: valor inicial e final
t_vi = np.linspace(0, 5, 500)
x_vi = 5 * (1 - np.exp(-2 * t_vi))

fig_vi, ax_vi = plt.subplots(figsize=(5.5, 2.8))
ax_vi.plot(t_vi, x_vi, color=COR["sinal"], lw=1.8, label=r"$x(t)=5(1-e^{-2t})$")
ax_vi.axhline(5, color=COR["natural"], ls="--", lw=1.2, label="valor final = 5")
ax_vi.axhline(0, color=COR["marginal"], ls=":", lw=1.2, label="valor inicial = 0")
ax_vi.set_title(r"Verificação: $X(s)=\dfrac{10}{s(s+2)}$ — teoremas de valor inicial e final",
                fontsize=8.5, fontweight="bold")
ax_vi.legend(fontsize=7)
estilo(ax_vi)
plt.tight_layout()
show_fig(fig_vi, 0.55)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 4 — CONVOLUÇÃO
# ═══════════════════════════════════════════════════════════════════════════════
st.header("4. Convolução")

st.markdown(r"""
A **convolução** de dois sinais mede a sobreposição acumulada entre eles conforme um desliza
sobre o outro:

$$(x_1 * x_2)(t) = \int_{-\infty}^{+\infty} x_1(\tau)\,x_2(t-\tau)\,d\tau$$

### 4.1 Convolução no Tempo → Multiplicação em $s$

$$x_1(t) * x_2(t) \;\overset{\mathcal{L}}{\longleftrightarrow}\; X_1(s)\cdot X_2(s)$$

Esta propriedade é central na análise de sistemas: a saída de um sistema **LCIT** é

$$y(t) = x(t)*h(t) \;\overset{\mathcal{L}}{\longleftrightarrow}\; Y(s) = X(s)\cdot H(s)$$

onde $h(t)$ é a resposta ao impulso e $H(s)$ é a função de transferência.

### 4.2 Multiplicação no Tempo → Convolução em $s$

$$x_1(t)\cdot x_2(t) \;\overset{\mathcal{L}}{\longleftrightarrow}\; \frac{1}{2\pi j}\,X_1(s) * X_2(s)$$
""")

# Convolução numérica de dois pulsos
h_c = 0.001
t_c = np.arange(0, 4, h_c)
x1_c = np.where((t_c >= 0) & (t_c <= 1), 1.0, 0.0)
x2_c = np.where((t_c >= 0) & (t_c <= 1), 1.0, 0.0)
conv_c = np.convolve(x1_c, x2_c, mode="full")[:len(t_c)] * h_c

fig_conv, axs_conv = plt.subplots(1, 3, figsize=(7.5, 2.4))
fig_conv.suptitle("Convolução de dois pulsos retangulares", fontsize=9, fontweight="bold")
for ax, y, lb, cor in zip(axs_conv,
    [x1_c, x2_c, conv_c],
    [r"$x_1(t)$", r"$x_2(t)$", r"$x_1(t)*x_2(t)$"],
    [COR["sinal"], COR["ref"], COR["saida"]]):
    ax.plot(t_c, y, color=cor, lw=1.6)
    ax.set_title(lb, fontsize=8.5)
    ax.set_xlim(0, 3.5)
    estilo(ax)
plt.tight_layout()
show_fig(fig_conv, 0.70)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 5 — FUNÇÃO DE TRANSFERÊNCIA
# ═══════════════════════════════════════════════════════════════════════════════
st.header("5. Função de Transferência")

st.markdown(r"""
A **função de transferência** $H(s)$ de um sistema **LCIT** é a Transformada de Laplace da
resposta ao impulso $h(t)$. Com condições iniciais nulas:

$$H(s) = \frac{Y(s)}{X(s)} = \mathcal{L}[h(t)]$$

### 5.1 Forma Geral — Pólos e Zeros

$$H(s) = \frac{N(s)}{D(s)} = \frac{b_m s^m + b_{m-1}s^{m-1} + \cdots + b_0}
{a_n s^n + a_{n-1}s^{n-1} + \cdots + a_0}, \qquad m \leq n$$

- **Pólos:** raízes de $D(s)$ — valores de $s$ onde $H(s) \to \infty$
- **Zeros:** raízes de $N(s)$ — valores de $s$ onde $H(s) = 0$
- A condição $m \leq n$ garante sistema **próprio** (fisicamente realizável)

### 5.2 Obtenção a partir de EDO

Dado o modelo diferencial com condições iniciais nulas:

$$a_n y^{(n)} + \cdots + a_0 y = b_m x^{(m)} + \cdots + b_0 x$$

Aplicando $\mathcal{L}$ (CI nulas):

$$(a_n s^n + \cdots + a_0)\,Y(s) = (b_m s^m + \cdots + b_0)\,X(s)$$

$$\therefore\quad H(s) = \frac{b_m s^m + \cdots + b_0}{a_n s^n + \cdots + a_0}$$

**Exemplo:** $\ddot{y} + 3\dot{y} + 2y = \dot{x} + x \;\Rightarrow\;
H(s) = \dfrac{s+1}{s^2+3s+2}$
""")

# Mapa de pólos e zeros
num_hs = [1, 1]; den_hs = [1, 3, 2]
zeros_hs = np.roots(num_hs); polos_hs = np.roots(den_hs)

fig_pz, ax_pz = plt.subplots(figsize=(4.0, 3.2))
ax_pz.axhline(0, color="k", lw=0.8); ax_pz.axvline(0, color="k", lw=0.8)
ax_pz.fill_betweenx([-3, 3], -5, 0, alpha=0.06, color=COR["polo_esq"], label="SPE (estável)")
ax_pz.fill_betweenx([-3, 3],  0, 5, alpha=0.06, color=COR["polo_dir"], label="SPD (instável)")
ax_pz.plot(zeros_hs.real, zeros_hs.imag, "bo", ms=8, label="Zeros")
ax_pz.plot(polos_hs.real, polos_hs.imag, "rx", ms=10, mew=2, label="Pólos")
ax_pz.set_xlim(-4, 1); ax_pz.set_ylim(-2, 2)
ax_pz.set_xlabel(r"$\sigma$", fontsize=8); ax_pz.set_ylabel(r"$j\omega$", fontsize=8)
ax_pz.set_title(r"Mapa de pólos e zeros — $H(s)=\dfrac{s+1}{s^2+3s+2}$",
                fontsize=8.5, fontweight="bold")
ax_pz.legend(fontsize=7); ax_pz.grid(True, alpha=0.3)
plt.tight_layout()
show_fig(fig_pz, 0.42)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 6 — ESTABILIDADE
# ═══════════════════════════════════════════════════════════════════════════════
st.header("6. Estabilidade via Função de Transferência")

st.markdown(r"""
A **estabilidade BIBO** (Bounded Input → Bounded Output) é determinada pela localização dos
pólos de $H(s)$ no plano complexo:

| Localização dos pólos de $H(s)$ | Estabilidade |
|:---|:---|
| Todos no **semiplano esquerdo** (SPE, $\text{Re}(s) < 0$) | **Assintoticamente estável** |
| Pelo menos um no **semiplano direito** (SPD, $\text{Re}(s) > 0$) | **Instável** |
| Pólos simples no eixo imaginário, demais no SPE | **Marginalmente estável** |
| Pólos repetidos no eixo imaginário, ou algum no SPD | **Instável** |

> A localização dos **zeros** não afeta a estabilidade BIBO.

> Para verificar a estabilidade sem calcular raízes, usa-se o **Critério de Routh-Hurwitz**,
> que determina o número de pólos no SPD a partir dos coeficientes de $D(s)$.
""")

t_est = np.linspace(0, 6, 2000)
sys_est6 = lti([6], [1, 3, 2])
_, y_est6 = sc_step(sys_est6, T=t_est)
y_marg6 = 1 - np.cos(t_est)
y_inst6 = np.where(t_est <= 5, np.exp(0.5 * t_est) - 1, np.nan)

fig_est6, axs_est6 = plt.subplots(1, 3, figsize=(8.0, 2.6))
fig_est6.suptitle("Estabilidade BIBO — resposta ao degrau", fontsize=9, fontweight="bold")
for ax, y, cor, titulo in zip(axs_est6,
    [y_est6, y_marg6, y_inst6],
    [COR["natural"], COR["marginal"], COR["instavel"]],
    ["Assintoticamente estável\n(todos pólos no SPE)",
     "Marginalmente estável\n(pólos simples em $j\\omega$)",
     "Instável\n(pólo no SPD)"]):
    ax.plot(t_est, y, color=cor, lw=1.6)
    ax.set_title(titulo, fontsize=7.5)
    estilo(ax)
plt.tight_layout()
show_fig(fig_est6, 0.75)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 7 — REALIZAÇÃO DE SISTEMAS
# ═══════════════════════════════════════════════════════════════════════════════
st.header("7. Realização de Sistemas")

st.markdown(r"""
**Realizar** $H(s)$ significa implementá-la com elementos físicos: **integradores** ($1/s$),
somadores e amplificadores. Uma realização é **canônica** se usa exatamente $n$ integradores,
onde $n$ é a ordem de $H(s)$.

### 7.1 Forma Direta

Separa $H(s)$ em dois blocos em cascata — $H_1$ trata apenas o denominador e $H_2$ apenas o numerador:

$$H(s) = \underbrace{\frac{1}{s^n + a_{n-1}s^{n-1}+\cdots+a_0}}_{H_1(s)} \cdot
\underbrace{\bigl(b_m s^m+\cdots+b_0\bigr)}_{H_2(s)}$$

### 7.2 Realização em Cascata

Fatora $H(s)$ em produto de subsistemas de 1ª (ou 2ª) ordem:

$$H(s) = H_1(s)\cdot H_2(s)\cdots H_n(s)$$

### 7.3 Realização em Paralelo

Expande $H(s)$ em frações parciais — cada termo é um subsistema de 1ª ordem:

$$H(s) = \frac{k_1}{s-\lambda_1}+\frac{k_2}{s-\lambda_2}+\cdots+\frac{k_n}{s-\lambda_n}$$

| Forma | Estrutura | Vantagem prática |
|:---|:---|:---|
| **Direta** | $H_1 \cdot H_2$ | Mínimo de integradores; estrutura compacta |
| **Cascata** | Produto de subsistemas | Ajuste de pólos individuais |
| **Paralelo** | Soma de subsistemas | Ajuste de resíduos (modos de resposta) |

### 7.4 Atraso de Transporte (Tempo Morto)

Um atraso puro $\theta$ não é racional em $s$: $e^{-\theta s}$. A **aproximação de Padé** de 2ª ordem:

$$e^{-\theta s} \approx \frac{1 - \frac{\theta}{2}s + \frac{\theta^2}{8}s^2}
{1 + \frac{\theta}{2}s + \frac{\theta^2}{8}s^2}$$

### 7.5 Exemplo Numérico

$$H(s) = \frac{s+3}{(s+1)(s+2)} = \frac{s+3}{s^2+3s+2}$$

**Paralelo (frações parciais):** $H(s) = \dfrac{2}{s+1} - \dfrac{1}{s+2}
\;\Rightarrow\; h(t) = 2\,e^{-t} - e^{-2t},\; t\geq 0$
""")

# Diagramas de realização
fig_real7, axs_d = plt.subplots(3, 1, figsize=(8.5, 6.5))
fig_real7.suptitle(r"Formas de Realização de $H(s)$", fontsize=10, fontweight="bold")

# Forma Direta
ax = axs_d[0]; ax.set_xlim(0, 11); ax.set_ylim(-0.7, 0.8); ax.axis("off")
ax.set_title(r"Forma Direta: $H(s)=H_1(s)\cdot H_2(s)$", fontsize=8.5, fontweight="bold")
ax.text(0.4, 0, "$X(s)$", ha="center", va="center", fontsize=9)
_arr(ax, 0.8, 0, 2.2, 0); _blk(ax, 3.2, 0, 2.0, 0.46, r"$H_1(s)=\dfrac{1}{D(s)}$")
_arr(ax, 4.2, 0, 5.6, 0, "$W(s)$", ldy=0.13); _blk(ax, 6.6, 0, 2.0, 0.46, r"$H_2(s)=N(s)$")
_arr(ax, 7.6, 0, 9.2, 0); ax.text(9.7, 0, "$Y(s)$", ha="center", va="center", fontsize=9)
ax.text(5.5, -0.58, r"Canônica: $N$ integradores $=$ ordem de $H(s)$",
        ha="center", fontsize=7.5, color="dimgray")

# Cascata
ax = axs_d[1]; ax.set_xlim(0, 11); ax.set_ylim(-0.6, 0.7); ax.axis("off")
ax.set_title(r"Cascata: $H(s)=H_1(s)\cdot H_2(s)\cdots H_n(s)$", fontsize=8.5, fontweight="bold")
ax.text(0.4, 0, "$X(s)$", ha="center", va="center", fontsize=9)
_arr(ax, 0.8, 0, 1.7, 0); _blk(ax, 2.5, 0, 1.5, 0.44, "$H_1(s)$")
_arr(ax, 3.25, 0, 4.25, 0); _blk(ax, 5.0, 0, 1.5, 0.44, "$H_2(s)$")
_arr(ax, 5.75, 0, 6.55, 0)
ax.text(7.1, 0, r"$\cdots$", ha="center", va="center", fontsize=14)
_arr(ax, 7.65, 0, 8.45, 0); _blk(ax, 9.2, 0, 1.5, 0.44, "$H_n(s)$")
_arr(ax, 9.95, 0, 10.7, 0); ax.text(10.95, 0, "$Y(s)$", ha="center", va="center", fontsize=9)

# Paralelo
ax = axs_d[2]; ax.set_aspect("equal")
ax.set_xlim(-0.5, 11.5); ax.set_ylim(-1.9, 2.1); ax.axis("off")
ax.set_title(r"Paralelo: $H(s)=H_1(s)+H_2(s)+\cdots+H_n(s)$", fontsize=8.5, fontweight="bold")
ax.text(-0.2, 0, "$X(s)$", ha="center", va="center", fontsize=9)
_lin(ax, 0.3, 0, 1.2, 0); _dot(ax, 1.2, 0)
for y_r, lb_p in zip([1.1, 0.0, -1.1], ["$H_1(s)$", "$H_2(s)$", "$H_n(s)$"]):
    _lin(ax, 1.2, 0, 1.2, y_r); _arr(ax, 1.2, y_r, 4.4, y_r)
    _blk(ax, 5.5, y_r, 2.2, 0.44, lb_p); _lin(ax, 6.6, y_r, 9.2, y_r)
ax.text(1.2, -0.55, r"$\vdots$", ha="center", va="center", fontsize=13)
ax.text(9.2, -0.55, r"$\vdots$", ha="center", va="center", fontsize=13)
_lin(ax, 9.2, 1.1, 9.2, -1.1); _dot(ax, 9.2, 0)
_som(ax, 10.3, 0); _lin(ax, 9.2, 0, 10.08, 0); _arr(ax, 10.52, 0, 11.2, 0)
ax.text(11.4, 0, "$Y(s)$", ha="center", va="center", fontsize=9)
plt.tight_layout()
show_fig(fig_real7, 0.80)

# Resposta ao degrau
t_r7 = np.linspace(0, 8, 800)
_, y_r7 = sc_step(lti([1, 3], [1, 3, 2]), T=t_r7)
fig_r7, ax_r7 = plt.subplots(figsize=(5.5, 2.6))
ax_r7.plot(t_r7, y_r7, color=COR["sinal"], lw=2,
           label=r"$H(s)=(s+3)/[(s+1)(s+2)]$")
ax_r7.axhline(y_r7[-1], color="k", lw=0.8, ls=":",
              label=f"Valor final = {y_r7[-1]:.2f}")
ax_r7.set_title("Verificação: resposta ao degrau", fontsize=8.5, fontweight="bold")
ax_r7.legend(fontsize=7)
estilo(ax_r7)
plt.tight_layout()
show_fig(fig_r7, 0.55)

# Padé
st.markdown("### 7.4 Atraso de transporte: exato vs. aproximação de Padé")
theta = 0.5
t_p = np.linspace(0, 6, 2000)
y_exato = np.where(t_p >= theta, 1 - np.exp(-(t_p - theta)), 0.0)
th = theta
num_pade = [0.125*th**2, -0.5*th, 1]
den_g    = [1, 1]
den_pade = [0.125*th**2,  0.5*th, 1]
num_total = np.convolve(num_pade, [1])
den_total = np.convolve(den_g, den_pade)
_, y_pade = sc_step(lti(num_total, den_total), T=t_p)

fig_pade, ax_pade = plt.subplots(figsize=(5.5, 2.8))
ax_pade.plot(t_p, y_exato, color=COR["sinal"],  lw=1.8, label="Exato (deslocamento temporal)")
ax_pade.plot(t_p, y_pade,  color=COR["saida"],  lw=1.8, ls="--", label=f"Padé 2ª ordem (θ={th})")
ax_pade.axvline(theta, color="gray", ls=":", lw=1, label=f"t = θ = {theta} s")
ax_pade.set_title(f"Atraso de transporte θ={theta} s — $H(s)=1/(s+1)$",
                  fontsize=8.5, fontweight="bold")
ax_pade.legend(fontsize=7)
estilo(ax_pade)
plt.tight_layout()
show_fig(fig_pade, 0.55)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 8 — SISTEMAS NÃO-LINEARES
# ═══════════════════════════════════════════════════════════════════════════════
st.header("8. Sistemas Não-Lineares e Linearização")

st.markdown(r"""
Sistemas reais frequentemente apresentam **não-linearidades** que violam o princípio da
superposição e impedem o uso direto da Transformada de Laplace. A estratégia usual é
**linearizar** o modelo em torno de um ponto de operação.

### 8.1 Classificação das Não-Linearidades

**Por magnitude** (a saída depende não-linearmente da amplitude da entrada):

| Tipo | Comportamento | Ocorrência típica |
|:---|:---|:---|
| **Saturação** | Ganho cai a zero além de um limite | Amplificadores, atuadores |
| **Zona morta** | Sem resposta abaixo de um limiar | Válvulas, atuadores pneumáticos |
| **Relé** | Saída binária $\pm M$ | Controladores on/off |
| **Atrito** | Força de partida > força de deslizamento | Sistemas mecânicos |
| **Folga** (*backlash*) | Histerese por folga mecânica | Engrenagens, acoplamentos |
| **Histerese** | Dependência do histórico da entrada | Materiais magnéticos, relés |

**Por frequência** (o sistema gera ou distorce frequências):

| Tipo | Comportamento |
|:---|:---|
| **Ciclo limite** | Oscilação auto-sustentada de amplitude e período fixos |
| **Salto em ressonância** | Resposta em frequência com histerese (Duffing) |
| **Batimento** | Modulação por dois sinais de frequências próximas |
| **Arrasto** | Amortecimento proporcional ao quadrado da velocidade |
| **Harmônicas** | Resposta contém múltiplos inteiros da frequência de excitação |
| **Caos** | Comportamento irregular sensível a condições iniciais |
""")

# ── Não-linearidades de magnitude ────────────────────────────────────────────
u_nl = np.linspace(-3, 3, 800)
sat  = np.clip(u_nl, -1, 1)
dz   = 0.6
dead = np.where(np.abs(u_nl) <= dz, 0.0, u_nl - dz * np.sign(u_nl))
rele = np.sign(u_nl)
hist = 0.5
rele_hist = np.zeros_like(u_nl); estado = 0
for j, uj in enumerate(u_nl):
    if uj >  hist: estado =  1
    if uj < -hist: estado = -1
    rele_hist[j] = estado
atrito = np.where(np.abs(u_nl) < 1e-3, 0.0,
         np.where(np.abs(u_nl) < 0.12, 1.2 * np.sign(u_nl), 0.6 * np.sign(u_nl)))
dq_nl = 0.5; quant = dq_nl * np.round(u_nl / dq_nl)
Hc_h = 1.0; Bs_h = 1.0
u_up = u_nl; u_dn = u_nl[::-1]
y_up_h = Bs_h * np.tanh((u_up - (-Hc_h)) / 0.6)
y_dn_h = Bs_h * np.tanh((u_dn -   Hc_h ) / 0.6)
Br_h   = float(Bs_h * np.tanh(Hc_h / 0.6))
bl_f   = 0.5
u_fl   = np.linspace(-3, 3, 1200); y_fl = np.zeros_like(u_fl)
for j in range(1, len(u_fl)):
    du = u_fl[j] - u_fl[j-1]
    if du > 0: y_fl[j] = max(y_fl[j-1], u_fl[j] - bl_f)
    else:       y_fl[j] = min(y_fl[j-1], u_fl[j] + bl_f)

casos_nl = [
    (sat,       "Saturação",           r"Linear até $|u|=1$; constante fora",          COR["sinal"]),
    (dead,      "Zona Morta",          r"Sem resposta para $|u|\leq 0{,}6$",            COR["saida"]),
    (rele,      "Relé (on/off)",       r"Saída $\pm1$ conforme sinal",                 COR["marginal"]),
    (rele_hist, "Relé c/ Histerese",   r"Comuta somente ao cruzar $\pm 0{,}5$",        COR["natural"]),
    (atrito,    "Atrito",              r"Força partida > deslizamento",                 COR["ref"]),
    (quant,     "Quantizador",         r"Arredonda para múltiplos de $\Delta=0{,}5$",  "purple"),
    (None,      "Histerese (B-H)",     r"Remanência $B_r$, coercividade $H_c$",        "saddlebrown"),
    ("folga",   "Folga (Backlash)",    r"Semi-largura $b=0{,}5$",                      "purple"),
]

fig_nl, axs_nl = plt.subplots(3, 3, figsize=(9.5, 7.5))
fig_nl.suptitle("Não-linearidades de magnitude", fontsize=10, fontweight="bold")
for ax, (y, titulo, subtit, cor) in zip(axs_nl.flat, casos_nl):
    if isinstance(y, str) and y == "folga":
        ax.plot(u_fl, y_fl, color=cor, lw=2)
        ax.plot(u_fl, u_fl, color="k", lw=0.8, ls="--", alpha=0.4, label="linear")
        ax.set_xlabel("Entrada $u$", fontsize=7); ax.set_ylabel("Saída $y$", fontsize=7)
        ax.legend(fontsize=6)
    elif y is None:
        ax.plot(u_up, y_up_h, color=cor, lw=2, label="subida →")
        ax.plot(u_dn, y_dn_h, color="darkred", lw=2, ls="--", label="descida ←")
        ax.plot(0, Br_h, "o", color=cor, ms=5, zorder=5)
        ax.plot(Hc_h, 0, "o", color="darkred", ms=5, zorder=5)
        ax.annotate(f"$B_r={Br_h:.2f}$", xy=(0, Br_h), xytext=(-1.8, 0.55),
                    arrowprops=dict(arrowstyle="->", color=cor, lw=1), fontsize=6, color=cor)
        ax.annotate(f"$H_c={Hc_h:.1f}$", xy=(Hc_h, 0), xytext=(1.3, -0.35),
                    arrowprops=dict(arrowstyle="->", color="darkred", lw=1), fontsize=6, color="darkred")
        ax.legend(fontsize=6)
        ax.set_xlabel("Campo $H$", fontsize=7); ax.set_ylabel("Indução $B$", fontsize=7)
    else:
        ax.plot(u_nl, y, color=cor, lw=2)
        ax.set_xlabel("Entrada $u$", fontsize=7); ax.set_ylabel("Saída $y$", fontsize=7)
    ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5)
    ax.set_title(titulo, fontsize=8.5, fontweight="bold")
    ax.text(0.97, 0.05, subtit, transform=ax.transAxes,
            fontsize=6.5, ha="right", va="bottom", color="dimgray")
    ax.spines[["right", "top"]].set_visible(False)
for ax_empty in axs_nl.flat[len(casos_nl):]:
    ax_empty.axis("off")
plt.tight_layout()
show_fig(fig_nl, 0.85)

# ── Não-linearidades de frequência ───────────────────────────────────────────
st.markdown("### 8.2 Não-linearidades de frequência — fenômenos dinâmicos")

@st.cache_data(show_spinner="Calculando fenômenos dinâmicos…")
def calc_freq_nonlin():
    def lorenz(t, y, sig=10, r=28, b=8/3):
        x, yd, z = y
        return [sig*(yd-x), x*(r-z)-yd, x*yd-b*z]
    sol_l = solve_ivp(lorenz, [0, 40], [1, 1, 1],
                      dense_output=True, rtol=1e-8, atol=1e-10)
    t_l = np.linspace(0, 40, 8000)
    xyz = sol_l.sol(t_l)

    t_b = np.linspace(0, 6*np.pi, 3000)
    w1, w2 = 10.0, 10.8
    y_bat = np.sin(w1*t_b) + np.sin(w2*t_b)
    env_b = 2*np.abs(np.cos((w2-w1)/2*t_b))

    def arrasto(t, y, c=0.5):
        x, xd = y
        return [xd, np.sin(t) - c*np.abs(xd)*xd - x]
    t_drag = np.linspace(0, 60, 6000)
    sol_d = solve_ivp(arrasto, [0, 60], [0, 0], t_eval=t_drag, rtol=1e-7)

    def duffing(t, y, gam=0.15, eps=0.3, F=0.5, Om=1.0):
        x, xd = y
        return [xd, F*np.cos(Om*t) - gam*xd - x - eps*x**3]
    omegas = np.linspace(0.4, 1.8, 80)
    amps_up, amps_dn = [], []
    x0d = [0.0, 0.0]
    for Om in omegas:
        s_ = solve_ivp(duffing, [0, 200], x0d, args=(0.15,0.3,0.5,Om),
                       dense_output=True, rtol=1e-7)
        t_ss = np.linspace(180, 200, 800)
        amps_up.append(np.max(np.abs(s_.sol(t_ss)[0])))
        x0d = list(s_.sol(200))
    x0d = [2.0, 0.0]
    for Om in omegas[::-1]:
        s_ = solve_ivp(duffing, [0, 200], x0d, args=(0.15,0.3,0.5,Om),
                       dense_output=True, rtol=1e-7)
        t_ss = np.linspace(180, 200, 800)
        amps_dn.insert(0, np.max(np.abs(s_.sol(t_ss)[0])))
        x0d = list(s_.sol(200))

    def vdp(t, y, mu=1.0):
        x, xd = y
        return [xd, mu*(1 - x**2)*xd - x]
    sol_v = solve_ivp(vdp, [0, 40], [0.1, 0],
                      t_eval=np.linspace(0, 40, 4000), rtol=1e-7)

    t_f = np.linspace(0, 4*np.pi, 2000)
    u_f = np.sin(t_f); bl = 0.4; y_f = np.zeros_like(u_f)
    for j in range(1, len(u_f)):
        if u_f[j] - u_f[j-1] > 0: y_f[j] = max(y_f[j-1], u_f[j] - bl)
        else:                        y_f[j] = min(y_f[j-1], u_f[j] + bl)

    freqs = np.linspace(0.05, 3.0, 1000)
    def H_mag(w, zeta=0.1, wn=1.0):
        return 1.0 / np.sqrt((1-(w/wn)**2)**2 + (2*zeta*(w/wn))**2)

    return (xyz, t_l, t_b, y_bat, env_b, sol_d, t_drag,
            omegas, amps_up, amps_dn, sol_v, t_f, u_f, y_f, bl, freqs, H_mag)

(xyz, t_l, t_b, y_bat, env_b, sol_d, t_drag,
 omegas, amps_up, amps_dn, sol_v, t_f, u_f, y_f, bl, freqs, H_mag) = calc_freq_nonlin()

fig_freq, axs_freq = plt.subplots(4, 2, figsize=(10.5, 12))
fig_freq.suptitle("Não-linearidades de frequência — fenômenos dinâmicos",
                  fontsize=10, fontweight="bold")

ax = axs_freq[0, 0]
ax.plot(xyz[0], xyz[2], lw=0.4, color=COR["sinal"], alpha=0.85)
ax.set_title(r"Caos — Atrator de Lorenz""\n"
             r"$\dot{x}=\sigma(y-x),\;\dot{y}=x(r-z)-y,\;\dot{z}=xy-bz$",
             fontsize=8, fontweight="bold")
ax.set_xlabel("x", fontsize=7); ax.set_ylabel("z", fontsize=7)
ax.spines[["right", "top"]].set_visible(False)

ax = axs_freq[0, 1]
ax.plot(t_b, y_bat, lw=0.7, color=COR["sinal"], label="sinal")
ax.plot(t_b,  env_b, lw=1.6, color=COR["saida"], ls="--", label="envelope")
ax.plot(t_b, -env_b, lw=1.6, color=COR["saida"], ls="--")
ax.set_title(r"Batimento — $\sin(\omega_1 t)+\sin(\omega_2 t)$,"
             r" $\omega_1{=}10,\,\omega_2{=}10{,}8$", fontsize=8, fontweight="bold")
ax.set_xlabel("t (s)", fontsize=7); ax.set_ylabel("Amplitude", fontsize=7)
ax.legend(fontsize=6); ax.spines[["right", "top"]].set_visible(False)

ax = axs_freq[1, 0]
ax.plot(sol_d.t[-3000:], sol_d.y[0, -3000:], lw=1.2, color=COR["natural"])
ax.set_title(r"Arrasto — $\ddot{x}+c|\dot{x}|\dot{x}+x=\sin t$, $c=0{,}5$",
             fontsize=8, fontweight="bold")
ax.set_xlabel("t (s)", fontsize=7); ax.set_ylabel("x(t)", fontsize=7)
ax.spines[["right", "top"]].set_visible(False)

ax = axs_freq[1, 1]
ax.plot(omegas, amps_up, color=COR["sinal"],  lw=1.6, label=r"varredura $\uparrow$")
ax.plot(omegas, amps_dn, color=COR["saida"],  lw=1.6, ls="--", label=r"varredura $\downarrow$")
ax.set_title("Salto em Ressonância — Duffing\n"
             r"$\ddot{x}+\gamma\dot{x}+x+\varepsilon x^3=F\cos(\Omega t)$",
             fontsize=8, fontweight="bold")
ax.set_xlabel(r"$\Omega$", fontsize=7); ax.set_ylabel("Amplitude estacionária", fontsize=7)
ax.legend(fontsize=6); ax.spines[["right", "top"]].set_visible(False)

ax = axs_freq[2, 0]
ax.plot(sol_v.y[0], sol_v.y[1], lw=1, color=COR["marginal"])
ax.set_title(r"Ciclo Limite — Van der Pol ($\mu=1$)""\n"
             r"$\ddot{x}-\mu(1-x^2)\dot{x}+x=0$", fontsize=8, fontweight="bold")
ax.set_xlabel("x", fontsize=7); ax.set_ylabel(r"$\dot{x}$", fontsize=7)
ax.spines[["right", "top"]].set_visible(False)

ax = axs_freq[2, 1]
ax.plot(u_f, y_f, lw=1.2, color="purple")
ax.plot([-1, 1], [-1, 1], lw=0.8, color="k", ls="--", alpha=0.4, label="linear ideal")
ax.set_title(f"Folga (Backlash, $b={bl}$)\n"
             r"Entrada $u=\sin t$; histerese de largura $2b$", fontsize=8, fontweight="bold")
ax.set_xlabel("Entrada $u$", fontsize=7); ax.set_ylabel("Saída $y$", fontsize=7)
ax.legend(fontsize=6); ax.spines[["right", "top"]].set_visible(False)

ax = axs_freq[3, 0]
cores_res = [COR["saida"], COR["marginal"], COR["natural"], COR["sinal"]]
for zeta, cor in zip([0.05, 0.15, 0.50, 1.0], cores_res):
    ax.plot(freqs, H_mag(freqs, zeta), lw=1.6, label=rf"$\zeta={zeta}$", color=cor)
ax.axvline(1, color="k", ls=":", lw=0.8, label=r"$\omega_n$")
ax.set_title(r"Ressonância — $|H(j\omega)|$ vs. frequência", fontsize=8, fontweight="bold")
ax.set_xlabel(r"$\omega/\omega_n$", fontsize=7); ax.set_ylabel("|H|", fontsize=7)
ax.set_ylim(0, 7); ax.legend(fontsize=6)
ax.spines[["right", "top"]].set_visible(False)

axs_freq[3, 1].axis("off")
plt.tight_layout()
show_fig(fig_freq, 0.88)

# ── Linearização de Taylor ────────────────────────────────────────────────────
st.markdown("### 8.3 Linearização pelo Método de Taylor")
st.markdown(r"""
Para pequenas variações $\delta x = x - x_0$ em torno do **ponto de equilíbrio** $x_0$,
a série de Taylor truncada na 1ª ordem fornece:

$$f(x) \approx f(x_0) + \underbrace{\left.\frac{df}{dx}\right|_{x_0}}_{m_a}\,(x - x_0)
\qquad\Rightarrow\qquad \delta f \approx m_a\,\delta x$$

O coeficiente $m_a$ é o **ganho linearizado** (inclinação local). Ordens superiores ampliam
a faixa de validade, conforme mostrado abaixo para $f(x) = \sqrt{x}$, $x_0 = 4$.
""")

Taylor_ordem = st.slider("Ordem da expansão de Taylor", 1, 5, 1)

x_sym_t = sp.Symbol("x")
f_sym_t = sp.sqrt(x_sym_t)
x0_t = 4.0
_cores_t = ["#e74c3c", "#e67e22", "#27ae60", "#8e44ad", "#2980b9"]

def taylor_serie_t(f, x, x0, ordem):
    serie = sp.Integer(0)
    for k in range(ordem + 1):
        dk = sp.diff(f, x, k).subs(x, x0)
        serie += dk / sp.factorial(k) * (x - x0)**k
    return serie

x_det_t  = np.linspace(2.5, 5.5, 300)
x_full_t = np.linspace(0.1, 9.0, 500)

fig_taylor, (ax_t1, ax_t2) = plt.subplots(2, 1, figsize=(5.5, 5.5))
fig_taylor.suptitle(r"Linearização por Taylor — $f(x)=\sqrt{x}$, $x_0=4$",
                    fontsize=9, fontweight="bold")

for ordem in range(1, Taylor_ordem + 1):
    t_expr = taylor_serie_t(f_sym_t, x_sym_t, x0_t, ordem)
    t_fn   = sp.lambdify(x_sym_t, t_expr, "numpy")
    cor    = _cores_t[ordem - 1]
    lbl    = f"Taylor {ordem}ª ordem"
    lw     = 2.0 if ordem == Taylor_ordem else 1.2
    alpha  = 1.0 if ordem == Taylor_ordem else 0.55
    ax_t1.plot(x_det_t,  np.clip(t_fn(x_det_t),  1.0, 3.5), color=cor, lw=lw, ls="--", alpha=alpha, label=lbl)
    ax_t2.plot(x_full_t, np.clip(t_fn(x_full_t), -0.5, 5.0), color=cor, lw=lw, ls="--", alpha=alpha, label=lbl)

for ax, xv, yv, xl, yl, tt in [
    (ax_t1, x_det_t,  np.sqrt(x_det_t),  [2.5, 5.5], [1.4, 2.6], r"Detalhe em torno de $x_0=4$"),
    (ax_t2, x_full_t, np.sqrt(x_full_t), [0.1, 9.0], [-0.3, 3.6], r"Intervalo amplo $x\in[0.1,\,9]$"),
]:
    ax.plot(xv, yv, color="black", lw=2.5, zorder=5, label=r"$f(x)=\sqrt{x}$")
    ax.plot(x0_t, np.sqrt(x0_t), "ko", ms=8, zorder=6, label=f"$x_0={x0_t}$")
    ax.set_title(tt, fontsize=8.5, fontweight="bold")
    ax.set_xlabel("x", fontsize=8); ax.set_ylabel("f(x)", fontsize=8)
    ax.set_xlim(xl); ax.set_ylim(yl)
    ax.legend(fontsize=7, loc="upper left")
    ax.grid(True, alpha=0.3); ax.spines[["right", "top"]].set_visible(False)
plt.tight_layout()
show_fig(fig_taylor, 0.52)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 9 — RESPOSTA NO DOMÍNIO DO TEMPO
# ═══════════════════════════════════════════════════════════════════════════════
st.header("9. Resposta no Domínio do Tempo")

st.markdown(r"""
A propriedade de derivação (§3) transforma a EDO em equação algébrica em $s$. A resposta total é:

$$y(t) = \underbrace{y_{en}(t)}_{\substack{\text{entrada nula} \\ \text{(condições iniciais)}}}
+ \underbrace{y_{ez}(t)}_{\substack{\text{estado nulo} \\ \text{(entrada aplicada)}}}$$

### 9.1 Procedimento

1. Aplicar $\mathcal{L}$ à EDO incluindo as condições iniciais $y^{(k)}(0^-)$.
2. Resolver algebricamente para $Y(s) = Y_{en}(s) + Y_{ez}(s)$.
3. Expandir em frações parciais (§10–12) e aplicar $\mathcal{L}^{-1}$ em cada termo.

### 9.2 Funções Próprias e Impróprias

| Condição | Classificação | Tratamento |
|:---|:---|:---|
| $\text{grau}(N) < \text{grau}(D)$ | **Própria** | Frações parciais diretamente |
| $\text{grau}(N) \geq \text{grau}(D)$ | **Imprópria** | Divisão polinomial primeiro |

Para funções impróprias: $F(s) = Q(s) + R(s)/D(s)$, onde $Q(s)$ corresponde a impulsos no tempo:

$$\mathcal{L}^{-1}[1] = \delta(t), \quad \mathcal{L}^{-1}[s] = \dot{\delta}(t),
\quad \mathcal{L}^{-1}[s^k] = \delta^{(k)}(t)$$

**Exemplo:** $F(s) = \dfrac{s^3+2s^2+6s+7}{s^2+s+5}$

Divisão: $F(s) = \underbrace{(s+1)}_{Q(s)} + \underbrace{\dfrac{2}{s^2+s+5}}_{R(s)/D(s)}$
""")

t_r9 = np.linspace(0, 6, 1000)
y_en9 = 2*np.exp(-t_r9) - np.exp(-2*t_r9)
y_ez9 = 0.5 - np.exp(-t_r9) + 0.5*np.exp(-2*t_r9)
y_tot9 = y_en9 + y_ez9

fig_r9, ax_r9 = plt.subplots(figsize=(6.0, 3.0))
ax_r9.plot(t_r9, y_en9,  color=COR["natural"],  ls="--", lw=1.4, label=r"$y_{en}(t)$ — entrada nula")
ax_r9.plot(t_r9, y_ez9,  color=COR["marginal"], ls=":",  lw=1.4, label=r"$y_{ez}(t)$ — estado nulo")
ax_r9.plot(t_r9, y_tot9, color=COR["sinal"],              lw=2.0, label=r"$y(t)$ — resposta total")
ax_r9.set_title(r"$\ddot{y}+3\dot{y}+2y=u(t)$, $y(0^-)=1$, $\dot{y}(0^-)=0$",
                fontsize=8.5, fontweight="bold")
ax_r9.legend(fontsize=7)
estilo(ax_r9)
plt.tight_layout()
show_fig(fig_r9, 0.60)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 10 — FRAÇÕES PARCIAIS: RAÍZES REAIS DISTINTAS
# ═══════════════════════════════════════════════════════════════════════════════
st.header("10. Frações Parciais — Raízes Reais Distintas")

st.markdown(r"""
Dada $F(s) = N(s)/D(s)$ **própria**, com $D(s)$ de raízes reais e distintas $-p_1, \ldots, -p_n$:

**Passo 1 — forma expandida:**

$$F(s) = \frac{k_1}{s+p_1} + \frac{k_2}{s+p_2} + \cdots + \frac{k_n}{s+p_n}$$

**Passo 2 — resíduo $k_m$ (método de Heaviside):**

$$k_m = \Bigl[(s+p_m)\,F(s)\Bigr]_{s=-p_m}$$

**Passo 3 — transformada inversa:**

$$f(t) = \bigl(k_1 e^{-p_1 t} + \cdots + k_n e^{-p_n t}\bigr)\,u(t)$$

> **Estabilidade:** se todos os $p_i > 0$, todos os pólos estão no SPE e $f(t) \to 0$.

---

### Exemplo 01 — $F_1(s) = \dfrac{6}{(s+1)(s+2)}$

$$k_1 = \left.\frac{6}{s+2}\right|_{s=-1} = 6 \qquad k_2 = \left.\frac{6}{s+1}\right|_{s=-2} = -6$$

$$\boxed{f_1(t) = \bigl(6\,e^{-t} - 6\,e^{-2t}\bigr)\,u(t)}$$

### Exemplo 02 — $F_2(s) = \dfrac{2(s+3)}{(s+1)(s+4)}$

$$k_1 = \left.\frac{2(s+3)}{s+4}\right|_{s=-1} = \frac{4}{3} \qquad k_2 = \left.\frac{2(s+3)}{s+1}\right|_{s=-4} = \frac{2}{3}$$

$$\boxed{f_2(t) = \left(\frac{4}{3}\,e^{-t}+\frac{2}{3}\,e^{-4t}\right)u(t)}$$

### Exemplo 03 — $F_3(s) = \dfrac{2(s-1)}{(s+1)(s+4)}$

$$k_1 = \left.\frac{2(s-1)}{s+4}\right|_{s=-1} = -\frac{4}{3} \qquad k_2 = \left.\frac{2(s-1)}{s+1}\right|_{s=-4} = \frac{10}{3}$$

$$\boxed{f_3(t) = \left(-\frac{4}{3}\,e^{-t}+\frac{10}{3}\,e^{-4t}\right)u(t)}$$
""")

t_fp = np.linspace(0, 6, 600)
y1_fp = 6*np.exp(-t_fp) - 6*np.exp(-2*t_fp)
y2_fp = (4/3)*np.exp(-t_fp) + (2/3)*np.exp(-4*t_fp)
y3_fp = (-4/3)*np.exp(-t_fp) + (10/3)*np.exp(-4*t_fp)

fig_fp, axs_fp = plt.subplots(1, 3, figsize=(8.5, 2.8))
fig_fp.suptitle("Exemplos 01–03 — raízes reais distintas", fontsize=9, fontweight="bold")
for ax, (y, lbl, cor) in zip(axs_fp, [
    (y1_fp, r"$f_1(t)=6e^{-t}-6e^{-2t}$",          COR["sinal"]),
    (y2_fp, r"$f_2=(4/3)e^{-t}+(2/3)e^{-4t}$",      COR["natural"]),
    (y3_fp, r"$f_3=(-4/3)e^{-t}+(10/3)e^{-4t}$",    COR["saida"]),
]):
    ax.plot(t_fp, y, color=cor, lw=2)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_title(lbl, fontsize=8)
    estilo(ax)
plt.tight_layout()
show_fig(fig_fp, 0.78)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 11 — FRAÇÕES PARCIAIS: RAÍZES COMPLEXAS
# ═══════════════════════════════════════════════════════════════════════════════
st.header("11. Frações Parciais — Raízes Complexas Conjugadas")

st.markdown(r"""
Quando $D(s)$ contém o fator irredutível $s^2 + as + b$ com $a^2 < 4b$, as raízes são complexas:

$$p_{1,2} = -\sigma \pm j\omega_d, \qquad \sigma = \frac{a}{2} > 0,
\qquad \omega_d = \frac{\sqrt{4b-a^2}}{2} > 0$$

**Passo 1 — forma expandida** (resíduos sempre conjugados $k$, $\bar{k}$):

$$k = \Bigl[(s+\sigma-j\omega_d)\,F(s)\Bigr]_{s=-\sigma+j\omega_d}$$

**Passo 2 — forma direta** (recomendada — evita aritmética complexa):

$$\frac{A(s+\sigma) + B\omega_d}{(s+\sigma)^2+\omega_d^2}
\;\xrightarrow{\mathcal{L}^{-1}}\;
e^{-\sigma t}\bigl(A\cos\omega_d t + B\sin\omega_d t\bigr)\,u(t)$$

---

### Exemplo 04 — $F_4(s) = \dfrac{3}{s^2+2s+5}$

Pólos: $s = -1 \pm j2$ ($\sigma=1$, $\omega_d=2$)

$$F_4(s) = \frac{3}{(s+1)^2+4} = \frac{3}{2}\cdot\frac{2}{(s+1)^2+2^2}$$

$$\boxed{f_4(t) = \tfrac{3}{2}\,e^{-t}\sin(2t)\,u(t)}$$

### Exemplo 05 — $F_5(s) = \dfrac{2s+6}{s^2+2s+5}$

Mesmos pólos. Decompor numerador: $2s+6 = A(s+1)+B\cdot2 \Rightarrow A=2,\; B=2$

$$F_5(s) = 2\cdot\frac{s+1}{(s+1)^2+4} + 2\cdot\frac{2}{(s+1)^2+4}$$

$$\boxed{f_5(t) = 2\,e^{-t}\cos(2t)\,u(t) + 2\,e^{-t}\sin(2t)\,u(t)
= 2\sqrt{2}\,e^{-t}\cos\!\left(2t-\tfrac{\pi}{4}\right)u(t)}$$
""")

t_fc = np.linspace(0, 6, 600)
y4_fc = 1.5*np.exp(-t_fc)*np.sin(2*t_fc)
env4  = 1.5*np.exp(-t_fc)
y5_fc = 2*np.exp(-t_fc)*(np.cos(2*t_fc)+np.sin(2*t_fc))
env5  = 2*np.sqrt(2)*np.exp(-t_fc)

fig_fc, axs_fc = plt.subplots(1, 2, figsize=(8.5, 3.0))
fig_fc.suptitle(r"Exemplos 04–05 — raízes complexas $(s+1)^2+4$",
                fontsize=9, fontweight="bold")

ax = axs_fc[0]
ax.plot(t_fc, y4_fc, color=COR["sinal"], lw=2, label=r"$f_4(t)$")
ax.plot(t_fc,  env4, color=COR["natural"], lw=1.2, ls="--", label=r"envelope $(3/2)e^{-t}$")
ax.plot(t_fc, -env4, color=COR["natural"], lw=1.2, ls="--")
ax.set_title(r"$f_4(t)=\frac{3}{2}\,e^{-t}\sin(2t)$", fontsize=8.5)
ax.legend(fontsize=7); estilo(ax)

ax = axs_fc[1]
ax.plot(t_fc, y5_fc, color=COR["saida"], lw=2, label=r"$f_5(t)$")
ax.plot(t_fc,  env5, color=COR["natural"], lw=1.2, ls="--", label=r"envelope $2\sqrt{2}\,e^{-t}$")
ax.plot(t_fc, -env5, color=COR["natural"], lw=1.2, ls="--")
ax.set_title(r"$f_5(t)=2e^{-t}[\cos(2t)+\sin(2t)]$", fontsize=8.5)
ax.legend(fontsize=7); estilo(ax)

plt.tight_layout()
show_fig(fig_fc, 0.78)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 12 — FRAÇÕES PARCIAIS: RAÍZES REPETIDAS
# ═══════════════════════════════════════════════════════════════════════════════
st.header("12. Frações Parciais — Raízes Reais Repetidas")

st.markdown(r"""
Quando $D(s)$ contém o fator $(s+p_1)^r$ (raiz $-p_1$ com multiplicidade $r$):

$$F(s) = \underbrace{\frac{k_1}{(s+p_1)^r} + \frac{k_2}{(s+p_1)^{r-1}} + \cdots +
\frac{k_r}{s+p_1}}_{\text{bloco repetido}}
+ \underbrace{\frac{k_{r+1}}{s+p_2} + \cdots}_{\text{pólos simples}}$$

**Cálculo dos resíduos** — define-se $G(s) = F(s)\cdot(s+p_1)^r$:

$$k_i = \frac{1}{(i-1)!}\left.\frac{d^{\,i-1}\,G(s)}{ds^{\,i-1}}\right|_{s=-p_1},
\quad i = 1, 2, \ldots, r$$

**Transformada inversa** de cada termo:

$$\mathcal{L}^{-1}\!\left[\frac{k_i}{(s+p_1)^{r-i+1}}\right] =
k_i\,\frac{t^{r-i}}{(r-i)!}\,e^{-p_1 t}\,u(t)$$

> O bloco repetido gera termos do tipo $t^m e^{-p_1 t}$: mesmo com $p_1 > 0$, o sinal cresce
> inicialmente antes de decair.

---

### Exemplo 06 — $F_6(s) = \dfrac{2}{(s+1)(s+2)^2}$

$$F_6(s) = \frac{k_1}{s+1} + \frac{k_2}{(s+2)^2} + \frac{k_3}{s+2}$$

**$k_1$:** $\;\left.\dfrac{2}{(s+2)^2}\right|_{s=-1} = 2$

**$G(s) = \dfrac{2}{s+1}$:** $\;k_2 = G(-2) = -2$, $\;k_3 = G'(-2) = -2$

$$\boxed{f_6(t) = \bigl(2\,e^{-t} - 2\,t\,e^{-2t} - 2\,e^{-2t}\bigr)\,u(t)}$$
""")

t_fr = np.linspace(0, 6, 600)
y_k1r = 2*np.exp(-t_fr)
y_k2r = -2*t_fr*np.exp(-2*t_fr)
y_k3r = -2*np.exp(-2*t_fr)
y6_fr = y_k1r + y_k2r + y_k3r

fig_fr, axs_fr = plt.subplots(1, 2, figsize=(8.5, 3.0))
fig_fr.suptitle("Exemplo 06 — raiz repetida: decomposição dos termos",
                fontsize=9, fontweight="bold")

ax = axs_fr[0]
ax.plot(t_fr, y_k1r, color=COR["natural"],  lw=1.4, ls="--", label=r"$2\,e^{-t}$")
ax.plot(t_fr, y_k2r, color=COR["marginal"], lw=1.4, ls=":",  label=r"$-2t\,e^{-2t}$")
ax.plot(t_fr, y_k3r, color=COR["saida"],    lw=1.4, ls="-.", label=r"$-2\,e^{-2t}$")
ax.plot(t_fr, y6_fr, color=COR["sinal"],    lw=2.2,           label=r"$f_6(t)$ total")
ax.axhline(0, color="k", lw=0.5)
ax.legend(fontsize=7); estilo(ax)

ax = axs_fr[1]
ax.plot(t_fr, y6_fr, color=COR["sinal"], lw=2)
ax.axhline(0, color="k", lw=0.5)
ax.set_title(r"$f_6(t)=2e^{-t}-2t\,e^{-2t}-2e^{-2t}$", fontsize=8.5)
estilo(ax)

plt.tight_layout()
show_fig(fig_fr, 0.78)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 13 — REFERÊNCIAS
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("13. Referências", expanded=False):
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
    "Transformada de Laplace &nbsp;·&nbsp; Modelagem e Sistemas Lineares"
    " &nbsp;·&nbsp; Engenharia de Energia &nbsp;·&nbsp; CNAT — IFRN<br>"
    "Autor: Marcus V A Fernandes &nbsp;·&nbsp; marcus.fernandes@ifrn.edu.br"
    " &nbsp;·&nbsp; v1.0"
    "</div>",
    unsafe_allow_html=True,
)
