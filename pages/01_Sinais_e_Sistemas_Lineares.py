import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(page_title="Sinais e Sistemas Lineares", page_icon="📡", layout="wide")
st.title("📡 Sinais e Sistemas Lineares")
st.caption("Modelagem e Sistemas Lineares · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

# ── ÍNDICE ────────────────────────────────────────────────────────────────────
with st.expander("📋 Índice", expanded=False):
    st.markdown("""
1. Definições Fundamentais
2. Tamanho de um Sinal
3. Natureza, Periodicidade e Causalidade
4. Operações sobre Sinais
5. Funções Pares e Ímpares
6. Funções Singulares
7. Funções Exponenciais
8. Sistemas — Definições e Classificação
9. Princípio da Superposição
10. Estabilidade
11. Sistemas de Controle
12. Diagramas de Blocos e Álgebra
13. Especificações de Desempenho
""")

# ── SEÇÃO 1 ───────────────────────────────────────────────────────────────────
st.markdown("## 1. Definições Fundamentais")
st.markdown(r"""
Um **sinal** é uma representação de dados ou informação. Os sinais são processados por **sistemas**, que os modificam ou extraem informações.

Um **sistema** transforma sinais de **entrada** em sinais de **saída**:

$$x_1(t),\ldots,x_j(t) \;\xrightarrow{\text{Sistema}}\; y_1(t),\ldots,y_k(t)$$

Sistemas com múltiplas entradas e saídas são chamados **MIMO** (*Multiple-Input Multiple-Output*); com uma entrada e uma saída, **SISO**.
""")

# ── SEÇÃO 2 ───────────────────────────────────────────────────────────────────
st.markdown("## 2. Tamanho de um Sinal")
st.markdown(r"""
### 2.1 Energia
Sinais que **tendem a zero** quando $t \to \pm\infty$ possuem energia finita:

$$E_x = \int_{-\infty}^{+\infty} |x(t)|^2 \, dt < \infty$$

### 2.2 Potência
Sinais que **persistem no tempo** possuem potência média finita:

$$P_x = \lim_{T \to \infty} \frac{1}{T} \int_{-T/2}^{+T/2} |x(t)|^2 \, dt < \infty$$

> **Nota:** um sinal não pode ser simultaneamente de energia e de potência. Sinais periódicos são de potência ($E_x = \infty$, $P_x < \infty$); pulsos isolados são de energia ($E_x < \infty$, $P_x = 0$).
""")

# ── SEÇÃO 3 ───────────────────────────────────────────────────────────────────
st.markdown("## 3. Natureza, Periodicidade e Causalidade")
st.markdown(r"""
### 3.1 Natureza do Sinal

| | **Analógico** (amplitude contínua) | **Digital** (amplitude quantizada) |
|---|---|---|
| **Contínuo** ($t \in \mathbb{R}$) | $x(t)$: grandeza física | $x(t)$: onda quadrada |
| **Discreto** ($n \in \mathbb{Z}$) | $x[n]$: amostras reais | $x[n]$: sequência de bits |

### 3.2 Periodicidade
Um sinal é **periódico** se existe $T_0 > 0$ tal que:

$$x(t) = x(t + T_0), \quad \forall\, t$$

### 3.3 Causalidade

| Tipo | Condição | Exemplo |
|---|---|---|
| **Causal** | $x(t) = 0$ para $t < 0$ | Resposta a uma excitação |
| **Não-causal** | $x(t) \neq 0$ para $t < 0$ | Sinal modelado matematicamente |
| **Anti-causal** | $x(t) = 0$ para $t \geq 0$ | Componente passada de um sistema |
""")

# ── SEÇÃO 4 ───────────────────────────────────────────────────────────────────
st.markdown("## 4. Operações sobre Sinais")
st.markdown(r"""
### 4.1 Deslocamento temporal
$$\phi(t) = x(t - t_0) \quad \Rightarrow \text{atraso se } t_0 > 0;\; \text{avanço se } t_0 < 0$$

### 4.2 Escalamento temporal
$$\phi(t) = x(at),\quad a > 1 \Rightarrow \text{compressão};\quad a < 1 \Rightarrow \text{expansão}$$

### 4.3 Reversão temporal
$$\phi(t) = x(-t) \quad \Rightarrow \text{espelhamento em } t=0$$
""")

# ── EXPLORADOR INTERATIVO — OPERAÇÕES SOBRE SINAIS ───────────────────────────
st.markdown("### 🎛️ Explorador de Operações sobre Sinais")

col1, col2 = st.columns([1, 2])
with col1:
    op = st.selectbox("Operação", ["Deslocamento temporal", "Escalamento temporal", "Reversão temporal"])
    if op == "Deslocamento temporal":
        t0 = st.slider("Atraso $t_0$", -4.0, 4.0, 1.5, 0.1)
    elif op == "Escalamento temporal":
        a = st.slider("Fator $a$", 0.25, 4.0, 2.0, 0.25)
    sinal = st.selectbox("Sinal base", ["Pulso retangular", "Rampa", "Senoide"])

t = np.linspace(-6, 6, 1000)

def make_signal(t, tipo):
    if tipo == "Pulso retangular":
        return ((t >= -1) & (t <= 1)).astype(float)
    elif tipo == "Rampa":
        return np.where(t >= 0, t * np.exp(-t), 0.0)
    else:
        return np.where(np.abs(t) <= 4, np.sin(2 * t) * np.exp(-0.2 * np.abs(t)), 0.0)

x_orig = make_signal(t, sinal)

if op == "Deslocamento temporal":
    x_mod = make_signal(t - t0, sinal)
    label_mod = f"x(t − {t0:.1f})"
elif op == "Escalamento temporal":
    x_mod = make_signal(a * t, sinal)
    label_mod = f"x({a:.2f}·t)"
else:
    x_mod = make_signal(-t, sinal)
    label_mod = "x(−t)"

with col2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=x_orig, name="x(t) original",
                             line=dict(color="#3d8ef0", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=t, y=x_mod, name=label_mod,
                             line=dict(color="#ef4444", width=2.5)))
    fig.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20),
                      legend=dict(orientation="h", y=1.1),
                      xaxis_title="t", yaxis_title="Amplitude")
    st.plotly_chart(fig, use_container_width=True)

# ── SEÇÃO 5 ───────────────────────────────────────────────────────────────────
st.markdown("## 5. Funções Pares e Ímpares")
st.markdown(r"""
Qualquer sinal real pode ser decomposto unicamente em partes par e ímpar:

$$x_e(t) = \frac{x(t)+x(-t)}{2} \quad\text{(parte par)}$$
$$x_o(t) = \frac{x(t)-x(-t)}{2} \quad\text{(parte ímpar)}$$

$$x(t) = x_e(t) + x_o(t)$$
""")

# ── SEÇÃO 6 ───────────────────────────────────────────────────────────────────
st.markdown("## 6. Funções Singulares")
st.markdown(r"""
### 6.1 Impulso unitário $\delta(t)$

$$\delta(t) = 0 \text{ para } t\neq 0, \qquad \int_{-\infty}^{+\infty}\delta(t)\,dt = 1$$

**Propriedade de amostragem:** $\displaystyle\int_{-\infty}^{+\infty} x(t)\,\delta(t-t_0)\,dt = x(t_0)$

### 6.2 Degrau unitário $u(t)$

$$u(t) = \begin{cases}1, & t > 0 \\ 0, & t < 0\end{cases}, \qquad u(t) = \int_{-\infty}^{t}\delta(\tau)\,d\tau$$

### 6.3 Rampa unitária $r(t)$

$$r(t) = t\,u(t) = \int_{-\infty}^{t}u(\tau)\,d\tau$$
""")

# ── SEÇÃO 7 ───────────────────────────────────────────────────────────────────
st.markdown("## 7. Funções Exponenciais")
st.markdown(r"""
A exponencial complexa $e^{st}$ com $s = \sigma + j\omega$ é o sinal fundamental da análise de sistemas:

| $\sigma$ | $\omega$ | Comportamento |
|---|---|---|
| $< 0$ | $0$ | Decaimento exponencial puro |
| $> 0$ | $0$ | Crescimento exponencial puro |
| $0$ | $\neq 0$ | Senoide pura (sem amortecimento) |
| $< 0$ | $\neq 0$ | Senoide amortecida |
| $> 0$ | $\neq 0$ | Senoide crescente (instável) |
""")

# ── SEÇÃO 8 ───────────────────────────────────────────────────────────────────
st.markdown("## 8. Sistemas — Definições e Classificação")
st.markdown(r"""
| Propriedade | Definição |
|---|---|
| **Linearidade** | $\mathcal{H}[\alpha x_1 + \beta x_2] = \alpha y_1 + \beta y_2$ |
| **Invariância no tempo** | Se $y(t)\leftrightarrow x(t)$, então $y(t-t_0)\leftrightarrow x(t-t_0)$ |
| **Causalidade** | $y(t)$ depende apenas de $x(\tau)$ para $\tau \leq t$ |
| **Estabilidade BIBO** | Entrada limitada $\Rightarrow$ saída limitada |
| **Memória** | Saída depende de valores passados ou futuros da entrada |
""")

# ── SEÇÃO 9 ───────────────────────────────────────────────────────────────────
st.markdown("## 9. Princípio da Superposição")
st.markdown(r"""
Um sistema é **linear** se satisfaz simultaneamente:

**Aditividade:** $\mathcal{H}[x_1(t)+x_2(t)] = y_1(t)+y_2(t)$

**Homogeneidade:** $\mathcal{H}[\alpha\,x(t)] = \alpha\,y(t)$

A combinação dessas propriedades permite analisar sistemas complexos decompondo a entrada em sinais mais simples.
""")

# ── SEÇÃO 10 ──────────────────────────────────────────────────────────────────
st.markdown("## 10. Estabilidade")
st.markdown(r"""
**Critério BIBO** (*Bounded-Input Bounded-Output*): um sistema LTI é BIBO-estável se e somente se sua resposta ao impulso $h(t)$ é absolutamente integrável:

$$\int_{-\infty}^{+\infty}|h(t)|\,dt < \infty$$

**Critério dos polos:** o sistema é estável se e somente se todos os polos da função de transferência estão no **semiplano esquerdo** (parte real negativa).
""")

# ── SEÇÃO 11 ──────────────────────────────────────────────────────────────────
st.markdown("## 11. Sistemas de Controle")
st.markdown(r"""
### 11.1 Malha Aberta
A saída **não é medida** — o controlador age sem conhecer o resultado.

### 11.2 Malha Fechada (Realimentação)
A saída é **medida e comparada** com a referência. O erro $E(t) = R(t) - Y(t)$ corrige o sistema continuamente.

### 11.3 Sinais de entrada típicos

| Entrada | Expressão | Uso principal |
|---|---|---|
| Impulso | $\delta(t)$ | Resposta transitória |
| Degrau | $u(t)$ | Transitória + erro estacionário |
| Rampa | $t\,u(t)$ | Sistemas de rastreamento |
| Senoide | $A\sin(\omega t)$ | Análise em frequência |
""")

# ── SEÇÃO 12 ──────────────────────────────────────────────────────────────────
st.markdown("## 12. Diagramas de Blocos")
st.markdown(r"""
| Configuração | Equivalente |
|---|---|
| Blocos em cascata | $G_{eq} = G_1 \cdot G_2$ |
| Blocos em paralelo | $G_{eq} = G_1 \pm G_2$ |
| Malha fechada (neg.) | $G_{eq} = \dfrac{G}{1+GH}$ |
""")

# ── SEÇÃO 13 ──────────────────────────────────────────────────────────────────
st.markdown("## 13. Especificações de Desempenho")
st.markdown(r"""
Para sistemas de 2ª ordem subamortecidos ($0 < \xi < 1$):

| Especificação | Expressão |
|---|---|
| Ultrapassagem $UP\,(\%)$ | $100\,e^{-\pi\xi/\sqrt{1-\xi^2}}$ |
| Tempo de pico $T_p$ | $\pi/\omega_d$ |
| Tempo de acomodação $T_s$ (2%) | $\approx 4/(\xi\omega_n)$ |
| Tempo de subida $T_r$ (10–90%) | $\approx (1.8)/\omega_n$ |
""")

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
