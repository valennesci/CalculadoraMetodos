import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from utils import mostrar_calculadora

def render():
    st.header("Polinomio Interpolador de Lagrange")
    st.info("Soporta ingreso de fracciones (ej. 1/2) y las mantiene exactas en el polinomio.")
    
    tipo_ingreso = st.radio("Método de entrada de datos:", ["Tengo una función f(x)", "Solo tengo puntos (x, y)"])
    
    col1, col2 = st.columns(2)
    tiene_funcion = (tipo_ingreso == "Tengo una función f(x)")
    
    with col1:
        if tiene_funcion:
            func_str = mostrar_calculadora("lagrange", "Ingresa la función f(x):", "exp(x)")
            x_str = st.text_input("Puntos x (separados por coma):", value="1, 2, 3")
        else:
            x_str = st.text_input("Puntos x (separados por coma):", value="1, 2, 3")
            y_str = st.text_input("Puntos y correspondientes:", value="2.718, 7.389, 20.085")
            
    with col2:
        x_eval_str = st.text_input("Punto 'x' a evaluar en el polinomio:", value="1.5")

    if st.button("Generar Polinomio", type="primary"):
        x_sym = sp.symbols('x')
        try:
            x_nodos_sym = [sp.sympify(val.strip()) for val in x_str.split(',')]
            
            if tiene_funcion:
                f_expr = sp.sympify(func_str)
                y_nodos_sym = [f_expr.subs(x_sym, xi) for xi in x_nodos_sym]
            else:
                y_nodos_sym = [sp.sympify(val.strip()) for val in y_str.split(',')]
                if len(x_nodos_sym) != len(y_nodos_sym):
                    st.error("⚠️ Debes ingresar la misma cantidad de valores para x e y.")
                    st.stop()

            n = len(x_nodos_sym) - 1

            polinomio = 0
            for i in range(n + 1):
                L_i = 1
                for j in range(n + 1):
                    if i != j:
                        L_i *= (x_sym - x_nodos_sym[j]) / (x_nodos_sym[i] - x_nodos_sym[j])
                polinomio += y_nodos_sym[i] * L_i

            polinomio_simp = sp.simplify(polinomio)
            
            st.subheader("📜 Polinomio de Lagrange P(x)")
            st.latex(sp.latex(polinomio_simp))

            x_eval_sym = sp.sympify(x_eval_str)
            x_eval = float(x_eval_sym)
            valor_aprox = float(polinomio_simp.subs(x_sym, x_eval_sym))
            
            st.divider()
            st.subheader("🎯 Resultados de la Evaluación")
            
            if tiene_funcion:
                m1, m2, m3 = st.columns(3)
                x_nodos = [float(xi) for xi in x_nodos_sym]
                f = sp.lambdify(x_sym, f_expr, "math")
                
                valor_exacto = f(x_eval)
                error_real = abs(valor_exacto - valor_aprox)
                
                df_n1_expr = sp.diff(f_expr, x_sym, n + 1)
                df_n1 = sp.lambdify(x_sym, df_n1_expr, "math")
                a, b = min(x_nodos), max(x_nodos)
                puntos_malla = [a + i * (b - a) / 1000 for i in range(1001)]
                
                try:
                    M = max(abs(df_n1(pt)) for pt in puntos_malla)
                except Exception:
                    M = 0

                productoria_local = math.prod([abs(x_eval - xi) for xi in x_nodos])
                cota_error_local = (M / math.factorial(n + 1)) * productoria_local
                max_productoria = max(math.prod([abs(pt - xi) for xi in x_nodos]) for pt in puntos_malla)
                cota_error_global = (M / math.factorial(n + 1)) * max_productoria

                m1.metric("P(x) Interpolado", f"{valor_aprox:.6f}")
                m2.metric("f(x) Exacto", f"{valor_exacto:.6f}", delta=f"Error Real: {error_real:.2e}", delta_color="inverse")
                m3.metric("Cota Global", f"{cota_error_global:.2e}")
                
                st.info(f"**Cota de Error Local en x={x_eval}:** {cota_error_local:.6e}")
            else:
                st.metric("P(x) Interpolado", f"{valor_aprox:.6f}")
                st.caption("No se pueden calcular errores teóricos sin la función f(x) original.")

            st.subheader("📈 Gráfica de Interpolación")
            fig, ax = plt.subplots(figsize=(8, 4))
            
            x_nodos_float = [float(xi) for xi in x_nodos_sym]
            y_nodos_float = [float(yi) for yi in y_nodos_sym]
            
            margen = (max(x_nodos_float) - min(x_nodos_float)) * 0.2 if n > 0 else 1
            x_vals = np.linspace(min(x_nodos_float) - margen, max(x_nodos_float) + margen, 400)
            
            P_func = sp.lambdify(x_sym, polinomio_simp, "math")
            y_vals_P = [P_func(val) for val in x_vals]
            
            ax.plot(x_vals, y_vals_P, label='P(x) Interpolado', color='orange')
            if tiene_funcion:
                y_vals_f = [f(val) for val in x_vals]
                ax.plot(x_vals, y_vals_f, label='f(x) Exacta', color='blue', linestyle='--', alpha=0.5)
                
            ax.plot(x_nodos_float, y_nodos_float, 'ko', label='Nodos dados')
            ax.plot(x_eval, valor_aprox, 'ro', markersize=8, label=f'Evaluación ({x_eval})')
            
            ax.axhline(0, color='black', linewidth=0.8)
            ax.grid(True, linestyle=':', alpha=0.6)
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Ocurrió un error: {e}")
