import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import lti, lsim

st.set_page_config(page_title="Estabilidade com Realimentação", page_icon="⚖️", layout="wide")
st.title("⚖️ Estabilidade com Realimentação")
st.caption("Modelagem e Sistemas Lineares · IFRN-CNAT · Marcus V A Fernandes")
st.markdown("---")

st.markdown("## 1. Conceitos de Estabilidade")
st.markdown(r"""
| Tipo | Comportamento após perturbação | Polos |
|---|---|---|
| **Estável** (assintótico) | Retorna ao equilíbrio | Todos no SPE: $\text{Re}(p_i)<0$ |
| **Marginalmente estável** | Oscila com amplitude constante | Polo(s) no eixo imaginário |
| **Instável** | Diverge indefinidamente | Polo(s) no SPD: $\text{Re}(p_i)>0$ |
""")

st.markdown("## 2. Classificação pelos Polos")
st.markdown(r"""
O modo natural associado ao polo $s_i = \sigma_i + j\omega_i$ é $e^{s_i t}$:

| Polo | $\sigma_i$ | Modo |
|---|---|---|
| SPE real | $<0$ | Decaimento exponencial |
| SPE complexo | $<0$ | Oscilação amortecida |
| Eixo Im (simples) | $=0$ | Senoide pura |
| SPD real | $>0$ | Crescimento exponencial |
| SPD complexo | $>0$ | Oscilação crescente |
""")

st.markdown("## 3. Critério de Routh-Hurwitz")
st.markdown(r"""
Para $D(s) = a_n s^n + a_{n-1}s^{n-1}+\cdots+a_0$:

**Condição necessária:** todos os coeficientes devem ter o **mesmo sinal** e ser **não nulos**.

**Tabela de Routh:** construída a partir dos coeficientes — o sistema é estável se e somente se **todos os elementos da primeira coluna** têm o mesmo sinal. O número de trocas de sinal = número de polos no SPD.
""")

st.markdown("### 🎛️ Calculadora de Routh-Hurwitz")
c1, c2 = st.columns([1, 2])
with c1:
    den_routh = st.text_input("Polinômio característico (ordem decrescente)",
                               "1, 10, 31, 1030", key="routh_den")
    st.caption("Ex: `1, 10, 31, 1030` → s³ + 10s² + 31s + 1030")

try:
    coeffs = list(map(float, den_routh.split(",")))
    n = len(coeffs)
    with c2:
        if any(c <= 0 for c in coeffs) or any(c > 0 for c in coeffs) and any(c < 0 for c in coeffs):
            st.error("❌ Condição necessária violada: coeficientes com sinais diferentes → sistema instável.")
        else:
            rows = []
            row0 = coeffs[0::2]
            row1 = coeffs[1::2]
            max_len = max(len(row0), len(row1))
            row0 += [0] * (max_len - len(row0))
            row1 += [0] * (max_len - len(row1))
            rows.append(row0)
            rows.append(row1)
            for i in range(2, n):
                prev = rows[-2]; curr = rows[-1]
                if abs(curr[0]) < 1e-12:
                    curr[0] = 1e-8
                new_row = []
                for j in range(len(curr)-1):
                    val = (curr[0]*prev[j+1] - prev[0]*curr[j+1]) / curr[0] if j+1 < len(prev) else 0
                    new_row.append(val)
                new_row += [0]
                rows.append(new_row[:max_len])
            first_col = [r[0] for r in rows[:n]]
            sign_changes = sum(1 for i in range(1, len(first_col))
                               if first_col[i-1] * first_col[i] < 0)
            table_data = []
            for i, row in enumerate(rows[:n]):
                table_data.append({"Linha": f"s^{n-1-i}"} |
                                   {f"Col {j+1}": f"{v:.4g}" for j, v in enumerate(row)})
            import pandas as pd
            st.dataframe(pd.DataFrame(table_data), use_container_width=True)
            if sign_changes == 0:
                st.success(f"✅ Sistema **estável** — 1ª coluna: {[f'{v:.3g}' for v in first_col]}")
            else:
                st.error(f"❌ Sistema **instável** — {sign_changes} polo(s) no SPD")
except Exception as e:
    st.error(f"Erro: {e}")

st.markdown("## 4. Explorador — Ganho Crítico e Região de Estabilidade")
st.markdown(r"""
Para $G(s) = k/[s(s+a_1)(s+a_2)]$, o critério de Routh fornece:
$$k_{crit} = a_1\,a_2\,(a_1+a_2)$$
""")

c1, c2 = st.columns([1, 2])
with c1:
    a1_v = st.slider("$a_1$", 1.0, 10.0, 7.0, 0.5, key="a1_est")
    a2_v = st.slider("$a_2$", 1.0, 10.0, 3.0, 0.5, key="a2_est")
    k_v  = st.slider("Ganho $k$", 0.1, 300.0, 50.0, 1.0, key="k_est")

k_crit = a1_v * a2_v * (a1_v + a2_v)
t_est = np.linspace(0, 20, 2000)
den_mf = [1, a1_v+a2_v, a1_v*a2_v, k_v]
try:
    sys_est = lti([k_v], den_mf)
    ref_est = np.ones_like(t_est)
    _, y_est, _ = lsim(sys_est, ref_est, t_est)
    y_est = np.clip(y_est, -100, 100)
    ok = k_v < k_crit
except Exception:
    y_est = np.zeros_like(t_est)
    ok = False

with c2:
    fig_est = go.Figure()
    fig_est.add_trace(go.Scatter(x=t_est, y=y_est, mode="lines",
                                  line=dict(color="#3d8ef0" if ok else "#ef4444", width=2.5),
                                  name="y(t)"))
    fig_est.add_hline(y=1, line_dash="dash", line_color="gray")
    fig_est.update_layout(height=300, xaxis_title="t (s)", yaxis_title="y(t)",
                          title=f"k={k_v:.1f} | k_crit={k_crit:.1f} | {'ESTÁVEL' if ok else 'INSTÁVEL'}",
                          margin=dict(t=40,b=20,l=10,r=10))
    st.plotly_chart(fig_est, use_container_width=True)

st.success(f"✅ k_crit = {k_crit:.2f}") if ok else st.error(f"❌ k = {k_v:.1f} > k_crit = {k_crit:.2f}")

st.markdown("---")
st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
