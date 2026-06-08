import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import lti, step as sc_step

st.set_page_config(page_title="Dinâmica — Sistemas de 1ª Ordem", page_icon="📈", layout="wide")
st.title("📈 Dinâmica — Sistemas de 1ª Ordem")
st.caption("Modelagem e Sistemas Lineares · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

with st.expander("📋 Índice", expanded=False):
    st.markdown("""
1. Função de Transferência de 1ª Ordem
2. Resposta ao Degrau — Componentes e Especificações
3. Sistemas de Grau Relativo 1 — Exemplos
4. Sistemas com Zero — Grau Relativo 0
5. Polo no Semiplano Direito — Sistema Instável
6. Polo na Origem — Sistema Marginalmente Estável
""")

# ── SEÇÃO 1 ───────────────────────────────────────────────────────────────────
st.markdown("## 1. Função de Transferência de 1ª Ordem")
st.markdown(r"""
### 1.1 Grau relativo
O **grau relativo** $n^*$ é a diferença entre o grau do denominador ($n$) e do numerador ($m$):
$$n^* = n - m$$

### 1.2 Formas canônicas
Para sistemas de 1ª ordem ($n=1$, $n^*=1$), polo em $s = -a$:
$$H(s) = \frac{k}{s+a} = \frac{k/a}{\frac{s}{a}+1} = \frac{k'}{\tau s+1}$$

onde $\tau = 1/a$ é a **constante de tempo** e $k' = k/a$ é o **ganho DC**.
""")

# ── SEÇÃO 2 ───────────────────────────────────────────────────────────────────
st.markdown("## 2. Resposta ao Degrau — Componentes e Especificações")
st.markdown(r"""
Para entrada degrau de amplitude $k_r$, $X(s) = k_r/s$:
$$Y(s) = \frac{k\,k_r}{s\,(s+a)} \quad\Rightarrow\quad \boxed{y(t) = \frac{k\,k_r}{a}\bigl(1-e^{-at}\bigr), \quad t\geq 0}$$

| Especificação | Fórmula |
|---|---|
| Valor final | $y(\infty) = k\,k_r/a$ |
| Constante de tempo | $\tau = 1/a$ |
| Tempo de subida (10–90%) | $T_r \approx 2{,}2/a$ |
| Tempo de acomodação (2%) | $T_s \approx 4/a$ |
""")

st.markdown("### 🎛️ Explorador — Resposta ao Degrau de 1ª Ordem")
c1, c2 = st.columns([1, 2])
with c1:
    k_v  = st.slider("Ganho $k$", 0.5, 5.0, 1.4, 0.1, key="o1_k")
    a_v  = st.slider("Polo $a$", 0.2, 3.0, 0.7, 0.1, key="o1_a")
    kr_v = st.slider("Amplitude $k_r$", 0.5, 3.0, 1.0, 0.1, key="o1_kr")

t  = np.linspace(0, 18, 700)
yf = k_v * kr_v / a_v
y  = yf * (1 - np.exp(-a_v * t))
tau = 1 / a_v

with c2:
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Plano s", "Resposta ao degrau"))
    fig.add_trace(go.Scatter(x=[-a_v], y=[0], mode="markers",
                             marker=dict(symbol="x", size=14, color="#d62728", line=dict(width=3)),
                             name=f"polo s = -{a_v:.1f}"), row=1, col=1)
    fig.add_shape(type="line", x0=0, y0=-2, x1=0, y1=2,
                  line=dict(color="gray", width=1), row=1, col=1)
    fig.add_shape(type="line", x0=-5, y0=0, x1=1, y1=0,
                  line=dict(color="gray", width=1), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=y, mode="lines",
                             line=dict(color="#1f77b4", width=2.2), name="y(t)"), row=1, col=2)
    fig.add_hline(y=yf, line_dash="dash", line_color="gray", annotation_text=f"y(∞)={yf:.2f}", row=1, col=2)
    fig.add_vline(x=tau, line_dash="dot", line_color="#f59e0b", annotation_text=f"τ={tau:.2f}s", row=1, col=2)
    fig.update_xaxes(range=[-5, 1], title_text="σ", row=1, col=1)
    fig.update_yaxes(range=[-2, 2], title_text="jω", row=1, col=1)
    fig.update_xaxes(title_text="t (s)", row=1, col=2)
    fig.update_yaxes(title_text="y(t)", row=1, col=2)
    fig.update_layout(height=320, margin=dict(t=30, b=20, l=10, r=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

col_m = st.columns(4)
for i, (lbl, val) in enumerate([
    ("y(∞)", f"{yf:.3f}"),
    ("τ = 1/a", f"{tau:.3f} s"),
    ("Tᵣ ≈ 2.2/a", f"{2.2/a_v:.3f} s"),
    ("Tₛ ≈ 4/a", f"{4/a_v:.3f} s"),
]):
    col_m[i].metric(lbl, val)

# ── SEÇÃO 3 ───────────────────────────────────────────────────────────────────
st.markdown("## 3. Sistemas de Grau Relativo 1 — Exemplos Físicos")
st.markdown(r"""
| Domínio | Sistema | $k$ | $a$ |
|---|---|---|---|
| Elétrico | Circuito RL: $V_a \to I$ | $1/L$ | $R/L$ |
| Elétrico | Circuito RC: $V_e \to V_s$ | $1/(RC)$ | $1/(RC)$ |
| Mecânico | Massa-amortecedor: $F \to v$ | $1/M$ | $B/M$ |
| Rotacional | Inércia-amortecedor: $\mathcal{T} \to \omega$ | $1/J$ | $B/J$ |
| Térmico | Câmara isolada: $\dot{Q} \to T$ | $1/C$ | $1/(RC)$ |
""")

# ── SEÇÃO 4 ───────────────────────────────────────────────────────────────────
st.markdown("## 4. Sistemas com Zero — Grau Relativo 0")
st.markdown(r"""
$$H(s) = \frac{k(s+b)}{s+a}, \quad n^* = 0$$

A presença de um zero $s = -b$ adiciona uma componente derivativa à saída:
$$y(t) = \frac{k\,k_r}{a}\bigl(1-e^{-at}\bigr) + \frac{k\,k_r(b-a)}{a}\,e^{-at}$$

Se $b < 0$ (zero no SPD), o sistema é de **fase não-mínima**: a resposta começa indo na direção errada.
""")

st.markdown("### 🎛️ Explorador — Efeito do Zero")
c1, c2 = st.columns([1, 2])
with c1:
    k2  = st.slider("Ganho $k$", 0.5, 5.0, 4.0, 0.5, key="z_k")
    a2  = st.slider("Polo $a$", 0.2, 3.0, 0.8, 0.1, key="z_a")
    b2  = st.slider("Zero $b$", -2.0, 4.0, 2.0, 0.2, key="z_b")

t2 = np.linspace(0, 15, 600)
sys2 = lti([k2, k2*b2], [1, a2])
_, y2 = sc_step(sys2, T=t2)
sys_ref = lti([k2], [1, a2])
_, y_ref = sc_step(sys_ref, T=t2)
y_ref = y_ref * (k2 / a2) / (y_ref[-1] + 1e-12) * (k2 * b2 / a2)

with c2:
    fig2 = make_subplots(rows=1, cols=2, subplot_titles=("Plano s", "Resposta ao degrau"))
    fig2.add_trace(go.Scatter(x=[-a2], y=[0], mode="markers",
                              marker=dict(symbol="x", size=14, color="#d62728", line=dict(width=3)),
                              name=f"polo -{a2:.1f}"), row=1, col=1)
    fig2.add_trace(go.Scatter(x=[-b2], y=[0], mode="markers",
                              marker=dict(symbol="circle-open", size=13, color="#1f77b4", line=dict(width=2.5)),
                              name=f"zero -{b2:.1f}"), row=1, col=1)
    fig2.add_shape(type="line", x0=0, y0=-2, x1=0, y1=2, line=dict(color="gray", width=1), row=1, col=1)
    fig2.add_shape(type="line", x0=-5, y0=0, x1=1, y1=0, line=dict(color="gray", width=1), row=1, col=1)
    fig2.add_trace(go.Scatter(x=t2, y=y2, mode="lines",
                              line=dict(color="#1f77b4", width=2.5), name="com zero"), row=1, col=2)
    fig2.update_xaxes(range=[-5, 1], title_text="σ", row=1, col=1)
    fig2.update_yaxes(range=[-2, 2], title_text="jω", row=1, col=1)
    fig2.update_xaxes(title_text="t (s)", row=1, col=2)
    fig2.update_layout(height=320, margin=dict(t=30, b=20, l=10, r=10))
    st.plotly_chart(fig2, use_container_width=True)

if b2 < 0:
    st.warning("⚠️ Zero no semiplano direito (b < 0): sistema de **fase não-mínima** — a resposta começa na direção oposta.")

# ── SEÇÃO 5 ───────────────────────────────────────────────────────────────────
st.markdown("## 5. Polo no Semiplano Direito — Sistema Instável")
st.markdown(r"""
Para $H(s) = k/(s-a)$ com $a > 0$, o polo está no SPD:
$$y(t) = \frac{k\,k_r}{a}\bigl(e^{at} - 1\bigr) \to \infty$$

A constante de tempo do modo instável é $1/a$ — quanto maior $a$, mais rápida a divergência.
""")

st.markdown("### 🎛️ Explorador — Polo Instável")
c1, c2 = st.columns([1, 2])
with c1:
    a_inst = st.slider("Polo $a > 0$", 0.1, 2.0, 0.5, 0.1, key="inst_a")

t_inst = np.linspace(0, 8, 500)
y_inst = (1/a_inst) * (np.exp(a_inst * t_inst) - 1)
y_inst = np.clip(y_inst, -50, 200)

with c2:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=t_inst, y=y_inst, mode="lines",
                              line=dict(color="#ef4444", width=2.5), name="y(t)"))
    fig3.update_layout(height=280, margin=dict(t=20,b=20,l=10,r=10),
                       xaxis_title="t (s)", yaxis_title="y(t)",
                       title=f"Polo em s = +{a_inst:.1f} (instável)")
    st.plotly_chart(fig3, use_container_width=True)

# ── SEÇÃO 6 ───────────────────────────────────────────────────────────────────
st.markdown("## 6. Polo na Origem — Sistema Marginalmente Estável")
st.markdown(r"""
Para $H(s) = k/s$ (integrador puro), o polo está na origem:
$$y(t) = k\,k_r\,t \quad \text{(rampa)}$$

Com realimentação unitária: $H_{MF}(s) = k/(s+k)$, polo em $s = -k$ — o integrador fica estável.
""")

st.markdown("### 🎛️ Explorador — Polo na Origem com Realimentação")
c1, c2 = st.columns([1, 2])
with c1:
    k_int = st.slider("Ganho $k$", 0.5, 5.0, 2.0, 0.5, key="int_k")

t_int = np.linspace(0, 10, 500)
sys_mf = lti([k_int], [1, k_int])
_, y_mf = sc_step(sys_mf, T=t_int)

with c2:
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=t_int, y=y_mf, mode="lines",
                              line=dict(color="#10b981", width=2.5), name="y(t) MF"))
    fig4.add_hline(y=1, line_dash="dash", line_color="gray")
    fig4.update_layout(height=280, margin=dict(t=20,b=20,l=10,r=10),
                       xaxis_title="t (s)", yaxis_title="y(t)",
                       title=f"Malha fechada com k={k_int:.1f}")
    st.plotly_chart(fig4, use_container_width=True)
    st.metric("Polo MF", f"s = -{k_int:.2f}", f"τ = {1/k_int:.3f} s")

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
