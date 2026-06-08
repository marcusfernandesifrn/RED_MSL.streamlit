import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Transformada de Laplace", page_icon="∫", layout="wide")
st.title("∫ Transformada de Laplace")
st.caption("Modelagem e Sistemas Lineares · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

st.markdown("## 1. Definição")
st.markdown(r"""
A **Transformada de Laplace** converte equações diferenciais em equações algébricas no domínio $s = \sigma + j\omega$.

### 1.1 Transformada unilateral
$$\mathcal{L}[x(t)] = X(s) = \int_0^{+\infty} x(t)\,e^{-st}\,dt$$

### 1.2 Transformada inversa
$$x(t) = \mathcal{L}^{-1}[X(s)] = \frac{1}{2\pi j}\int_{\sigma-j\infty}^{\sigma+j\infty} X(s)\,e^{st}\,ds$$
""")

st.markdown("## 2. Tabela de Transformadas")
st.markdown(r"""
| $x(t)$ | $X(s)$ |
|:---|:---|
| $\delta(t)$ | $1$ |
| $u(t)$ | $\dfrac{1}{s}$ |
| $t\,u(t)$ | $\dfrac{1}{s^2}$ |
| $t^n u(t)$ | $\dfrac{n!}{s^{n+1}}$ |
| $e^{-at}u(t)$ | $\dfrac{1}{s+a}$ |
| $t\,e^{-at}u(t)$ | $\dfrac{1}{(s+a)^2}$ |
| $\sin(\omega t)\,u(t)$ | $\dfrac{\omega}{s^2+\omega^2}$ |
| $\cos(\omega t)\,u(t)$ | $\dfrac{s}{s^2+\omega^2}$ |
| $e^{-at}\sin(\omega t)\,u(t)$ | $\dfrac{\omega}{(s+a)^2+\omega^2}$ |
| $e^{-at}\cos(\omega t)\,u(t)$ | $\dfrac{s+a}{(s+a)^2+\omega^2}$ |
""")

st.markdown("## 3. Propriedades")
st.markdown(r"""
| Propriedade | Teorema |
|:---|:---|
| **Linearidade** | $\mathcal{L}[k_1 x_1+k_2 x_2] = k_1 X_1(s)+k_2 X_2(s)$ |
| **Deslocamento no tempo** | $\mathcal{L}[x(t-T)u(t-T)] = e^{-sT}X(s)$ |
| **Deslocamento na freq.** | $\mathcal{L}[e^{-at}x(t)] = X(s+a)$ |
| **Derivação** | $\mathcal{L}[x'(t)] = sX(s) - x(0^-)$ |
| **Integração** | $\mathcal{L}\!\left[\int_0^t x\,d\tau\right] = X(s)/s$ |
| **Convolução** | $\mathcal{L}[x_1*x_2] = X_1(s)\cdot X_2(s)$ |
| **Valor inicial** | $x(0^+) = \lim_{s\to\infty} s\,X(s)$ |
| **Valor final** | $x(\infty) = \lim_{s\to 0} s\,X(s)$ |
""")

st.markdown("## 4. Convolução")
st.markdown(r"""
$$(x_1 * x_2)(t) = \int_{-\infty}^{+\infty} x_1(\tau)\,x_2(t-\tau)\,d\tau$$

A saída de um sistema LCIT é:
$$y(t) = x(t)*h(t) \;\overset{\mathcal{L}}{\longleftrightarrow}\; Y(s) = X(s)\cdot H(s)$$
""")

st.markdown("## 5. Função de Transferência")
st.markdown(r"""
$$H(s) = \frac{Y(s)}{X(s)} = \frac{b_m s^m + \cdots + b_0}{s^n + a_{n-1}s^{n-1} + \cdots + a_0}$$

- **Zeros:** raízes do numerador — $H(z_i) = 0$
- **Polos:** raízes do denominador — $|H(p_i)| \to \infty$
- **Estabilidade:** todos os polos no semiplano esquerdo ($\text{Re}(p_i) < 0$)
""")

st.markdown("## 6. Frações Parciais")
st.markdown(r"""
### Raízes reais distintas
$$F(s) = \frac{N(s)}{(s+p_1)(s+p_2)\cdots} = \frac{k_1}{s+p_1} + \frac{k_2}{s+p_2} + \cdots$$
$$k_i = \left.(s+p_i)\,F(s)\right|_{s=-p_i}$$

### Raízes complexas conjugadas
Para $s^2+2\alpha s + (\alpha^2+\beta^2)$, complete o quadrado:
$$F(s) = \frac{A(s+\alpha)+B\beta}{(s+\alpha)^2+\beta^2} \;\overset{\mathcal{L}^{-1}}{\longrightarrow}\; e^{-\alpha t}[A\cos(\beta t)+B\sin(\beta t)]$$

### Raízes repetidas
$$F(s) = \frac{k_r}{(s+p)^r} + \frac{k_{r-1}}{(s+p)^{r-1}} + \cdots$$
$$k_{r-j} = \frac{1}{j!}\frac{d^j}{ds^j}\left[(s+p)^r F(s)\right]_{s=-p}$$
""")

st.markdown("### 🎛️ Explorador — Visualização de Polos e Zeros")
c1, c2 = st.columns([1, 2])
with c1:
    st.markdown("**Insira os polos (parte real, imaginária):**")
    p1r = st.number_input("Polo 1 — real", -5.0, 0.5, -1.0, 0.5, key="p1r")
    p1i = st.number_input("Polo 1 — imag", -5.0, 5.0, 0.0, 0.5, key="p1i")
    p2r = st.number_input("Polo 2 — real", -5.0, 0.5, -2.0, 0.5, key="p2r")
    p2i = st.number_input("Polo 2 — imag", -5.0, 5.0, 1.0, 0.5, key="p2i")
    z1r = st.number_input("Zero 1 — real", -5.0, 2.0, -0.5, 0.5, key="z1r")
    z1i = st.number_input("Zero 1 — imag", -5.0, 5.0, 0.0, 0.5, key="z1i")

poles = [(p1r, p1i), (p1r, -p1i) if p1i != 0 else None,
         (p2r, p2i), (p2r, -p2i) if p2i != 0 else None]
poles = [p for p in poles if p is not None]
zeros = [(z1r, z1i), (z1r, -z1i) if z1i != 0 else None]
zeros = [z for z in zeros if z is not None]

with c2:
    fig = go.Figure()
    fig.add_shape(type="line", x0=0, y0=-5, x1=0, y1=5, line=dict(color="gray", width=1))
    fig.add_shape(type="line", x0=-6, y0=0, x1=2, y1=0, line=dict(color="gray", width=1))
    fig.add_vrect(x0=0, x1=2, fillcolor="rgba(239,68,68,0.07)", layer="below", line_width=0)
    fig.add_vrect(x0=-6, x1=0, fillcolor="rgba(16,185,129,0.07)", layer="below", line_width=0)
    px_vals = [p[0] for p in poles]; py_vals = [p[1] for p in poles]
    zx_vals = [z[0] for z in zeros]; zy_vals = [z[1] for z in zeros]
    fig.add_trace(go.Scatter(x=px_vals, y=py_vals, mode="markers",
                             marker=dict(symbol="x", size=16, color="#d62728", line=dict(width=3)),
                             name="Polos (×)"))
    fig.add_trace(go.Scatter(x=zx_vals, y=zy_vals, mode="markers",
                             marker=dict(symbol="circle-open", size=14, color="#1f77b4", line=dict(width=2.5)),
                             name="Zeros (○)"))
    fig.update_layout(height=360, xaxis=dict(range=[-6,2], title="σ"),
                      yaxis=dict(range=[-5,5], title="jω"),
                      title="Plano s — Polos e Zeros",
                      margin=dict(t=40,b=20,l=10,r=10))
    st.plotly_chart(fig, use_container_width=True)
    all_real = all(abs(p[0]) > 0 and p[1] == 0 for p in poles)
    stable = all(p[0] < 0 for p in poles)
    st.success("✅ Sistema estável — todos os polos no SPE") if stable else st.error("❌ Sistema instável — polo(s) no SPD")

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
