import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal

st.set_page_config(page_title="Resposta em Frequência", page_icon="📊", layout="wide")
st.title("📊 Resposta em Frequência")
st.caption("Modelagem e Sistemas Lineares · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

st.markdown("## 1. Conceitos")
st.markdown(r"""
Para entrada senoidal $u(t)=A\sin(\omega t)$ em sistema LTI estável, a saída em regime permanente é:
$$y_{rp}(t) = A\,|H(j\omega)|\,\sin\!\bigl(\omega t + \angle H(j\omega)\bigr)$$

| Indicador | Definição | Unidade |
|---|---|---|
| **Magnitude** | $|H(j\omega)|$ ou $20\log_{10}|H(j\omega)|$ | dB |
| **Fase** | $\angle H(j\omega)$ | graus |
""")

st.markdown("## 2. Diagrama de Bode — Fatores Elementares")
st.markdown(r"""
| Fator $G(s)$ | Inclinação (mag) | Fase |
|---|---|---|
| Constante $K$ | 0 dB/déc | 0° (K>0) ou −180° (K<0) |
| Integrador $1/s$ | −20 dB/déc | −90° |
| Derivador $s$ | +20 dB/déc | +90° |
| Polo simples $1/(1+s/a)$ | −20 dB/déc acima de $a$ | 0° → −90° |
| Zero simples $(1+s/a)$ | +20 dB/déc acima de $a$ | 0° → +90° |
| Par complexo (2ª ord.) | −40 dB/déc | 0° → −180° |
""")

st.markdown("### 🎛️ Explorador de Bode — Sistemas de 1ª Ordem")
c1, c2 = st.columns([1, 2])
with c1:
    k1 = st.slider("Ganho $k$", 0.1, 10.0, 1.0, 0.1, key="b1k")
    a1 = st.slider("Polo $a$", 0.1, 10.0, 1.0, 0.1, key="b1a")

w = np.logspace(-2, 3, 1500)
_, H1 = signal.freqs([k1], [1, a1], worN=w)
mag1 = 20*np.log10(np.abs(H1))
ph1  = np.degrees(np.unwrap(np.angle(H1)))

with c2:
    fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True,
                         subplot_titles=("Magnitude (dB)", "Fase (°)"))
    fig1.add_trace(go.Scatter(x=w, y=mag1, mode="lines",
                              line=dict(color="#3d8ef0", width=2.5), showlegend=False), row=1, col=1)
    fig1.add_trace(go.Scatter(x=w, y=ph1, mode="lines",
                              line=dict(color="#ef4444", width=2.5), showlegend=False), row=2, col=1)
    fig1.update_xaxes(type="log", title_text="ω (rad/s)", row=2, col=1)
    fig1.update_yaxes(title_text="dB", row=1, col=1)
    fig1.update_yaxes(title_text="°", row=2, col=1)
    fig1.update_layout(height=380, margin=dict(t=30,b=20,l=10,r=10))
    st.plotly_chart(fig1, use_container_width=True)

st.markdown("## 3. Margens de Ganho e Fase")
st.markdown(r"""
| Margem | Definição | Sistema estável |
|---|---|---|
| **Margem de ganho** $MG$ | Ganho extra até instabilidade (freq. de fase −180°) | $MG > 0$ dB |
| **Margem de fase** $MF$ | Fase extra até −180° (freq. de ganho 0 dB) | $MF > 0°$ |

Valores típicos de projeto: $MG > 6\text{ dB}$, $MF > 30°$.
""")

st.markdown("### 🎛️ Explorador de Bode — Sistemas de 2ª Ordem")
c1, c2 = st.columns([1, 2])
with c1:
    k2  = st.slider("Ganho $k$", 0.1, 5.0, 1.0, 0.1, key="b2k")
    xi2 = st.slider("ξ", 0.05, 2.0, 0.7, 0.05, key="b2xi")
    wn2 = st.slider("ωₙ (rad/s)", 0.2, 10.0, 2.0, 0.2, key="b2wn")

num2 = [k2 * wn2**2]
den2 = [1, 2*xi2*wn2, wn2**2]
_, H2 = signal.freqs(num2, den2, worN=w)
mag2 = 20*np.log10(np.abs(H2)+1e-12)
ph2  = np.degrees(np.unwrap(np.angle(H2)))

with c2:
    fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True,
                         subplot_titles=("Magnitude (dB)", "Fase (°)"))
    fig2.add_trace(go.Scatter(x=w, y=mag2, mode="lines",
                              line=dict(color="#3d8ef0", width=2.5), showlegend=False), row=1, col=1)
    fig2.add_trace(go.Scatter(x=w, y=ph2, mode="lines",
                              line=dict(color="#ef4444", width=2.5), showlegend=False), row=2, col=1)
    fig2.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
    fig2.add_hline(y=-180, line_dash="dash", line_color="gray", row=2, col=1)
    fig2.update_xaxes(type="log", title_text="ω (rad/s)", row=2, col=1)
    fig2.update_yaxes(title_text="dB", row=1, col=1)
    fig2.update_yaxes(title_text="°", row=2, col=1)
    fig2.update_layout(height=380, margin=dict(t=30,b=20,l=10,r=10))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("## 4. Diagrama de Nichols")
st.markdown(r"""
O diagrama de Nichols plota **fase (eixo x)** vs **magnitude em dB (eixo y)** parametrizados por $\omega$.
Permite ler graficamente as margens de ganho e fase.
""")

st.markdown("### 🎛️ Explorador de Nichols — Variação de ξ")
c1, c2 = st.columns([1, 2])
with c1:
    wn_n = st.slider("ωₙ (rad/s)", 0.5, 5.0, 2.0, 0.5, key="n_wn")
    xi_list = st.multiselect("Valores de ξ", [0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5],
                              default=[0.1, 0.3, 0.7])

cores = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2"]
w_n = np.logspace(-1, 2, 2000)

with c2:
    fig_n = go.Figure()
    for i, xi_n in enumerate(xi_list):
        _, H_n = signal.freqs([wn_n**2], [1, 2*xi_n*wn_n, wn_n**2], worN=w_n)
        ph_n  = np.degrees(np.unwrap(np.angle(H_n)))
        mag_n = 20*np.log10(np.abs(H_n)+1e-12)
        fig_n.add_trace(go.Scatter(x=ph_n, y=mag_n, mode="lines",
                                   line=dict(color=cores[i % len(cores)], width=2),
                                   name=f"ξ={xi_n}"))
    fig_n.add_vline(x=-180, line_dash="dash", line_color="gray")
    fig_n.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_n.update_layout(height=360, xaxis_title="Fase (°)", yaxis_title="Magnitude (dB)",
                        title="Diagrama de Nichols", margin=dict(t=40,b=20,l=10,r=10))
    st.plotly_chart(fig_n, use_container_width=True)

st.markdown("## 5. Explorador Livre — Qualquer G(s)")
st.markdown("Insira os coeficientes de $G(s) = N(s)/D(s)$ em ordem **decrescente** de $s$.")
c1, c2 = st.columns([1, 2])
with c1:
    num_str = st.text_input("Numerador (ex: `10`)", "10", key="free_num")
    den_str = st.text_input("Denominador (ex: `1,3,2,0`)", "1,3,2,0", key="free_den")
    w_min = st.number_input("ω mín (rad/s)", 0.001, 1.0, 0.01, key="wmin")
    w_max = st.number_input("ω máx (rad/s)", 1.0, 10000.0, 1000.0, key="wmax")

try:
    num_f = list(map(float, num_str.split(",")))
    den_f = list(map(float, den_str.split(",")))
    w_f = np.logspace(np.log10(w_min), np.log10(w_max), 2000)
    _, H_f = signal.freqs(num_f, den_f, worN=w_f)
    mag_f = 20*np.log10(np.abs(H_f)+1e-12)
    ph_f  = np.degrees(np.unwrap(np.angle(H_f)))
    with c2:
        fig_f = make_subplots(rows=2, cols=1, shared_xaxes=True,
                              subplot_titles=("Magnitude (dB)", "Fase (°)"))
        fig_f.add_trace(go.Scatter(x=w_f, y=mag_f, mode="lines",
                                   line=dict(color="#3d8ef0", width=2.5), showlegend=False), row=1, col=1)
        fig_f.add_trace(go.Scatter(x=w_f, y=ph_f, mode="lines",
                                   line=dict(color="#ef4444", width=2.5), showlegend=False), row=2, col=1)
        fig_f.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
        fig_f.add_hline(y=-180, line_dash="dash", line_color="gray", row=2, col=1)
        fig_f.update_xaxes(type="log", title_text="ω (rad/s)", row=2, col=1)
        fig_f.update_layout(height=380, margin=dict(t=30,b=20,l=10,r=10))
        st.plotly_chart(fig_f, use_container_width=True)
except Exception as e:
    st.error(f"Erro ao calcular: {e}. Verifique os coeficientes.")

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
