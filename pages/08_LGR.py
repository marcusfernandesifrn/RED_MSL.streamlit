import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import lti, lsim

st.set_page_config(page_title="Lugar Geométrico das Raízes", page_icon="🗺️", layout="wide")
st.title("🗺️ Lugar Geométrico das Raízes (LGR)")
st.caption("Modelagem e Sistemas Lineares · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

st.markdown("## 1. Conceito e Regras do LGR")
st.markdown(r"""
O **LGR** mostra como os polos de malha fechada se movem no plano $s$ quando o ganho $k$ varia de $0$ a $\infty$.

Para $G(s) = k\,N(s)/D(s)$, os polos de MF satisfazem $1 + k\,G(s) = 0$, i.e. $G(s) = -1/k$.

### Regras construtivas
| Regra | Enunciado |
|---|---|
| **Partida** ($k=0$) | LGR parte dos **polos de malha aberta** |
| **Chegada** ($k\to\infty$) | LGR chega nos **zeros de malha aberta** (ou ao infinito) |
| **Eixo real** | Ponto no eixo real pertence ao LGR se o número de polos+zeros à sua **direita** for **ímpar** |
| **Assíntotas** | $(n_p-n_z)$ ramos vão ao infinito com ângulos $\pm 180°/(n_p-n_z)$ |
| **Centróide** | $\sigma_c = (\sum p_i - \sum z_i)/(n_p-n_z)$ |
""")

st.markdown("## 2. LGR Interativo")
c1, c2 = st.columns([1, 2])
with c1:
    num_str = st.text_input("Numerador N(s) — coef. ordem decrescente", "1", key="lgr_num")
    den_str = st.text_input("Denominador D(s) — coef. ordem decrescente", "1,3,2,0", key="lgr_den")
    k_lgr   = st.slider("Ganho atual $k$", 0.0, 200.0, 10.0, 0.5, key="lgr_k")
    st.caption("Exemplo: `1,3,2,0` → $s(s+1)(s+2)$")

try:
    num_c = list(map(float, num_str.split(",")))
    den_c = list(map(float, den_str.split(",")))
    poles_ma = np.roots(den_c)
    zeros_ma = np.roots(num_c) if len(num_c) > 1 else np.array([])

    k_arr = np.linspace(0, k_lgr * 3 + 50, 3000)
    roots_all = []
    for k_i in k_arr:
        closed_den = np.polyadd(den_c, list(k_i * np.array(num_c)) + [0]*(len(den_c)-len(num_c)-1) if len(den_c) > len(num_c)+1 else list(k_i * np.poly1d(num_c)))
        try:
            closed_den = np.polyadd(den_c, np.pad(k_i * np.array(num_c), (len(den_c)-len(num_c), 0)))
            r = np.roots(closed_den)
            roots_all.append(r)
        except Exception:
            pass

    poles_k = np.roots(np.polyadd(den_c, np.pad(k_lgr * np.array(num_c), (len(den_c)-len(num_c), 0))))

    with c2:
        fig_lgr = go.Figure()
        fig_lgr.add_shape(type="line", x0=0, y0=-10, x1=0, y1=10, line=dict(color="gray", width=1))
        fig_lgr.add_shape(type="line", x0=-10, y0=0, x1=3, y1=0, line=dict(color="gray", width=1))
        fig_lgr.add_vrect(x0=0, x1=3, fillcolor="rgba(239,68,68,0.06)", layer="below", line_width=0)

        if roots_all:
            roots_arr = np.array(roots_all)
            n_roots = roots_arr.shape[1]
            colors_lgr = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd"]
            for i in range(n_roots):
                fig_lgr.add_trace(go.Scatter(
                    x=roots_arr[:,i].real, y=roots_arr[:,i].imag,
                    mode="lines", line=dict(color=colors_lgr[i%len(colors_lgr)], width=1.5),
                    showlegend=False, hoverinfo="skip"))

        fig_lgr.add_trace(go.Scatter(
            x=poles_ma.real, y=poles_ma.imag, mode="markers",
            marker=dict(symbol="x", size=14, color="#d62728", line=dict(width=3)),
            name="Polos MA"))
        if len(zeros_ma) > 0:
            fig_lgr.add_trace(go.Scatter(
                x=zeros_ma.real, y=zeros_ma.imag, mode="markers",
                marker=dict(symbol="circle-open", size=13, color="#1f77b4", line=dict(width=2.5)),
                name="Zeros MA"))
        fig_lgr.add_trace(go.Scatter(
            x=poles_k.real, y=poles_k.imag, mode="markers",
            marker=dict(symbol="diamond", size=10, color="#f59e0b", line=dict(width=2)),
            name=f"Polos MF (k={k_lgr:.1f})"))

        fig_lgr.update_layout(height=420, title=f"LGR — k atual = {k_lgr:.1f}",
                               xaxis=dict(range=[-10, 3], title="σ"),
                               yaxis=dict(range=[-10, 10], title="jω"),
                               margin=dict(t=40,b=20,l=10,r=10))
        st.plotly_chart(fig_lgr, use_container_width=True)

        stable = all(p.real < 0 for p in poles_k)
        if stable:
            st.success(f"✅ k = {k_lgr:.1f} — Sistema **estável**")
        else:
            st.error(f"❌ k = {k_lgr:.1f} — Sistema **instável**")

except Exception as e:
    st.error(f"Erro: {e}")

st.markdown("## 3. Ganho Crítico e Erro com Perturbação")
st.markdown(r"""
Para $G(s) = k/[s(s+a_1)(s+a_2)]$:
$$k_{crit} = a_1\,a_2\,(a_1+a_2)$$

Com perturbação degrau $D(s) = 1/s$ na entrada da planta:
$$e_{rp,D} = \frac{-1}{a+k}$$

O ganho $k$ aumentado reduz o erro de perturbação, mas pode desestabilizar o sistema.
""")

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
