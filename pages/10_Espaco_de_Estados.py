import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import lti, step as sc_step
from scipy.linalg import expm

st.set_page_config(page_title="Espaço de Estados", page_icon="🔢", layout="wide")
st.title("🔢 Análise no Espaço de Estados")
st.caption("Modelagem e Sistemas Lineares · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

st.markdown("## 1. Descrição Interna vs Externa")
st.markdown(r"""
| | Descrição externa | Descrição interna |
|---|---|---|
| Representação | $H(s) = Y(s)/U(s)$ | $\dot{\mathbf{x}} = A\mathbf{x}+B\mathbf{u}$, $\mathbf{y}=C\mathbf{x}+D\mathbf{u}$ |
| Informação | Entrada-saída (caixa preta) | Todos os estados internos |
| Sistemas MIMO | Matriz $\mathbf{H}(s)$ | Matrizes A, B, C, D |
""")

st.markdown("## 2. Equações de Estado")
st.markdown(r"""
$$\dot{\mathbf{x}}(t) = A\,\mathbf{x}(t) + B\,\mathbf{u}(t)$$
$$\mathbf{y}(t) = C\,\mathbf{x}(t) + D\,\mathbf{u}(t)$$

| Matriz | Dimensão | Descrição |
|---|---|---|
| $A$ | $n\times n$ | Dinâmica do sistema |
| $B$ | $n\times m$ | Influência da entrada nos estados |
| $C$ | $p\times n$ | Saída em função dos estados |
| $D$ | $p\times m$ | Transmissão direta |
""")

st.markdown("## 3. Realização na Forma Direta")
st.markdown(r"""
Para $H(s) = (b_1 s + b_0)/(s^2+a_1 s+a_0)$:

$$A = \begin{bmatrix}0 & 1 \\ -a_0 & -a_1\end{bmatrix}, \quad B = \begin{bmatrix}0\\1\end{bmatrix}, \quad C = \begin{bmatrix}b_0 & b_1\end{bmatrix}, \quad D = [0]$$
""")

st.markdown("## 4. Solução — Matriz de Transição")
st.markdown(r"""
$$\mathbf{x}(t) = e^{At}\,\mathbf{x}(0) + \int_0^t e^{A(t-\tau)}B\,\mathbf{u}(\tau)\,d\tau$$

A **matriz de transição de estados** $\Phi(t) = e^{At}$ satisfaz:
$$\Phi(t) = \mathcal{L}^{-1}\!\left[(sI-A)^{-1}\right]$$
""")

st.markdown("## 5. Controlabilidade e Observabilidade")
st.markdown(r"""
**Controlabilidade:** é possível levar $\mathbf{x}$ de qualquer estado inicial a qualquer estado final em tempo finito.
$$\mathcal{C} = \begin{bmatrix}B & AB & A^2B & \cdots & A^{n-1}B\end{bmatrix}, \quad \text{rank}(\mathcal{C})=n$$

**Observabilidade:** é possível determinar $\mathbf{x}(0)$ a partir de $\mathbf{u}(t)$ e $\mathbf{y}(t)$ em $[0,T]$.
$$\mathcal{O} = \begin{bmatrix}C \\ CA \\ CA^2 \\ \vdots \\ CA^{n-1}\end{bmatrix}, \quad \text{rank}(\mathcal{O})=n$$
""")

st.markdown("## 6. Explorador de Espaço de Estados")
st.info("Insira as matrizes do sistema — linhas separadas por `;`, elementos por `,`")

c1, c2 = st.columns([1, 2])
with c1:
    A_str = st.text_input("Matriz A", "-1,1;-2,-3", key="A_mat")
    B_str = st.text_input("Matriz B", "0;1", key="B_mat")
    C_str = st.text_input("Matriz C", "1,0", key="C_mat")
    D_str = st.text_input("Matriz D (escalar)", "0", key="D_mat")
    st.caption("Exemplo 2ª ordem: A=`-1,1;-2,-3` B=`0;1` C=`1,0` D=`0`")

def parse_mat(s, is_row=False):
    rows = s.strip().split(";")
    return np.array([[float(x) for x in r.split(",")] for r in rows])

try:
    A = parse_mat(A_str)
    B = parse_mat(B_str)
    C = parse_mat(C_str)
    D_val = float(D_str)
    n = A.shape[0]

    eigs = np.linalg.eigvals(A)
    stable = all(e.real < 0 for e in eigs)

    C_ctrl = np.hstack([np.linalg.matrix_power(A, i) @ B for i in range(n)])
    O_obs  = np.vstack([C @ np.linalg.matrix_power(A, i) for i in range(n)])
    ctrl_rank = np.linalg.matrix_rank(C_ctrl)
    obs_rank  = np.linalg.matrix_rank(O_obs)

    t_sim = np.linspace(0, 15, 700)
    sys_ss = lti(A, B, C, [[D_val]])
    _, y_ss = sc_step(sys_ss, T=t_sim)

    with c2:
        fig_ss = make_subplots(rows=1, cols=2, subplot_titles=("Plano s (autovalores)", "Resposta ao degrau"))
        fig_ss.add_shape(type="line", x0=0, y0=-5, x1=0, y1=5, line=dict(color="gray", width=1), row=1, col=1)
        fig_ss.add_shape(type="line", x0=-6, y0=0, x1=2, y1=0, line=dict(color="gray", width=1), row=1, col=1)
        fig_ss.add_vrect(x0=0, x1=2, fillcolor="rgba(239,68,68,0.07)", layer="below", line_width=0, row=1, col=1)
        fig_ss.add_trace(go.Scatter(x=eigs.real, y=eigs.imag, mode="markers",
                                    marker=dict(symbol="x", size=14,
                                                color=["#10b981" if e.real < 0 else "#ef4444" for e in eigs],
                                                line=dict(width=3)),
                                    showlegend=False), row=1, col=1)
        fig_ss.add_trace(go.Scatter(x=t_sim, y=np.clip(y_ss.flatten(), -20, 20), mode="lines",
                                    line=dict(color="#3d8ef0", width=2.5), showlegend=False), row=1, col=2)
        fig_ss.update_xaxes(range=[-6, 2], title_text="σ", row=1, col=1)
        fig_ss.update_yaxes(range=[-5, 5], title_text="jω", row=1, col=1)
        fig_ss.update_xaxes(title_text="t (s)", row=1, col=2)
        fig_ss.update_layout(height=320, margin=dict(t=30,b=20,l=10,r=10))
        st.plotly_chart(fig_ss, use_container_width=True)

    cols = st.columns(4)
    cols[0].metric("Autovalores", str([f"{e:.2f}" for e in eigs]))
    cols[1].metric("Estabilidade", "Estável ✅" if stable else "Instável ❌")
    cols[2].metric("Controlabilidade", f"rank={ctrl_rank}/{n} {'✅' if ctrl_rank==n else '❌'}")
    cols[3].metric("Observabilidade", f"rank={obs_rank}/{n} {'✅' if obs_rank==n else '❌'}")

    with st.expander("Ver função de transferência equivalente"):
        num_tf, den_tf = [], []
        try:
            sys_tf = lti(A, B, C, [[D_val]])
            st.write(f"Zeros: {np.roots(sys_tf.zeros) if len(sys_tf.zeros)>0 else 'nenhum'}")
            st.write(f"Polos: {sys_tf.poles}")
        except Exception:
            st.write("Não foi possível calcular a FT.")

except Exception as e:
    st.error(f"Erro ao processar as matrizes: {e}")
    st.info("Verifique o formato: linhas com `;`, elementos com `,`")

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
