# Comando para ejecutar la app: python -m streamlit run app.py
import streamlit as st

# Configuración básica de la página
st.set_page_config(page_title="Calculadora Numérica", layout="wide")

st.title("🧮 Calculadora de Métodos Numéricos")
st.markdown("Laboratorio de Matemática Computacional")

# --- MENÚ LATERAL ---
st.sidebar.header("Módulos")
modulo = st.sidebar.selectbox(
    "Selecciona el método:",
    [
        "Dashboard General",
        "Método de Bisección", 
        "Newton-Raphson", 
        "Punto Fijo Acelerado (Aitken)", 
        "Interpolación (Lagrange)",
        "Integración Numérica",
        "Monte Carlo (Integración)",
        "Calculadora Analítica",
        "Método de Euler",
        "Runge-Kutta 4 (RK4)"
    ]
)

if modulo == "Dashboard General":
    import methods.dashboard as dashboard
    dashboard.render()
elif modulo == "Método de Bisección":
    import methods.biseccion as biseccion
    biseccion.render()
elif modulo == "Newton-Raphson":
    import methods.newton as newton
    newton.render()
elif modulo == "Punto Fijo Acelerado (Aitken)":
    import methods.aitken as aitken
    aitken.render()
elif modulo == "Interpolación (Lagrange)":
    import methods.lagrange as lagrange
    lagrange.render()
elif modulo == "Integración Numérica":
    import methods.integracion as integracion
    integracion.render()
elif modulo == "Monte Carlo (Integración)":
    import methods.montecarlo as montecarlo
    montecarlo.render()
elif modulo == "Método de Euler":
    import methods.euler as euler
    euler.render()
elif modulo == "Runge-Kutta 4 (RK4)":
    import methods.rk4 as rk4
    rk4.render()
elif modulo == "Calculadora Analítica":
    import methods.analitica as analitica
    analitica.render()