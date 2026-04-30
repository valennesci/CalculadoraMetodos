import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import mostrar_calculadora

def render():
    st.header("Búsqueda de Raíces: Método de Bisección")
    
    col1, col2 = st.columns(2)
    with col1:
        func_str = mostrar_calculadora("bisec", "Ingresa la función f(x):", "x**3 - x - 2")
        tolerancia = st.number_input("Tolerancia (Error máximo):", value=1e-6, format="%.1e")
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            a_str = st.text_input("Límite inferior (a):", value="1")
        with col_b:
            b_str = st.text_input("Límite superior (b):", value="2")
        max_iter = st.number_input("Máximo de iteraciones:", value=100, step=1)

    if st.button("Calcular Raíz", type="primary"):
        x_sym = sp.symbols('x')
        try:
            f_expr = sp.sympify(func_str)
            f = sp.lambdify(x_sym, f_expr, "math")
            a = float(sp.sympify(a_str))
            b = float(sp.sympify(b_str))
            
            if f(a) * f(b) >= 0:
                st.error("⚠️ Error (Bolzano): f(a) y f(b) deben tener signos opuestos en ese intervalo.")
            else:
                tabla_datos = []
                m = a
                progress_bar = st.progress(0)
                
                for n in range(1, int(max_iter) + 1):
                    m = (a + b) / 2
                    fm = f(m)
                    error_max = (b - a) / 2
                    
                    tabla_datos.append({"Paso": n, "a": a, "m (raíz)": m, "b": b, "f(m)": fm, "Error máx": error_max})
                    
                    if error_max < tolerancia:
                        progress_bar.progress(100)
                        break
                        
                    if f(a) * fm < 0:
                        b = m
                    else:
                        a = m
                    progress_bar.progress(min(n / max_iter, 1.0))

                st.success(f"✅ **Raíz encontrada:** `{m:.6f}` en {len(tabla_datos)} pasos.")
                
                st.subheader("📊 Tabla de Iteraciones")
                df = pd.DataFrame(tabla_datos)
                format_dict = {col: "{:.12f}" for col in df.select_dtypes(include=['float', 'float64']).columns}
                st.dataframe(df.style.format(format_dict))

                st.subheader("📈 Visualización de la Función")
                fig, ax = plt.subplots(figsize=(8, 4))
                a_ini, b_ini = float(sp.sympify(a_str)), float(sp.sympify(b_str))
                margen = (b_ini - a_ini) * 0.5
                x_vals = np.linspace(a_ini - margen, b_ini + margen, 400)
                y_vals = [f(val) for val in x_vals]
                
                ax.plot(x_vals, y_vals, label=f'f(x) = {func_str}', color='#1f77b4')
                ax.axhline(0, color='black', linewidth=1)
                ax.axvline(a_ini, color='red', linestyle='--', alpha=0.5, label='Límite a')
                ax.axvline(b_ini, color='green', linestyle='--', alpha=0.5, label='Límite b')
                ax.plot(m, 0, 'ko', markersize=8, label=f'Raíz ({m:.4f})')
                
                ax.grid(True, linestyle=':', alpha=0.6)
                ax.legend()
                st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Ocurrió un error: {e}")
