import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# =====================================================================
# COMPONENTE CENTRAL: TECLADO MATEMÁTICO
# =====================================================================
def mostrar_calculadora(key_prefix, label, default_func=""):
    input_key = f"input_{key_prefix}"
    if input_key not in st.session_state:
        st.session_state[input_key] = default_func

    def agregar_simbolo(simbolo):
        st.session_state[input_key] += simbolo
    def limpiar_ecuacion():
        st.session_state[input_key] = ""

    func_str = st.text_input(label, key=input_key)
    
    if func_str:
        try:
            expr = sp.sympify(func_str)
            symbols = list(expr.free_symbols)
            symbols_str = ", ".join(sorted([str(s) for s in symbols]))
            if symbols_str:
                st.latex(rf"f({symbols_str}) = {sp.latex(expr)}")
            else:
                st.latex(rf"f(x) = {sp.latex(expr)}")
        except Exception:
            pass

    with st.expander("⌨️ Abrir Teclado Matemático"):
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.button("7", on_click=agregar_simbolo, args=("7",), key=f"{key_prefix}_7", use_container_width=True)
            st.button("4", on_click=agregar_simbolo, args=("4",), key=f"{key_prefix}_4", use_container_width=True)
            st.button("1", on_click=agregar_simbolo, args=("1",), key=f"{key_prefix}_1", use_container_width=True)
            st.button("0", on_click=agregar_simbolo, args=("0",), key=f"{key_prefix}_0", use_container_width=True)
        with c2:
            st.button("8", on_click=agregar_simbolo, args=("8",), key=f"{key_prefix}_8", use_container_width=True)
            st.button("5", on_click=agregar_simbolo, args=("5",), key=f"{key_prefix}_5", use_container_width=True)
            st.button("2", on_click=agregar_simbolo, args=("2",), key=f"{key_prefix}_2", use_container_width=True)
            st.button(".", on_click=agregar_simbolo, args=(".",), key=f"{key_prefix}_dot", use_container_width=True)
        with c3:
            st.button("9", on_click=agregar_simbolo, args=("9",), key=f"{key_prefix}_9", use_container_width=True)
            st.button("6", on_click=agregar_simbolo, args=("6",), key=f"{key_prefix}_6", use_container_width=True)
            st.button("3", on_click=agregar_simbolo, args=("3",), key=f"{key_prefix}_3", use_container_width=True)
            st.button("pi", on_click=agregar_simbolo, args=("pi",), key=f"{key_prefix}_pi", use_container_width=True)
        with c4:
            st.button("+", on_click=agregar_simbolo, args=("+",), key=f"{key_prefix}_mas", use_container_width=True)
            st.button("-", on_click=agregar_simbolo, args=("-",), key=f"{key_prefix}_menos", use_container_width=True)
            st.button("*", on_click=agregar_simbolo, args=("*",), key=f"{key_prefix}_por", use_container_width=True)
            st.button("/", on_click=agregar_simbolo, args=("/",), key=f"{key_prefix}_div", use_container_width=True)
        with c5:
            st.button("x", on_click=agregar_simbolo, args=("x",), key=f"{key_prefix}_x", use_container_width=True)
            st.button("y", on_click=agregar_simbolo, args=("y",), key=f"{key_prefix}_y", use_container_width=True)
            st.button("sin()", on_click=agregar_simbolo, args=("sin(",), key=f"{key_prefix}_sin", use_container_width=True)
            st.button("cos()", on_click=agregar_simbolo, args=("cos(",), key=f"{key_prefix}_cos", use_container_width=True)
        
        c6, c7, c8, c9 = st.columns(4)
        with c6:
            st.button("(", on_click=agregar_simbolo, args=("(",), key=f"{key_prefix}_pa", use_container_width=True)
        with c7:
            st.button(")", on_click=agregar_simbolo, args=(")",), key=f"{key_prefix}_pc", use_container_width=True)
        with c8:
            st.button("exp()", on_click=agregar_simbolo, args=("exp(",), key=f"{key_prefix}_exp", use_container_width=True)
        with c9:
            st.button("🧹 Borrar Todo", on_click=limpiar_ecuacion, key=f"{key_prefix}_clear", use_container_width=True)
            
    return func_str
