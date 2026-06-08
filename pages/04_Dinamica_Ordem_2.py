import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import lti, step as sc_step

st.set_page_config(page_title="Dinâmica — Sistemas de 2ª Ordem", page_icon="〰", layout="wide")
st.title("〰 Dinâmica — Sistemas de 2ª Ordem")
st.caption("Modelagem e Sistemas Lineares · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

st.markdown("## 1. Forma Canônica de 2ª Ordem")
st.markdown(r"""
$$H(s) = \frac{k\,\omega_n^2}{s^2 + 2\xi\omega_n s + \omega_n^2}$$

| Parâmetro | Símbolo | Significado |
|---|---|---|
| Ganho DC | $k$ | $y(\infty)/k_r$ para degrau $k_r$ |
| Frequência natural | $\omega_n$ [rad/s] | Raio dos polos no plano $s$ |
| Amortecimento | $\xi$ (*zeta*) | Controla o tipo de resposta |
""")

st.markdown("## 2. Tipos de Resposta ao Degrau")
st.markdown(r"""
### Regime subamortecido ($0 < \xi < 1$)
Polos complexos $s_{1,2} = -\sigma \pm j\omega_d$, com $\sigma=\xi\omega_n$, $\omega_d=\omega_n\sqrt{1-\xi^2}$:
$$y(t) = k\!\left[1 - \frac{e^{-\sigma t}}{\sqrt{1-\xi^2}}\sin(\omega_d t + \varphi)\right], \quad \varphi=\arccos(\xi)$$

### Criticamente amortecido ($\xi = 1$)
Polo duplo em $s = -\omega_n$:
$$y(t) = k\!\left[1-(1+\omega_n t)\,e^{-\omega_n t}\right]$$

### Sobreamortecido ($\xi > 1$)
Dois polos reais: $s_{1,2} = -\xi\omega_n \pm \omega_n\sqrt{\xi^2-1}$
""")

# ── EXPLORADOR 1: Slider ξ ────────────────────────────────────────────────────
st.markdown("### 🎛️ Explorador — Efeito do Amortecimento ξ")
c1, c2 = st.columns([1, 2])
with c1:
    xi_v = st.slider("Amortecimento ξ", -0.2, 3.0, 0.7, 0.05, key="xi_s")
    wn_v = st.number_input("ωₙ (rad/s)", 0.5, 10.0, 2.0, 0.5, key="wn_s")
    k_v  = st.number_input("Ganho k", 0.1, 5.0, 1.0, 0.1, key="k_s")

t = np.linspace(0, 14, 700)

def get_regime(xi):
    if xi < 0: return "Instável", "#9467bd"
    if xi == 0: return "Oscilatório puro", "#17becf"
    if xi < 1: return "Subamortecido", "#1f77b4"
    if abs(xi-1) < 1e-9: return "Criticamente amortecido", "#2ca02c"
    return "Sobreamortecido", "#d62728"

regime, cor = get_regime(xi_v)

sys_v = lti([k_v * wn_v**2], [1, 2*xi_v*wn_v, wn_v**2])
try:
    _, y_v = sc_step(sys_v, T=t)
    y_v = np.clip(y_v, -20, 20)
except Exception:
    y_v = np.zeros_like(t)

sigma = xi_v * wn_v
wd = wn_v * np.sqrt(max(1 - xi_v**2, 0)) if abs(xi_v) < 1 else 0

with c2:
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Plano s", "Resposta ao degrau"))
    if abs(xi_v) < 1 and xi_v >= 0:
        fig.add_trace(go.Scatter(x=[-sigma, -sigma], y=[wd, -wd], mode="markers",
                                 marker=dict(symbol="x", size=14, color=cor, line=dict(width=3)),
                                 showlegend=False), row=1, col=1)
    else:
        d = (xi_v*wn_v)**2 - wn_v**2
        if d >= 0:
            p1, p2 = -xi_v*wn_v + np.sqrt(d), -xi_v*wn_v - np.sqrt(d)
            for p in [p1, p2]:
                fig.add_trace(go.Scatter(x=[p], y=[0], mode="markers",
                                         marker=dict(symbol="x", size=14, color=cor, line=dict(width=3)),
                                         showlegend=False), row=1, col=1)
    fig.add_shape(type="line", x0=0, y0=-4, x1=0, y1=4, line=dict(color="gray", width=1), row=1, col=1)
    fig.add_shape(type="line", x0=-8, y0=0, x1=2, y1=0, line=dict(color="gray", width=1), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=y_v, mode="lines",
                             line=dict(color=cor, width=2.5), showlegend=False), row=1, col=2)
    fig.add_hline(y=k_v, line_dash="dash", line_color="gray", row=1, col=2)
    fig.update_xaxes(range=[-8, 2], title_text="σ", row=1, col=1)
    fig.update_yaxes(range=[-4, 4], title_text="jω", row=1, col=1)
    fig.update_xaxes(title_text="t (s)", row=1, col=2)
    fig.update_layout(height=320, margin=dict(t=30,b=20,l=10,r=10))
    st.plotly_chart(fig, use_container_width=True)

st.info(f"**Regime:** {regime}")

# ── SEÇÃO 3: Especificações ───────────────────────────────────────────────────
st.markdown("## 3. Especificações de Desempenho")
st.markdown(r"""
Para $0 < \xi < 1$:

| Especificação | Expressão analítica |
|---|---|
| Ultrapassagem $UP\,(\%)$ | $100\,e^{-\pi\xi/\sqrt{1-\xi^2}}$ |
| Instante de pico $T_p$ | $\pi/\omega_d$ |
| Tempo de acomodação $T_s$ (2%) | $\approx 4/(\xi\omega_n)$ |
| Tempo de subida $T_r$ | $\approx (1{,}8)/\omega_n$ |
""")

st.markdown("### 🎛️ Explorador — Especificações: sliders ξ e ωₙ")
c1, c2 = st.columns([1, 2])
with c1:
    xi2 = st.slider("ξ", 0.05, 0.99, 0.4, 0.05, key="xi2")
    wn2 = st.slider("ωₙ (rad/s)", 0.5, 5.0, 2.0, 0.5, key="wn2")

t2 = np.linspace(0, 14, 700)
wd2 = wn2 * np.sqrt(1 - xi2**2)
UP = 100 * np.exp(-np.pi * xi2 / np.sqrt(1 - xi2**2))
Tp = np.pi / wd2
Ts = 4 / (xi2 * wn2)
sig2 = xi2 * wn2

sys2 = lti([wn2**2], [1, 2*xi2*wn2, wn2**2])
_, y2 = sc_step(sys2, T=t2)

with c2:
    fig2 = make_subplots(rows=1, cols=2, subplot_titles=("Plano s", "Resposta ao degrau"))
    fig2.add_trace(go.Scatter(x=[-sig2, -sig2], y=[wd2, -wd2], mode="markers",
                              marker=dict(symbol="x", size=14, color="#1f77b4", line=dict(width=3)),
                              showlegend=False), row=1, col=1)
    fig2.add_shape(type="line", x0=0, y0=-6, x1=0, y1=6, line=dict(color="gray", width=1), row=1, col=1)
    fig2.add_shape(type="line", x0=-8, y0=0, x1=1, y1=0, line=dict(color="gray", width=1), row=1, col=1)
    fig2.add_trace(go.Scatter(x=t2, y=y2, mode="lines",
                              line=dict(color="#1f77b4", width=2.5), showlegend=False), row=1, col=2)
    fig2.add_hline(y=1, line_dash="dash", line_color="gray", row=1, col=2)
    if Tp < t2[-1]:
        fig2.add_vline(x=Tp, line_dash="dot", line_color="#f59e0b",
                       annotation_text=f"Tₚ={Tp:.2f}s", row=1, col=2)
    fig2.update_xaxes(range=[-8, 1], title_text="σ", row=1, col=1)
    fig2.update_yaxes(range=[-6, 6], title_text="jω", row=1, col=1)
    fig2.update_xaxes(title_text="t (s)", row=1, col=2)
    fig2.update_layout(height=320, margin=dict(t=30,b=20,l=10,r=10))
    st.plotly_chart(fig2, use_container_width=True)

cols = st.columns(4)
cols[0].metric("UP (%)", f"{UP:.1f}")
cols[1].metric("Tₚ (s)", f"{Tp:.3f}")
cols[2].metric("Tₛ 2% (s)", f"{Ts:.3f}")
cols[3].metric("ωd (rad/s)", f"{wd2:.3f}")

# ── SEÇÃO 4: Efeito conjunto ───────────────────────────────────────────────────
st.markdown("## 4. Efeito Conjunto de ξ, ωₙ e k")
st.markdown(r"""
- **ξ fixo, ωₙ varia:** o raio do polo muda — todos os tempos escalam por $1/\omega_n$
- **ωₙ fixo, ξ varia:** o ângulo do polo muda — UP muda, raio fixo
- **k varia:** polos não mudam, apenas $y(\infty) = k$ escala
""")

st.markdown("### 🎛️ Explorador — Sliders ξ, ωₙ e k")
c1, c2 = st.columns([1, 2])
with c1:
    xi3 = st.slider("ξ", 0.1, 2.0, 0.5, 0.1, key="xi3")
    wn3 = st.slider("ωₙ (rad/s)", 0.5, 5.0, 2.0, 0.5, key="wn3")
    k3  = st.slider("Ganho k", 0.5, 3.0, 1.0, 0.1, key="k3")

t3 = np.linspace(0, 14, 700)
sys3 = lti([k3 * wn3**2], [1, 2*xi3*wn3, wn3**2])
try:
    _, y3 = sc_step(sys3, T=t3)
    y3 = np.clip(y3, -20, 20)
except Exception:
    y3 = np.zeros_like(t3)

sig3 = xi3 * wn3
wd3  = wn3 * np.sqrt(max(1-xi3**2, 0)) if xi3 < 1 else 0

with c2:
    fig3 = make_subplots(rows=1, cols=2, subplot_titles=("Plano s", "Resposta ao degrau"))
    if xi3 < 1:
        fig3.add_trace(go.Scatter(x=[-sig3, -sig3], y=[wd3, -wd3], mode="markers",
                                  marker=dict(symbol="x", size=14, color="#1f77b4", line=dict(width=3)),
                                  showlegend=False), row=1, col=1)
    else:
        d3 = (xi3*wn3)**2 - wn3**2
        p1, p2 = -xi3*wn3 + np.sqrt(d3), -xi3*wn3 - np.sqrt(d3)
        for p in [p1, p2]:
            fig3.add_trace(go.Scatter(x=[p], y=[0], mode="markers",
                                      marker=dict(symbol="x", size=14, color="#d62728", line=dict(width=3)),
                                      showlegend=False), row=1, col=1)
    fig3.add_shape(type="line", x0=0, y0=-6, x1=0, y1=6, line=dict(color="gray", width=1), row=1, col=1)
    fig3.add_shape(type="line", x0=-8, y0=0, x1=1, y1=0, line=dict(color="gray", width=1), row=1, col=1)
    fig3.add_trace(go.Scatter(x=t3, y=y3, mode="lines",
                              line=dict(color="#1f77b4", width=2.5), showlegend=False), row=1, col=2)
    fig3.add_hline(y=k3, line_dash="dash", line_color="gray",
                   annotation_text=f"y(∞)={k3:.1f}", row=1, col=2)
    fig3.update_xaxes(range=[-8, 1], title_text="σ", row=1, col=1)
    fig3.update_yaxes(range=[-6, 6], title_text="jω", row=1, col=1)
    fig3.update_layout(height=320, margin=dict(t=30,b=20,l=10,r=10))
    st.plotly_chart(fig3, use_container_width=True)

# ── SEÇÃO 5: Sliders σ e ωd ───────────────────────────────────────────────────
st.markdown("## 5. Polos Complexos: σ e ωd diretamente")
st.markdown(r"""
Os polos complexos $s_{1,2} = -\sigma \pm j\omega_d$ controlam independentemente:
- $\sigma$: velocidade de decaimento do envelope — **não altera** a frequência
- $\omega_d$: frequência de oscilação — **não altera** o envelope
""")

st.markdown("### 🎛️ Explorador — Sliders σ e ωd")
c1, c2 = st.columns([1, 2])
with c1:
    sig5 = st.slider("σ (decaimento)", 0.2, 5.0, 1.0, 0.2, key="sig5")
    wd5  = st.slider("ωd (oscilação rad/s)", 0.5, 6.0, 2.0, 0.2, key="wd5")

t5 = np.linspace(0, 14, 700)
wn5  = np.sqrt(sig5**2 + wd5**2)
xi5  = sig5 / wn5
sys5 = lti([wn5**2], [1, 2*xi5*wn5, wn5**2])
_, y5 = sc_step(sys5, T=t5)

with c2:
    fig5 = make_subplots(rows=1, cols=2, subplot_titles=("Plano s", "Resposta ao degrau"))
    fig5.add_trace(go.Scatter(x=[-sig5, -sig5], y=[wd5, -wd5], mode="markers",
                              marker=dict(symbol="x", size=14, color="#1f77b4", line=dict(width=3)),
                              showlegend=False), row=1, col=1)
    fig5.add_shape(type="line", x0=0, y0=-7, x1=0, y1=7, line=dict(color="gray", width=1), row=1, col=1)
    fig5.add_shape(type="line", x0=-8, y0=0, x1=1, y1=0, line=dict(color="gray", width=1), row=1, col=1)
    env = np.exp(-sig5 * t5)
    fig5.add_trace(go.Scatter(x=t5, y=env, mode="lines",
                              line=dict(color="#f59e0b", width=1.5, dash="dot"),
                              name="envelope", showlegend=True), row=1, col=2)
    fig5.add_trace(go.Scatter(x=t5, y=y5, mode="lines",
                              line=dict(color="#1f77b4", width=2.5),
                              name="y(t)", showlegend=True), row=1, col=2)
    fig5.add_hline(y=1, line_dash="dash", line_color="gray", row=1, col=2)
    fig5.update_xaxes(range=[-8, 1], title_text="σ", row=1, col=1)
    fig5.update_yaxes(range=[-7, 7], title_text="jω", row=1, col=1)
    fig5.update_layout(height=330, margin=dict(t=30,b=20,l=10,r=10),
                       legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig5, use_container_width=True)

cols = st.columns(3)
cols[0].metric("ωn (rad/s)", f"{wn5:.3f}")
cols[1].metric("ξ", f"{xi5:.3f}")
cols[2].metric("τ = 1/σ (s)", f"{1/sig5:.3f}")

# ── SEÇÃO 6: Exemplos físicos ─────────────────────────────────────────────────
st.markdown("## 6. Exemplos Físicos de Sistemas de 2ª Ordem")
st.markdown(r"""
| Domínio | Sistema | $\omega_n$ | $\xi$ |
|---|---|---|---|
| Mecânico | Massa-mola-amortecedor | $\sqrt{k_s/M}$ | $B/(2\sqrt{k_s M})$ |
| Elétrico | Circuito RLC série | $1/\sqrt{LC}$ | $R/(2)\sqrt{C/L}$ |
| Térmico-fluido | Tanque com nível controlado | Depende do sistema | Depende das perdas |
""")

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
