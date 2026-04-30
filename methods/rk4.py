import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import mostrar_calculadora

def render():
    st.header("Resolución de EDOs: Runge-Kutta 4 (RK4)")
    st.info("Resuelve ecuaciones diferenciales de la forma dy/dx = f(x, y)")
    
    col1, col2 = st.columns(2)
    with col1:
        func_str = mostrar_calculadora("rk4", "Ingresa f(x, y):", "x - y")
        x0_str = st.text_input("Valor inicial x0:", value="0")
        y0_str = st.text_input("Valor inicial y0:", value="1")
    with col2:
        h_str = st.text_input("Tamaño de paso (h):", value="0.1")
        xf_str = st.text_input("Valor final xf a evaluar:", value="1.0")
        exact_str = st.text_input("Solución Exacta y(x) (Opcional, para comparar):", value="x - 1 + 2*exp(-x)")

    if st.button("Ejecutar RK4", type="primary"):
        x_sym, y_sym = sp.symbols('x y')
        try:
            f_expr = sp.sympify(func_str)
            f = sp.lambdify((x_sym, y_sym), f_expr, "math")
            
            x0 = float(sp.sympify(x0_str))
            y0 = float(sp.sympify(y0_str))
            h = float(sp.sympify(h_str))
            xf = float(sp.sympify(xf_str))
            
            if h == 0 or (xf - x0) * h < 0:
                st.error("⚠️ El paso 'h' no es válido para llegar desde x0 hasta xf.")
                st.stop()
                
            n_steps = int(abs((xf - x0) / h))
            
            tabla_datos = []
            x_act, y_act = x0, y0
            
            for i in range(n_steps + 1):
                k1 = f(x_act, y_act)
                k2 = f(x_act + h / 2, y_act + k1 * h / 2)
                k3 = f(x_act + h / 2, y_act + k2 * h / 2)
                k4 = f(x_act + h, y_act + k3 * h)
                
                y_sig = y_act + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
                
                tabla_datos.append({
                    "n": i, "x_n": x_act, "y_n": y_act,
                    "k1": k1, "k2": k2, "k3": k3, "k4": k4,
                    "y_{n+1}": y_sig
                })
                
                x_sig = x_act + h
                x_act, y_act = x_sig, y_sig

            df_resultados = pd.DataFrame(tabla_datos)
            
            tiene_exacta = False
            if exact_str.strip() != "":
                try:
                    exact_expr = sp.sympify(exact_str)
                    exact_f = sp.lambdify(x_sym, exact_expr, "math")
                    df_resultados['y_Exacta'] = df_resultados['x_n'].apply(exact_f)
                    df_resultados['Error Absoluto'] = abs(df_resultados['y_Exacta'] - df_resultados['y_n'])
                    tiene_exacta = True
                except Exception as e:
                    st.warning(f"No se pudo parsear la solución exacta: {e}")

            st.success(f"✅ **Valor final calculado:** $y({x_act:.4f}) \approx {y_act:.6f}$")
            
            st.subheader("📊 Tabla de Iteraciones (RK4)")
            format_dict = {col: "{:.12f}" for col in df_resultados.select_dtypes(include=['float', 'float64']).columns}
            st.dataframe(df_resultados.style.format(format_dict))
            
            st.subheader("📈 Gráfica de la Solución")
            fig, ax = plt.subplots(figsize=(8, 4))
            
            x_vals = df_resultados['x_n'].values
            y_rk4 = df_resultados['y_n'].values
            
            ax.plot(x_vals, y_rk4, 'b-o', label='RK4 (Aproximación)', markersize=4)
            
            if tiene_exacta:
                x_dense = np.linspace(x0, xf, max(200, n_steps * 10))
                y_dense = [exact_f(val) for val in x_dense]
                ax.plot(x_dense, y_dense, 'r-', alpha=0.6, label='Solución Exacta')
                
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True, linestyle=':', alpha=0.6)
            ax.legend()
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"❌ Ocurrió un error matemático: {e}")
