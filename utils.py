import streamlit as st

def page_cfg(title: str, icon: str = "📘"):
    st.set_page_config(page_title=title, page_icon=icon,
                       layout="wide", initial_sidebar_state="expanded")

def header(title: str, subtitle: str = ""):
    st.markdown(f"# {title}")
    if subtitle:
        st.caption(subtitle)
    st.markdown("---")

def secao(titulo: str):
    st.markdown(f"## {titulo}")

def rodape():
    st.markdown("---")
    st.caption("© 2025 Marcus V A Fernandes · IFRN-CNAT · Engenharia de Energia")
