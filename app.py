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
from src.tools import (
    gerar_senha,
    validar_cpf,
    cifra_cesar,
    converter_base,
    analisar_frequencia,
)

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
    seconds = (2**entropy) / 10**10
    return {"entropy": round(entropy, 2), "seconds": seconds, "charset": charset_size}


if check_password():
    st.title(":lock: H-System Security Console")

    st.sidebar.title("Status do Dispositivo")
    stats = get_system_stats()
    st.sidebar.metric("CPU", f"{stats['CPU']}%")
    st.sidebar.metric("Memoria", f"{stats['Memoria']}%")
    st.sidebar.text(f"Host: {stats['Rede']}")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Decifrador",
        "Escada",
        "Senhas",
        "CPF",
        "Cifra",
        "Bases",
        "Texto",
    ])

    with tab1:
        st.header("Decifracao de Mensagens")
        url = st.text_input("URL do Google Docs:", value=DECIPHER_DEFAULT_URL)
        if st.button("Decifrar"):
            resultado = decipher_secret_message(url)
            if resultado:
                st.code(resultado, language=None)
                cipher = get_cipher()
                encrypted = cipher.encrypt(resultado.encode())
                st.info(f"Protecao AES: {encrypted.decode()}")
            else:
                st.error("Nenhum dado encontrado no documento.")

    with tab2:
        st.header("Gerador de Escada")
        entrada = st.text_input("Numeros separados por espaco:")
        if st.button("Gerar Escada"):
            if entrada:
                try:
                    nums = [int(x) for x in entrada.split()]
                    res = create_staircase(nums)
                    if res:
                        for row in res:
                            st.write(f"`{row}`")
                    else:
                        st.warning("Quantidade nao forma escada perfeita.")
                except ValueError:
                    st.error("Digite apenas numeros inteiros.")

    with tab3:
        st.header("Gerador de Senhas Seguras")
        col1, col2 = st.columns(2)
        with col1:
            length = st.slider("Tamanho", 4, 64, 16)
        with col2:
            st.markdown("### Caracteres")
            use_upper = st.checkbox("Maiusculas (A-Z)", True)
            use_lower = st.checkbox("Minusculas (a-z)", True)
            use_digits = st.checkbox("Numeros (0-9)", True)
            use_symbols = st.checkbox("Simbolos (!@#$)", True)

        if st.button("Gerar Senha"):
            if not any([use_upper, use_lower, use_digits, use_symbols]):
                st.error("Selecione ao menos um tipo de caractere.")
            else:
                senha = gerar_senha(length, use_upper, use_lower, use_digits, use_symbols)
                st.code(senha)
                st.info("Senha copiada para a area de transferencia (selecione e copie).")

        st.divider()
        st.header("Auditor de Senhas")
        test_pw = st.text_input("Testar forca de uma senha:", type="password", key="pw_test")
        if test_pw:
            analysis = analyze_password_strength(test_pw)
            assert analysis is not None
            st.metric("Entropia", f"{analysis['entropy']} bits")
            seconds = analysis["seconds"]
            if seconds < 60:
                st.error(f"Critica: quebrada em {seconds:.2f}s")
            elif seconds < 3600:
                st.warning(f"Fraca: quebrada em {seconds / 60:.2f} min")
            elif seconds < 86400 * 365:
                st.info(f"Moderada: quebrada em {seconds / 86400:.2f} dias")
            else:
                st.success(f"Forte: levaria {seconds / (86400 * 365):,.0f} anos")

    with tab4:
        st.header("Validador de CPF")
        cpf = st.text_input("Digite o CPF (com ou sem pontuacao):")
        if st.button("Validar CPF"):
            if cpf:
                if validar_cpf(cpf):
                    st.success("CPF valido!")
                else:
                    st.error("CPF invalido.")
            else:
                st.warning("Digite um CPF.")

    with tab5:
        st.header("Cifra de Cesar")
        texto_cifra = st.text_area("Texto:", height=100)
        col1, col2 = st.columns([1, 1])
        with col1:
            shift = st.number_input("Deslocamento", value=3, step=1)
        with col2:
            modo = st.radio("Modo", ["Cifrar", "Decifrar"], horizontal=True)

        if st.button("Executar"):
            if texto_cifra:
                decrypt = modo == "Decifrar"
                resultado = cifra_cesar(texto_cifra, shift, decrypt)
                st.code(resultado)
            else:
                st.warning("Digite um texto.")

    with tab6:
        st.header("Conversor de Bases Numericas")
        bases = [2, 8, 10, 16]
        value = st.text_input("Valor:", "FF")
        col1, col2 = st.columns(2)
        with col1:
            from_b = st.selectbox("Base de origem", bases, index=3)
        with col2:
            to_b = st.selectbox("Base de destino", bases, index=2)

        if value:
            try:
                result = converter_base(value.strip(), from_b, to_b)
                st.success(f"Resultado: **{result}**")
                st.caption(f"Base {from_b} → Base {to_b}")
            except (ValueError, IndexError):
                st.error("Valor invalido para a base informada.")

    with tab7:
        st.header("Analisador de Frequencia de Texto")
        texto_analise = st.text_area("Cole seu texto aqui:", height=200)
        if st.button("Analisar"):
            if texto_analise.strip():
                result = analisar_frequencia(texto_analise)
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Palavras", result["total_palavras"])
                c2.metric("Palavras Unicas", result["palavras_unicas"])
                c3.metric("Frases", result["total_frases"])
                c4.metric("Caracteres", result["total_caracteres"])

                st.subheader("Palavras mais frequentes")
                for palavra, count in result["palavras_topo"]:
                    st.markdown(f"- **{palavra}**: {count}x")

                st.subheader("Caracteres mais frequentes")
                cols = st.columns(5)
                for i, (char, count) in enumerate(result["caracteres_topo"]):
                    cols[i % 5].metric(f"'{char}'", count)
            else:
                st.warning("Cole um texto para analisar.")

    if st.sidebar.button("Sair"):
        st.session_state["password_correct"] = False
        st.rerun()
