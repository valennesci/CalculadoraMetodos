import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import mostrar_calculadora

def render():
    st.header("Búsqueda de Raíces: Newton-Raphson")
    st.info("El programa calculará la derivada simbólica automáticamente.")
    
    col1, col2 = st.columns(2)
    with col1:
        func_str = mostrar_calculadora("newton", "Ingresa la función f(x):", "(x-1)**2")
        tolerancia = st.number_input("Tolerancia:", value=1e-6, format="%.1e")
    with col2:
        x0_str = st.text_input("Valor inicial (x0):", value="0")
        max_iter = st.number_input("Máximo de iteraciones:", value=100, step=1)

    if st.button("Ejecutar Newton-Raphson", type="primary"):
        x_sym = sp.symbols('x')
        try:
            f_expr = sp.sympify(func_str)
            df_expr = sp.diff(f_expr, x_sym)
            
            st.success(f"**Derivada calculada:** f'(x) = `{df_expr}`")
            
            f = sp.lambdify(x_sym, f_expr, "math")
            df = sp.lambdify(x_sym, df_expr, "math")
            x0 = float(sp.sympify(x0_str))
            
            tabla_datos = []
            raiz_encontrada = False
            
            for n in range(1, int(max_iter) + 1):
                fx = f(x0)
                dfx = df(x0)

                if abs(dfx) < 1e-12:
                    st.error(f"⚠️ La derivada es cero o muy cercana a cero en x = {x0}. El método falla.")
                    break

                x1 = x0 - (fx / dfx)
                error = abs(x1 - x0)
                
                tabla_datos.append({"Paso": n, "x_n": x0, "f(x_n)": fx, "f'(x_n)": dfx, "x_{n+1}": x1, "Error": error})

                if error < tolerancia:
                    st.success(f"✅ **Raíz encontrada:** `{x1:.6f}` en {n} pasos.")
                    raiz_encontrada = True
                    break
                
                x0 = x1

            if not raiz_encontrada and len(tabla_datos) > 0:
                st.warning("Se alcanzó el máximo de iteraciones. El método podría estar divergiendo.")
            
            if len(tabla_datos) > 0:
                st.subheader("📊 Tabla de Iteraciones")
                st.dataframe(pd.DataFrame(tabla_datos))
                
                st.subheader("📈 Gráfica")
                fig, ax = plt.subplots(figsize=(8, 4))
                margen = 2.0
                x_vals = np.linspace(x1 - margen, x1 + margen, 400)
                y_vals = [f(val) for val in x_vals]
                ax.plot(x_vals, y_vals, label=f'f(x)', color='blue')
                ax.axhline(0, color='black', linewidth=1)
                
                x_prev = x0
                fx_prev = f(x_prev)
                dfx_prev = df(x_prev)
                tangent_y = [fx_prev + dfx_prev * (val - x_prev) for val in x_vals]
                ax.plot(x_vals, tangent_y, 'g--', label='Última Tangente', alpha=0.7)
                ax.plot(x_prev, fx_prev, 'go', markersize=6)
                
                ax.plot(x1, 0, 'ro', markersize=8, label=f'Raíz ({x1:.4f})')
                ax.grid(True, linestyle=':', alpha=0.6)
                ax.legend()
                st.pyplot(fig)
                
        except Exception as e:
            st.error(f"❌ Ocurrió un error: {e}")
