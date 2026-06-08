import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import lti, lsim

st.set_page_config(page_title="Realimentação — Malha Fechada", page_icon="🔄", layout="wide")
st.title("🔄 Realimentação — Malha Fechada")
st.caption("Modelagem e Sistemas Lineares · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

st.markdown("## 1. Estrutura de Malha Fechada")
st.markdown(r"""
Realimentação negativa unitária com controlador proporcional $C(s) = k$:
$$E(s) = R(s)-Y(s), \qquad \boxed{H_{MF}(s)=\frac{G(s)}{1+G(s)}}$$

| Aspecto | Malha Aberta | Malha Fechada |
|---|---|---|
| Erro em regime | Não controlado | Pode ser zerado |
| Sensibilidade | Alta | Reduzida |
| Rejeição a perturbações | Nenhuma | Significativa |
""")

st.markdown("## 2. Erro em Regime Permanente e Tipo do Sistema")
st.markdown(r"""
Pelo **Teorema do Valor Final**:
$$e_{rp} = \lim_{s\to 0}\frac{s\,R(s)}{1+G(s)}$$

| Tipo | Integradores em $G(s)$ | Erro degrau | Erro rampa | Erro parábola |
|---|---|---|---|---|
| Tipo 0 | 0 | $k_r/(1+K_p)$ | $\infty$ | $\infty$ |
| Tipo 1 | 1 | 0 | $k_r/K_v$ | $\infty$ |
| Tipo 2 | 2 | 0 | 0 | $k_r/K_a$ |
""")

st.markdown("### 🎛️ Explorador — Erro em Regime Permanente")
c1, c2 = st.columns([1, 2])
with c1:
    tipo = st.radio("Tipo do sistema", ["Tipo 0", "Tipo 1", "Tipo 2"], key="tipo_sys")
    entrada = st.radio("Entrada", ["Degrau", "Rampa", "Parábola"], key="entrada_sys")
    k_e = st.slider("Ganho $k$", 0.5, 10.0, 2.0, 0.5, key="k_err")

t = np.linspace(0, 15, 1200)
n_int = {"Tipo 0": 0, "Tipo 1": 1, "Tipo 2": 2}[tipo]

if entrada == "Degrau":
    ref = np.ones_like(t)
elif entrada == "Rampa":
    ref = t.copy()
else:
    ref = 0.5 * t**2

if n_int == 0:
    num_g, den_g = [k_e], [1, 1]
elif n_int == 1:
    num_g, den_g = [k_e], [1, 1, 0]
else:
    num_g, den_g = [k_e], [1, 1, 0, 0]

try:
    from numpy.polynomial import polynomial as P
    num_mf = num_g
    den_mf_poly = np.polymul(den_g, [1]) 
    den_mf = list(np.polyadd(den_g, num_g))
    sys_mf = lti(num_g, den_mf)
    _, y_out, _ = lsim(sys_mf, ref, t)
    err = ref - y_out
    e_rp = abs(err[-1]) if abs(err[-1]) < 1000 else float('inf')
except Exception:
    y_out = np.zeros_like(t)
    err   = ref.copy()
    e_rp  = float('inf')

with c2:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Saída y(t) vs Referência r(t)", "Erro e(t)"))
    fig.add_trace(go.Scatter(x=t, y=ref, mode="lines",
                             line=dict(color="gray", width=1.5, dash="dash"), name="r(t)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=np.clip(y_out, -50, 200), mode="lines",
                             line=dict(color="#3d8ef0", width=2.5), name="y(t)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=np.clip(err, -50, 50), mode="lines",
                             line=dict(color="#ef4444", width=2), name="e(t)"), row=2, col=1)
    fig.add_hline(y=0, line_dash="dot", line_color="gray", row=2, col=1)
    fig.update_xaxes(title_text="t (s)", row=2, col=1)
    fig.update_layout(height=380, margin=dict(t=30,b=20,l=10,r=10))
    st.plotly_chart(fig, use_container_width=True)

erp_str = f"{e_rp:.4f}" if e_rp != float('inf') else "∞"
st.metric("Erro em regime permanente $e_{rp}$", erp_str)

st.markdown("## 3. Planta de 1ª Ordem em Malha Fechada")
st.markdown(r"""
Para $G_p(s) = 1/(s+a)$ e $C(s) = k$:
$$H_{MF}(s) = \frac{k}{s+a+k} \quad\Rightarrow\quad \text{polo em } s=-(a+k), \quad y(\infty)=\frac{k}{a+k}$$
""")

st.markdown("### 🎛️ Explorador — Planta 1ª Ordem")
c1, c2 = st.columns([1, 2])
with c1:
    a_p1 = st.slider("Polo da planta $a$", 0.1, 3.0, 0.8, 0.1, key="ap1")
    k_p1 = st.slider("Ganho $k$", 0.5, 20.0, 3.0, 0.5, key="kp1")
    ent_p1 = st.radio("Entrada", ["Degrau", "Rampa"], key="entp1")

t1 = np.linspace(0, 15, 1500)
ref1 = np.ones_like(t1) if ent_p1 == "Degrau" else t1
sys_p1 = lti([k_p1], [1, a_p1 + k_p1])
_, y_p1, _ = lsim(sys_p1, ref1, t1)
err1 = ref1 - y_p1
polo_mf1 = -(a_p1 + k_p1)
y_inf1 = k_p1 / (a_p1 + k_p1)

with c2:
    fig_p1 = make_subplots(rows=1, cols=2, subplot_titles=("Saída vs Referência", "Plano s"))
    fig_p1.add_trace(go.Scatter(x=t1, y=ref1, mode="lines",
                                line=dict(color="gray", dash="dash", width=1.5), name="r(t)"), row=1, col=1)
    fig_p1.add_trace(go.Scatter(x=t1, y=y_p1, mode="lines",
                                line=dict(color="#3d8ef0", width=2.5), name="y(t)"), row=1, col=1)
    fig_p1.add_trace(go.Scatter(x=[-a_p1], y=[0], mode="markers",
                                marker=dict(symbol="x", size=12, color="gray", line=dict(width=2.5)),
                                name="polo MA"), row=1, col=2)
    fig_p1.add_trace(go.Scatter(x=[polo_mf1], y=[0], mode="markers",
                                marker=dict(symbol="x", size=12, color="#3d8ef0", line=dict(width=2.5)),
                                name="polo MF"), row=1, col=2)
    fig_p1.add_shape(type="line", x0=0, y0=-2, x1=0, y1=2, line=dict(color="gray", width=1), row=1, col=2)
    fig_p1.add_shape(type="line", x0=-25, y0=0, x1=1, y1=0, line=dict(color="gray", width=1), row=1, col=2)
    fig_p1.update_xaxes(range=[-25, 1], title_text="σ", row=1, col=2)
    fig_p1.update_yaxes(range=[-2, 2], row=1, col=2)
    fig_p1.update_layout(height=320, margin=dict(t=30,b=20,l=10,r=10))
    st.plotly_chart(fig_p1, use_container_width=True)

cols = st.columns(3)
cols[0].metric("Polo MF", f"{polo_mf1:.2f}")
cols[1].metric("y(∞)", f"{y_inf1:.4f}")
cols[2].metric("eᵣₚ (degrau)", f"{1-y_inf1:.4f}")

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
