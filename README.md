# RED — Modelagem e Sistemas Lineares (Streamlit)

**Recurso Educacional Digital** · IFRN-CNAT · Marcus V A Fernandes

## Estrutura

```
RED_MSL_streamlit/
├── Home.py                              ← Portal principal
├── pages/
│   ├── 01_Sinais_e_Sistemas_Lineares.py
│   ├── 02_Transformada_de_Laplace.py
│   ├── 03_Dinamica_Ordem_1.py
│   ├── 04_Dinamica_Ordem_2.py
│   ├── 05_Resposta_Frequencia.py
│   ├── 06_Realimentacao_Malha_Fechada.py
│   ├── 07_Estabilidade_Realimentacao.py
│   ├── 08_LGR.py
│   ├── 09_Criterio_Nyquist.py
│   └── 10_Espaco_de_Estados.py
├── .streamlit/
│   └── config.toml                      ← Tema dark
├── requirements.txt
└── README.md
```

---

## 🚀 Deploy — Streamlit Community Cloud (gratuito e permanente)

### Passo 1 — Suba no GitHub
Crie um repositório público e envie toda a pasta `RED_MSL_streamlit/`.

### Passo 2 — Acesse share.streamlit.io
1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte com sua conta GitHub
3. Clique em **New app**
4. Preencha:
   - **Repository:** `SEU_USUARIO/RED_MSL_streamlit`
   - **Branch:** `main`
   - **Main file path:** `Home.py`
5. Clique em **Deploy**

O Streamlit Cloud instala as dependências automaticamente via `requirements.txt`.
Em ~2 minutos o app estará disponível em:
```
https://SEU_USUARIO-red-msl-streamlit-home-xxxxx.streamlit.app
```

> **Vantagem sobre Binder:** o Streamlit Community Cloud **não hiberna** — o app fica sempre disponível e abre instantaneamente.

---

## 💻 Execução local

```bash
pip install -r requirements.txt
streamlit run Home.py
# Acesse: http://localhost:8501
```

---

## 🐳 Docker

```bash
docker build -t red-msl-streamlit .
docker run -p 8501:8501 red-msl-streamlit
```

Dockerfile incluso na pasta `docker/`.
