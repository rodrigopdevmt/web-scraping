import os
import re
import math
import socket
from typing import Optional

import streamlit as st
import psutil
from cryptography.fernet import Fernet

from src.config import PASSWORD, DECIPHER_DEFAULT_URL
from src.decipher import decipher_secret_message
from src.staircase import create_staircase

st.set_page_config(page_title="H-System Security Console", layout="wide", page_icon=":lock:")


def check_password() -> bool:
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.title("Acesso Restrito")
        password = st.text_input("Senha do Sistema", type="password")
        if st.button("Entrar"):
            if password == PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Senha incorreta")
        return False
    return True


def get_cipher() -> Fernet:
    if "cipher_key" not in st.session_state:
        st.session_state["cipher_key"] = Fernet.generate_key()
    return Fernet(st.session_state["cipher_key"])


def get_system_stats() -> dict[str, object]:
    return {
        "CPU": psutil.cpu_percent(),
        "Memoria": psutil.virtual_memory().percent,
        "Rede": socket.gethostname(),
    }


def analyze_password_strength(password: str) -> Optional[dict[str, object]]:
    if not password:
        return None

    charset_size = 0
    if re.search(r"[a-z]", password):
        charset_size += 26
    if re.search(r"[A-Z]", password):
        charset_size += 26
    if re.search(r"[0-9]", password):
        charset_size += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        charset_size += 32

    length = len(password)
    entropy = length * math.log2(charset_size) if charset_size > 0 else 0
    attempts_per_sec = 10**10
    seconds_to_crack = (2**entropy) / attempts_per_sec

    return {
        "entropy": round(entropy, 2),
        "seconds": seconds_to_crack,
        "charset": charset_size,
    }


if check_password():
    st.title(":lock: H-System Security Console")

    st.sidebar.title("Status do Dispositivo")
    stats = get_system_stats()
    st.sidebar.metric("Uso de CPU", f"{stats['CPU']}%")
    st.sidebar.metric("Uso de Memória", f"{stats['Memoria']}%")
    st.sidebar.text(f"Host: {stats['Rede']}")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Decifrador",
        "Auditor de Senhas",
        "Utilitarios",
        "Sobre",
    ])

    with tab1:
        st.header("Decifracao de Mensagens")
        url = st.text_input("URL do Google Docs:", value=DECIPHER_DEFAULT_URL)
        if st.button("Decifrar Agora"):
            resultado = decipher_secret_message(url)
            if resultado:
                st.code(resultado, language=None)
                cipher = get_cipher()
                encrypted = cipher.encrypt(resultado.encode())
                st.info(f" Protecao AES: {encrypted.decode()}")
            else:
                st.error("Nenhum dado encontrado no documento.")

    with tab2:
        st.header("Auditoria de Robustez de Senha")
        st.write("Teste quanto tempo levaria para uma senha ser quebrada por forca bruta.")

        test_pw = st.text_input("Digite uma senha para testar:", type="password")
        if test_pw:
            analysis = analyze_password_strength(test_pw)
            assert analysis is not None
            st.metric("Entropia (Bits)", f"{analysis['entropy']}")

            seconds = analysis["seconds"]
            if seconds < 60:
                st.error(f"Critica: Quebrada em {seconds:.2f} segundos!")
            elif seconds < 3600:
                st.warning(f"Fraca: Quebrada em {seconds / 60:.2f} minutos.")
            elif seconds < 86400 * 365:
                st.info(f"Moderada: Quebrada em {seconds / 86400:.2f} dias.")
            else:
                st.success(f"Forte: Levaria {seconds / (86400 * 365):,.0f} anos para quebrar!")

    with tab3:
        st.header("Gerador de Escada")
        entrada = st.text_input("Digite os numeros separados por espaco:")
        if st.button("Gerar"):
            if entrada:
                try:
                    nums = [int(x) for x in entrada.split()]
                    res = create_staircase(nums)
                    if res:
                        for row in res:
                            st.write(f"`{row}`")
                    else:
                        st.warning("Quantidade de numeros nao forma uma escada perfeita.")
                except ValueError:
                    st.error("Erro: Digite apenas numeros inteiros.")

    with tab4:
        st.header("Sobre o Sistema")
        st.markdown("""
        **H-System Security Console** - v1.0.0

        Desenvolvido por **Rodrigo Dev MT**

        Funcionalidades:
        - Decifrador de mensagens ocultas em Google Docs
        - Auditor de forca de senhas (entropia)
        - Gerador de escada numerica
        - Criptografia AES dos resultados
        """)

    if st.sidebar.button("Sair"):
        st.session_state["password_correct"] = False
        st.rerun()
