import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import math

def render():
    st.header("Dashboard General: Demostración de Todos los Métodos")
    st.markdown("A continuación se presenta un resumen gráfico de la ejecución de cada método con una función de ejemplo.")
    
    colA, colB = st.columns(2)
    
    with colA:
        # 1. Bisección
        st.subheader("1. Método de Bisección")
        x_sym = sp.symbols('x')
        f_expr = sp.sympify("x**3 - x - 2")
        f = sp.lambdify(x_sym, f_expr, "math")
        a, b = 1.0, 2.0
        m = a
        for _ in range(20):
            m = (a + b) / 2
            if f(a) * f(m) < 0: b = m
            else: a = m
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        x_vals = np.linspace(0.5, 2.5, 200)
        ax1.plot(x_vals, [f(v) for v in x_vals], label='x^3 - x - 2')
        ax1.axhline(0, color='black', linewidth=0.8)
        ax1.plot(m, 0, 'ro', label=f'Raíz: {m:.4f}')
        ax1.legend(); ax1.grid(True, alpha=0.3)
        st.pyplot(fig1)

        # 3. Aitken
        st.subheader("3. Punto Fijo (Aitken)")
        g_expr = sp.sympify("sqrt(2 * (x + 2) / pi)")
        g = sp.lambdify(x_sym, g_expr, "math")
        x0 = 1.5
        for _ in range(10):
            x1 = g(x0); x2 = g(x1)
            den = x2 - 2*x1 + x0
            if abs(den)<1e-9: break
            x0 = x0 - (x1-x0)**2 / den
        fig3, ax3 = plt.subplots(figsize=(6, 3))
        x_vals = np.linspace(0, 3, 200)
        ax3.plot(x_vals, [g(v) for v in x_vals], label='g(x)')
        ax3.plot(x_vals, x_vals, 'g--', label='y = x')
        ax3.plot(x0, x0, 'ro', label=f'Raíz: {x0:.4f}')
        ax3.legend(); ax3.grid(True, alpha=0.3)
        st.pyplot(fig3)

        # 5. Integracion
        st.subheader("5. Integración Numérica")
        f_expr = sp.sympify("sin(x)/x")
        f = sp.lambdify(x_sym, f_expr, "math")
        fig5, ax5 = plt.subplots(figsize=(6, 3))
        x_vals = np.linspace(0.0001, 1.2, 200)
        ax5.plot(x_vals, [f(v) for v in x_vals], 'r', label='sin(x)/x')
        x_fill = np.linspace(0.0001, 1.0, 100)
        ax5.fill_between(x_fill, [f(v) for v in x_fill], color='orange', alpha=0.3, label='Área')
        ax5.legend(); ax5.grid(True, alpha=0.3)
        st.pyplot(fig5)

        # 7. Euler
        st.subheader("7. Método de Euler")
        st.markdown("Ejemplo: $y' = x - y$, $y(0)=1$")
        def f_euler(x, y): return x - y
        h_e = 0.5
        x_e, y_e = 0.0, 1.0
        x_vals_e = [x_e]; y_vals_e = [y_e]
        for _ in range(4):
            y_e += h_e * f_euler(x_e, y_e)
            x_e += h_e
            x_vals_e.append(x_e); y_vals_e.append(y_e)
        fig8, ax8 = plt.subplots(figsize=(6, 3))
        ax8.plot(x_vals_e, y_vals_e, 'g-o', label='Euler')
        x_ex = np.linspace(0, 2, 100)
        y_ex = x_ex - 1 + 2*np.exp(-x_ex)
        ax8.plot(x_ex, y_ex, 'r--', label='Exacta')
        ax8.legend(); ax8.grid(True, alpha=0.3)
        st.pyplot(fig8)

    with colB:
        # 2. Newton
        st.subheader("2. Newton-Raphson")
        f_expr = sp.sympify("(x-1)**2")
        df_expr = sp.diff(f_expr, x_sym)
        f = sp.lambdify(x_sym, f_expr, "math")
        df = sp.lambdify(x_sym, df_expr, "math")
        x0 = 0.0
        for _ in range(10): x0 = x0 - f(x0)/df(x0)
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        x_vals = np.linspace(-1, 3, 200)
        ax2.plot(x_vals, [f(v) for v in x_vals], label='(x-1)^2')
        ax2.axhline(0, color='black', linewidth=0.8)
        ax2.plot(x0, 0, 'ro', label=f'Raíz: {x0:.4f}')
        ax2.legend(); ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)

        # 4. Lagrange
        st.subheader("4. Interpolación (Lagrange)")
        x_nodes, y_nodes = [1, 2, 3], [math.exp(1), math.exp(2), math.exp(3)]
        polinomio = 0
        for i in range(3):
            L_i = 1
            for j in range(3):
                if i != j: L_i *= (x_sym - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
            polinomio += y_nodes[i] * L_i
        P_func = sp.lambdify(x_sym, sp.simplify(polinomio), "math")
        fig4, ax4 = plt.subplots(figsize=(6, 3))
        x_vals = np.linspace(0.5, 3.5, 200)
        ax4.plot(x_vals, [math.exp(v) for v in x_vals], 'b--', alpha=0.5, label='exp(x)')
        ax4.plot(x_vals, [P_func(v) for v in x_vals], 'orange', label='P(x)')
        ax4.plot(x_nodes, y_nodes, 'ko')
        ax4.legend(); ax4.grid(True, alpha=0.3)
        st.pyplot(fig4)

        # 6. Monte Carlo
        st.subheader("6. Monte Carlo (1D)")
        f_expr = sp.sympify("exp(-x**2)")
        f = sp.lambdify(x_sym, f_expr, "numpy")
        x_rand = np.random.uniform(0.0, 1.0, 2000)
        evals = f(x_rand)
        z_max = max(1.0, np.max(evals))
        z_rand = np.random.uniform(0.0, z_max, 2000)
        h_pos = (z_rand >= 0) & (z_rand <= evals)
        fig6, ax6 = plt.subplots(figsize=(6, 3))
        x_vals = np.linspace(0.0, 1.0, 200)
        ax6.plot(x_vals, f(x_vals), 'k-', label='exp(-x^2)')
        ax6.scatter(x_rand[h_pos], z_rand[h_pos], color='green', s=5, alpha=0.5, label='Acierto')
        ax6.scatter(x_rand[~h_pos], z_rand[~h_pos], color='red', s=5, alpha=0.3, label='Fallo')
        ax6.legend(); ax6.grid(True, alpha=0.3)
        st.pyplot(fig6)

        # 8. RK4
        st.subheader("8. Runge-Kutta 4")
        st.markdown("Ejemplo: $y' = x - y$, $y(0)=1$")
        def f_rk4(x, y): return x - y
        h_rk4 = 0.5
        x_rk4, y_rk4 = 0.0, 1.0
        x_vals_rk4 = [x_rk4]; y_vals_rk4 = [y_rk4]
        for _ in range(4):
            k1 = f_rk4(x_rk4, y_rk4)
            k2 = f_rk4(x_rk4 + h_rk4/2, y_rk4 + k1*h_rk4/2)
            k3 = f_rk4(x_rk4 + h_rk4/2, y_rk4 + k2*h_rk4/2)
            k4 = f_rk4(x_rk4 + h_rk4, y_rk4 + k3*h_rk4)
            y_rk4 += (h_rk4/6)*(k1 + 2*k2 + 2*k3 + k4)
            x_rk4 += h_rk4
            x_vals_rk4.append(x_rk4); y_vals_rk4.append(y_rk4)
        fig7, ax7 = plt.subplots(figsize=(6, 3))
        ax7.plot(x_vals_rk4, y_vals_rk4, 'b-o', label='RK4')
        x_ex = np.linspace(0, 2, 100)
        y_ex = x_ex - 1 + 2*np.exp(-x_ex)
        ax7.plot(x_ex, y_ex, 'r--', label='Exacta')
        ax7.legend(); ax7.grid(True, alpha=0.3)
        st.pyplot(fig7)
