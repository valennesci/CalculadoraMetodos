import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from utils import mostrar_calculadora

def render():
    st.header("Integración por Método de Monte Carlo")
    
    dimension = st.radio("Dimensión de la integral:", ["1D (Una variable: x)", "2D (Dos variables: x, y)"], horizontal=True)
    es_2d = "2D" in dimension

    col1, col2 = st.columns(2)
    with col1:
        default_f = "exp(x+y)" if es_2d else "exp(-x**2)"
        func_str = mostrar_calculadora("mc", "Función a integrar:", default_f)
        n_puntos = st.number_input("Número de puntos aleatorios (n):", min_value=100, max_value=10000000, value=50000, step=1000)
        
        col_sem, col_conf = st.columns(2)
        with col_sem:
            semilla = st.number_input("Semilla (Seed):", value=42, step=1)
        with col_conf:
            confianza = st.selectbox("Nivel de Confianza:", [0.90, 0.95, 0.99], index=1)
            z_map = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
            z_val = z_map[confianza]
        
    with col2:
        if es_2d:
            st.write("**Límites X (Diferencial Exterior)**")
            c_xa, c_xb = st.columns(2)
            xa_str = c_xa.text_input("Límite inf. (x_a):", value="0")
            xb_str = c_xb.text_input("Límite sup. (x_b):", value="2")
            
            st.write("**Límites Y (Diferencial Interior)**")
            c_ya, c_yb = st.columns(2)
            ya_str = c_ya.text_input("Límite inf. (y_a):", value="1")
            yb_str = c_yb.text_input("Límite sup. (y_b):", value="3")
        else:
            c_a, c_b = st.columns(2)
            a_str = c_a.text_input("Límite inferior (a):", value="0")
            b_str = c_b.text_input("Límite superior (b):", value="1")

    if st.button("Ejecutar Simulación Científica", type="primary"):
        np.random.seed(int(semilla))
        x_sym, y_sym = sp.symbols('x y')
        
        try:
            f_expr = sp.sympify(func_str)
            
            if not es_2d:
                f_rapida = sp.lambdify(x_sym, f_expr, "numpy") 
                a, b = float(sp.sympify(a_str)), float(sp.sympify(b_str))
                
                x_rand = np.random.uniform(a, b, int(n_puntos))
                evaluaciones = np.asarray(f_rapida(x_rand))
                if evaluaciones.ndim == 0: evaluaciones = np.full(int(n_puntos), evaluaciones)
                
                area_dominio = (b - a)
                try: exacta = float(sp.integrate(f_expr, (x_sym, a, b)))
                except: exacta = None
                
                x_malla = np.linspace(a, b, 1000)
                z_malla = f_rapida(x_malla)
            else:
                f_rapida = sp.lambdify((x_sym, y_sym), f_expr, "numpy") 
                xa, xb = float(sp.sympify(xa_str)), float(sp.sympify(xb_str))
                ya, yb = float(sp.sympify(ya_str)), float(sp.sympify(yb_str))
                
                x_rand = np.random.uniform(xa, xb, int(n_puntos))
                y_rand = np.random.uniform(ya, yb, int(n_puntos))
                
                evaluaciones = np.asarray(f_rapida(x_rand, y_rand))
                if evaluaciones.ndim == 0: evaluaciones = np.full(int(n_puntos), evaluaciones)
                
                area_dominio = (xb - xa) * (yb - ya)
                try: exacta = float(sp.integrate(f_expr, (y_sym, ya, yb), (x_sym, xa, xb)))
                except: exacta = None
                
                x_m = np.linspace(xa, xb, 100)
                y_m = np.linspace(ya, yb, 100)
                X_m, Y_m = np.meshgrid(x_m, y_m)
                z_malla = f_rapida(X_m, Y_m)

            integral_vm = area_dominio * np.mean(evaluaciones)
            
            s_simple = np.std(evaluaciones, ddof=1)
            g_eval = area_dominio * evaluaciones
            s_escalada = np.std(g_eval, ddof=1)
            
            error_estandar = (z_val * s_escalada) / np.sqrt(n_puntos)
            ic_inf, ic_sup = integral_vm - error_estandar, integral_vm + error_estandar

            z_max_malla = np.max(z_malla) if np.max(z_malla) > 0 else 0
            z_min_malla = min(0, np.min(z_malla))
            
            z_max = max(z_max_malla, np.max(evaluaciones) if np.max(evaluaciones) > 0 else 0)
            z_min = min(z_min_malla, min(0, np.min(evaluaciones)))

            escala = area_dominio * (z_max - z_min)
            
            z_rand_box = np.random.uniform(z_min, z_max, int(n_puntos))
            
            hits_pos = (z_rand_box >= 0) & (z_rand_box <= evaluaciones)
            hits_neg = (z_rand_box < 0) & (z_rand_box >= evaluaciones)
            total_hits = np.sum(hits_pos) + np.sum(hits_neg)
            
            integral_ae = ((np.sum(hits_pos) - np.sum(hits_neg)) / int(n_puntos)) * escala

            st.divider()
            c1, c2 = st.columns(2)

            with c1:
                st.subheader("📊 Análisis Estadístico (Valor Medio)")
                st.metric("Integral Estimada (Î)", f"{integral_vm:.8f}")
                
                st.write("**Análisis de Desviación (S):**")
                st.write(f"• $S$ Simple (solo f): `{s_simple:.6f}`")
                st.write(f"• $S$ Escalada (con Dominio): `{s_escalada:.6f}` *(La del pizarrón)*")
                
                st.write(f"**Error Estándar (EE):** `{error_estandar:.6f}` (Z={z_val})")
                st.write(f"**Intervalo de Confianza ({int(confianza*100)}%):**")
                st.info(f"[{ic_inf:.6f} ; {ic_sup:.6f}]")

            with c2:
                st.subheader("🎯 Análisis Geométrico (Acierto/Error)")
                st.metric("Integral Estimada", f"{integral_ae:.8f}")
                st.write(f"**Volumen de Escala (Caja):** `{escala:.4f}`")
                st.write(f"**Aciertos (Totales):** `{total_hits}` de `{n_puntos}`")
                
                if exacta is not None:
                    st.divider()
                    st.metric("Valor Analítico Exacto", f"{exacta:.6f}", delta=f"Desviación Abs: {abs(exacta - integral_vm):.4e}", delta_color="inverse")

            if not es_2d:
                st.divider()
                st.subheader("📈 Gráfica de Simulación 1D")
                fig, ax = plt.subplots(figsize=(8, 4))
                x_vals_plot = np.linspace(a, b, 400)
                y_vals_plot = f_rapida(x_vals_plot)
                ax.plot(x_vals_plot, y_vals_plot, 'k-', linewidth=2, label='f(x)')
                
                max_pts = min(5000, int(n_puntos))
                x_plot, z_plot = x_rand[:max_pts], z_rand_box[:max_pts]
                h_p_plot, h_n_plot = hits_pos[:max_pts], hits_neg[:max_pts]
                miss_plot = ~(h_p_plot | h_n_plot)
                
                ax.scatter(x_plot[miss_plot], z_plot[miss_plot], color='red', s=2, alpha=0.3, label='Fallo')
                ax.scatter(x_plot[h_p_plot], z_plot[h_p_plot], color='green', s=2, alpha=0.5, label='Acierto (+)')
                ax.scatter(x_plot[h_n_plot], z_plot[h_n_plot], color='blue', s=2, alpha=0.5, label='Acierto (-)')
                
                ax.axhline(0, color='black', linewidth=1)
                ax.grid(True, linestyle=':', alpha=0.6)
                ax.legend()
                st.pyplot(fig)

            st.session_state['mc_z_val'] = z_val
            st.session_state['mc_s_escalada'] = s_escalada

        except Exception as e:
            st.error(f"❌ Error: Revisa la sintaxis matemática. Detalle: {e}")

    if 'mc_z_val' in st.session_state and 'mc_s_escalada' in st.session_state:
        st.divider()
        st.subheader("🔮 Proyección de N (Parte B del Pizarrón)")
        error_obj = st.number_input("Error Máximo Deseado (EE):", value=0.01, format="%.3f", key="mc_error_obj")
        
        if error_obj > 0:
            n_nuevo = math.ceil(((st.session_state['mc_z_val'] * st.session_state['mc_s_escalada']) / error_obj)**2)
            st.success("Fórmula: n ≥ (Z * S_escalada / EE_objetivo)²")
            st.metric("Nuevo 'n' necesario:", f"{n_nuevo}")
        else:
            st.warning("El error objetivo debe ser mayor a 0.")
