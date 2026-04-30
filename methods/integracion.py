import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import mostrar_calculadora

def render():
    st.header("Cálculo de Área: Integración Numérica")
    
    col1, col2 = st.columns(2)
    with col1:
        metodo = st.selectbox("Elige el método:", 
                              ["1. Regla del Trapecio (Simple)", 
                               "2. Regla del Trapecio (Compuesta)", 
                               "3. Regla de Simpson 1/3 (Compuesta)", 
                               "4. Regla de Simpson 3/8 (Compuesta)"])
        func_str = mostrar_calculadora("integracion", "Función f(x) a integrar:", "(sin(x))/x")
        
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            a_str = st.text_input("Límite inferior (a):", value="0")
        with col_b:
            b_str = st.text_input("Límite superior (b):", value="1")
            
        if "Simple" in metodo:
            n = 1
            st.info("Trapecio Simple usa n=1 por defecto.")
        else:
            n = st.number_input("Número de subintervalos (n):", min_value=1, value=6, step=1)

    if st.button("Calcular Integral", type="primary"):
        x_sym = sp.symbols('x')
        
        if "Simpson 1/3" in metodo and n % 2 != 0:
            st.error("❌ Error matemático: Para Simpson 1/3, 'n' debe ser un número par.")
            st.stop()
        if "Simpson 3/8" in metodo and n % 3 != 0:
            st.error("❌ Error matemático: Para Simpson 3/8, 'n' debe ser múltiplo de 3.")
            st.stop()
            
        try:
            f_expr = sp.sympify(func_str)
            f_rapida = sp.lambdify(x_sym, f_expr, "math")
            a = float(sp.sympify(a_str))
            b = float(sp.sympify(b_str))
            
            def f(valor):
                try:
                    return f_rapida(valor)
                except (ZeroDivisionError, ValueError):
                    st.toast(f"Singularidad en x={valor}. Límite aplicado.", icon="⚠️")
                    return float(sp.limit(f_expr, x_sym, valor))

            h = (b - a) / n

            tabla_datos = []
            for i in range(n + 1):
                xi = a + i * h
                fxi = f(xi)
                tabla_datos.append({"n (índice)": i, "X_n": xi, "F(X_n)": fxi})

            integral = 0
            if "Trapecio (Simple)" in metodo:
                integral = (h / 2) * (f(a) + f(b))
            elif "Trapecio (Compuesta)" in metodo:
                suma_interna = sum(f(a + i * h) for i in range(1, n))
                integral = (h / 2) * (f(a) + 2 * suma_interna + f(b))
            elif "Simpson 1/3" in metodo:
                suma_impares = sum(f(a + i * h) for i in range(1, n, 2))
                suma_pares = sum(f(a + i * h) for i in range(2, n, 2))
                integral = (h / 3) * (f(a) + 4 * suma_impares + 2 * suma_pares + f(b))
            elif "Simpson 3/8" in metodo:
                suma = f(a) + f(b)
                for i in range(1, n):
                    if i % 3 == 0:
                        suma += 2 * f(a + i * h)
                    else:
                        suma += 3 * f(a + i * h)
                integral = (3 * h / 8) * suma

            orden_derivada = 2 if "Trapecio" in metodo else 4
            df_expr = sp.diff(f_expr, x_sym, orden_derivada)
            df_func = sp.lambdify(x_sym, df_expr, "math")

            puntos_malla = [a + i * (b - a) / 1000 for i in range(1001)]
            try:
                M = max(abs(df_func(pt)) for pt in puntos_malla)
            except Exception:
                M = 0

            if "Trapecio (Simple)" in metodo:
                cota_error = ((b - a)**3 / 12) * M
            elif "Trapecio (Compuesta)" in metodo:
                cota_error = ((b - a) * h**2 / 12) * M
            elif "Simpson 1/3" in metodo:
                cota_error = ((b - a) * h**4 / 180) * M
            elif "Simpson 3/8" in metodo:
                cota_error = ((b - a) * h**4 / 80) * M

            try:
                integral_exacta_sym = sp.integrate(f_expr, (x_sym, a, b))
                integral_exacta = float(integral_exacta_sym)
                error_real = abs(integral_exacta - integral)
                tiene_exacta = True
            except Exception:
                tiene_exacta = False

            st.divider()
            st.subheader("🎯 Resultados")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Valor Aproximado", f"{integral:.8f}")
            m2.metric("Cota Máx. Error (Truncamiento)", f"{cota_error:.2e}")
            if tiene_exacta:
                m3.metric("Valor Exacto (Analítico)", f"{integral_exacta:.8f}", delta=f"Error Real: {error_real:.2e}", delta_color="inverse")
            else:
                m3.metric("Valor Exacto", "No calculable analíticamente")

            col_tabla, col_grafico = st.columns([1, 2])
            with col_tabla:
                st.write("**Tabla de Valores (Xn, Yn)**")
                df = pd.DataFrame(tabla_datos)
                format_dict = {col: "{:.12f}" for col in df.select_dtypes(include=['float', 'float64']).columns}
                st.dataframe(df.style.format(format_dict))

            with col_grafico:
                st.write("**Área bajo la curva**")
                fig, ax = plt.subplots(figsize=(6, 4))
                x_vals = np.linspace(a - 0.2, b + 0.2, 400)
                y_vals = np.array([f(val) for val in x_vals]) 
                
                ax.plot(x_vals, y_vals, color='red', label=f'f(x) = {func_str}')
                x_fill = np.linspace(a, b, 200)
                y_fill = np.array([f(val) for val in x_fill])
                ax.fill_between(x_fill, y_fill, color='orange', alpha=0.3, label='Área Calculada')
                
                ax.axhline(0, color='black', linewidth=0.8)
                ax.grid(True, linestyle=':', alpha=0.6)
                ax.legend()
                st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Ocurrió un error en los cálculos: {e}")
