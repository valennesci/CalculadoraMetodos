import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import mostrar_calculadora

def render():
    st.header("Búsqueda de Raíces: Punto Fijo + Aitken")
    st.info("Recuerda ingresar tu función ya despejada en la forma x = g(x).")
    
    col1, col2 = st.columns(2)
    with col1:
        func_str = mostrar_calculadora("aitken", "Ingresa la función g(x):", "sqrt(2 * (x + 2) / pi)")
        tolerancia = st.number_input("Tolerancia:", value=1e-6, format="%.1e")
    with col2:
        x0_str = st.text_input("Valor inicial (x0):", value="1.5")
        max_iter = st.number_input("Máximo de iteraciones:", value=100, step=1)

    if st.button("Ejecutar Punto Fijo", type="primary"):
        x_sym = sp.symbols('x')
        try:
            g_expr = sp.sympify(func_str)
            g = sp.lambdify(x_sym, g_expr, "math")
            x0 = float(sp.sympify(x0_str))
            
            tabla_datos = []
            raiz_encontrada = False
            
            for n in range(1, int(max_iter) + 1):
                x1 = g(x0)
                x2 = g(x1)
                denominador = x2 - 2 * x1 + x0

                if abs(denominador) < 1e-12:
                    st.success(f"✅ Convergencia absoluta alcanzada (denominador cero). Raíz: `{x2:.6f}`")
                    raiz_encontrada = True
                    break

                x_acel = x0 - ((x1 - x0)**2) / denominador
                error = abs(x_acel - x0)
                
                tabla_datos.append({"Paso": n, "x0": x0, "x1": x1, "x2": x2, "x_acel": x_acel, "Error": error})

                if error < tolerancia:
                    st.success(f"✅ **Raíz encontrada:** `{x_acel:.6f}` en {n} pasos.")
                    raiz_encontrada = True
                    break
                x0 = x_acel

            if not raiz_encontrada and len(tabla_datos) > 0:
                st.warning("Se alcanzó el máximo de iteraciones. El método podría estar divergiendo.")
            
            if len(tabla_datos) > 0:
                st.subheader("📊 Tabla de Iteraciones")
                df = pd.DataFrame(tabla_datos)
                format_dict = {col: "{:.12f}" for col in df.select_dtypes(include=['float', 'float64']).columns}
                st.dataframe(df.style.format(format_dict))
                
                st.subheader("📈 Gráfica")
                fig, ax = plt.subplots(figsize=(8, 4))
                margen = 2.0
                x_vals = np.linspace(x_acel - margen, x_acel + margen, 400)
                try:
                    y_vals = [g(val) for val in x_vals]
                    ax.plot(x_vals, y_vals, label='g(x)', color='blue')
                    ax.plot(x_vals, x_vals, label='y = x', color='green', linestyle='--')
                    ax.plot(x_acel, x_acel, 'ro', markersize=8, label=f'Raíz ({x_acel:.4f})')
                    
                    ax.grid(True, linestyle=':', alpha=0.6)
                    ax.legend()
                    st.pyplot(fig)
                except Exception as e:
                    st.warning("No se pudo generar la gráfica de intersección.")
                
        except Exception as e:
            st.error(f"❌ Ocurrió un error matemático: {e}")
