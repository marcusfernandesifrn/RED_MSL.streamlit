# Instruções de montagem do repositório RED-MSL

## Estrutura de arquivos

```
seu-repo/
├── Home.py                          ← Página inicial (substituir)
├── requirements.txt                 ← Dependências (substituir)
├── pages/
│   ├── 01_Sinais_e_Sistemas_Lineares.py   ← conteúdo de sinais_e_sistemas_lineares.py
│   ├── 02_Transformada_de_Laplace.py      ← conteúdo de transformada_de_laplace.py
│   ├── 03_Dinamica_Ordem_1.py             ← conteúdo de dinamica_sistemas_ordem_1.py
│   ├── 04_Dinamica_Ordem_2.py             ← conteúdo de dinamica_sistemas_ordem_2.py
│   ├── 05_Realimentacao_Malha_Fechada.py  ← conteúdo de realimentacao_malha_fechada.py
│   ├── 06_Realimentacao_LGR.py            ← conteúdo de realimentacao_lgr.py
│   ├── 07_Estabilidade_Realimentacao.py   ← conteúdo de estabilidade_realimentacao.py
│   ├── 08_Resposta_Frequencia.py          ← conteúdo de resposta_frequencia.py
│   ├── 09_Criterio_Nyquist.py             ← conteúdo de criterio_nyquist.py
│   └── 10_Espaco_de_Estados.py            ← conteúdo de espaco_de_estados.py
```

## Passos

1. Substitua `Home.py` pelo arquivo gerado `Home.py`
2. Substitua `requirements.txt` pelo arquivo atualizado
3. Para cada arquivo em `pages/`, substitua o conteúdo pelo arquivo `.py` correspondente gerado nas sessões anteriores
4. Faça commit e push — o Streamlit Cloud recarrega automaticamente

## Mapeamento de arquivos antigos → novos

| Arquivo antigo | Arquivo novo | Módulo |
|---|---|---|
| `pages/05_Resposta_Frequencia.py` | `pages/08_Resposta_Frequencia.py` | Bode |
| `pages/06_Realimentacao_Malha_Fechada.py` | `pages/05_Realimentacao_Malha_Fechada.py` | Realimentação MF |
| `pages/07_Estabilidade_Realimentacao.py` | `pages/07_Estabilidade_Realimentacao.py` | Estabilidade |
| `pages/08_LGR.py` | `pages/06_Realimentacao_LGR.py` | LGR |
| `pages/09_Criterio_Nyquist.py` | `pages/09_Criterio_Nyquist.py` | Nyquist |

## Ícones por módulo (únicos)

| Módulo | Ícone |
|---|---|
| Sinais e Sistemas | 📡 |
| Transformada de Laplace | 🌀 |
| Dinâmica Ordem 1 | 📈 |
| Dinâmica Ordem 2 | 📊 |
| Realimentação MF | 🔄 |
| Realimentação LGR | 📍 |
| Estabilidade | ⚖️ |
| Resposta em Frequência (Bode) | 📉 |
| Critério de Nyquist | 🔁 |
| Espaço de Estados | 🧮 |
