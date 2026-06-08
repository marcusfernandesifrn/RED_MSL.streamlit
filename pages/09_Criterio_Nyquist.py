import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal

st.set_page_config(page_title="Critério de Nyquist", page_icon="🌀", layout="wide")
st.title("🌀 Critério de Nyquist")
st.caption("Modelagem e Sistemas Lineares · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

st.markdown("## 1. Introdução e Motivação")
st.markdown(r"""
Dado o sistema realimentado $T(s) = G(s)/[1+G(s)H(s)]$, os **polos de $T(s)$** são as raízes de $1+G(s)H(s)=0$.

Definindo $F(s) = 1+G(s)H(s)$:
| Singularidade | Relação |
|---|---|
| **Zeros** de $F(s)$ | Polos de malha fechada |
| **Polos** de $F(s)$ | Polos de malha aberta |
""")

st.markdown("## 2. Princípio do Argumento")
st.markdown(r"""
Ao percorrer um contorno fechado $A$ no plano $s$ **no sentido horário**, o contorno $F(A)$ no plano $F$ dá:

$$\boxed{N_h = Z - P}$$

onde $N_h$ = envolvimentos **horários** ao redor da origem, $Z$ = zeros de $F$ dentro de $A$, $P$ = polos de $F$ dentro de $A$.
""")

st.markdown("## 3. Enunciado do Critério de Nyquist")
st.markdown(r"""
Com $P$ polos de $G(s)H(s)$ no SPD, o sistema é **estável** se e somente se:

$$\boxed{Z = N + P = 0}$$

onde $N$ = envolvimentos **horários** do diagrama de Nyquist ao redor de $(-1, j0)$.

| $P$ | $N$ necessário | Condição |
|---|---|---|
| 0 | $N = 0$ | Diagrama não envolve $(-1,j0)$ |
| 1 | $N = -1$ | Um envolvimento anti-horário |
| 2 | $N = -2$ | Dois envolvimentos anti-horários |
""")

st.markdown("## 4. Explorador de Nyquist")
c1, c2 = st.columns([1, 2])
with c1:
    num_str = st.text_input("Numerador G(s)H(s)", "10", key="nyq_num")
    den_str = st.text_input("Denominador G(s)H(s)", "1,3,2,0", key="nyq_den")
    K_nyq   = st.slider("Ganho $K$", 0.1, 1000.0, 10.0, 1.0, key="nyq_k")
    st.caption("Ex: `1,3,2,0` → $s(s+1)(s+2)$")

try:
    num_n = [K_nyq * float(x) for x in num_str.split(",")]
    den_n = list(map(float, den_str.split(",")))
    w_pos = np.logspace(-3, 3, 5000)
    _, H_pos = signal.freqs(num_n, den_n, worN=w_pos)
    Re_pos =  H_pos.real;  Im_pos =  H_pos.imag
    Re_neg =  H_pos.real;  Im_neg = -H_pos.imag

    with c2:
        fig_nyq = go.Figure()
        fig_nyq.add_trace(go.Scatter(x=Re_pos, y=Im_pos, mode="lines",
                                      line=dict(color="#1f77b4", width=2), name="ω: 0→+∞"))
        fig_nyq.add_trace(go.Scatter(x=Re_neg, y=Im_neg, mode="lines",
                                      line=dict(color="#1f77b4", width=2, dash="dot"), name="ω: 0→−∞"))
        fig_nyq.add_trace(go.Scatter(x=[-1], y=[0], mode="markers",
                                      marker=dict(symbol="x", size=14, color="#ef4444", line=dict(width=3)),
                                      name="(-1, j0)"))
        fig_nyq.add_shape(type="line", x0=0, y0=-max(abs(Im_pos))*1.2, x1=0, y1=max(abs(Im_pos))*1.2,
                          line=dict(color="gray", width=1))
        fig_nyq.add_shape(type="line", x0=min(Re_pos)*1.2, y0=0, x1=max(Re_pos)*1.2, y1=0,
                          line=dict(color="gray", width=1))
        fig_nyq.update_layout(height=400, title=f"Diagrama de Nyquist — K={K_nyq:.1f}",
                               xaxis_title="Re", yaxis_title="Im",
                               margin=dict(t=40,b=20,l=10,r=10))
        st.plotly_chart(fig_nyq, use_container_width=True)

        # Check if (-1,0) is encircled (approximate)
        min_dist = min(np.abs(H_pos + 1))
        if min_dist < 0.1:
            st.warning("⚠️ Diagrama passa muito próximo de (-1, j0) — verifique a margem de fase.")
except Exception as e:
    st.error(f"Erro: {e}")

st.markdown("## 5. Margens de Ganho e Fase pelo Critério de Nyquist")
st.markdown(r"""
| Margem | Definição gráfica no Nyquist |
|---|---|
| **Margem de ganho** | Inverso da distância do cruzamento do eixo real negativo à origem: $MG = 1/|G(j\omega_\phi)|$ |
| **Margem de fase** | Ângulo entre o ponto de módulo unitário e o eixo real negativo: $MF = 180° + \angle G(j\omega_c)$ |
""")

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
