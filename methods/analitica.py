import streamlit as st
import sympy as sp

def render():
    st.header("Calculadora Analítica")
    st.markdown("Cálculo exacto de derivadas e integrales usando SymPy.")

    # Input para la función
    func_str = st.text_input("Ingrese la función matemática f(x):", value="sin(x)*exp(x)")
    
    # Definir la variable simbólica
    x = sp.Symbol('x')

    try:
        # Parsear la función
        f = sp.sympify(func_str)
        
        # Mostrar la función ingresada
        st.latex(r"f(x) = " + sp.latex(f))

        # Crear pestañas para Derivadas e Integrales
        tab_derivada, tab_integral = st.tabs(["Derivadas", "Integrales"])

        with tab_derivada:
            st.subheader("Cálculo de Derivadas")
            orden_opciones = {
                "1ra": 1,
                "2da": 2,
                "3ra": 3,
                "4ta": 4
            }
            orden_seleccionado = st.selectbox("Orden de la derivada:", list(orden_opciones.keys()))
            n = orden_opciones[orden_seleccionado]
            
            if st.button("Calcular Derivada"):
                # Calcular la derivada exacta
                derivada = sp.diff(f, x, n)
                
                # Formatear el lado izquierdo de la ecuación
                if n == 1:
                    d_tex = r"f'(x) = \frac{d}{dx}[f(x)] = "
                elif n == 2:
                    d_tex = r"f''(x) = \frac{d^2}{dx^2}[f(x)] = "
                elif n == 3:
                    d_tex = r"f'''(x) = \frac{d^3}{dx^3}[f(x)] = "
                else:
                    d_tex = rf"f^{{({n})}}(x) = \frac{{d^{{{n}}}}}{{dx^{{{n}}}}}[f(x)] = "
                
                st.latex(d_tex + sp.latex(derivada))

        with tab_integral:
            st.subheader("Cálculo de Integrales")
            tipo_integral = st.radio("Tipo de integral:", ["Indefinida", "Definida"])
            
            if tipo_integral == "Definida":
                col1, col2 = st.columns(2)
                with col1:
                    lim_inf = st.text_input("Límite inferior (a):", value="0")
                with col2:
                    lim_sup = st.text_input("Límite superior (b):", value="pi")
            
            if st.button("Calcular Integral"):
                if tipo_integral == "Indefinida":
                    # Calcular integral indefinida
                    integral = sp.integrate(f, x)
                    st.latex(r"\int " + sp.latex(f) + r" \, dx = " + sp.latex(integral) + " + C")
                else:
                    try:
                        # Evaluar límites, pueden ser expresiones simbólicas como "pi"
                        a = sp.sympify(lim_inf)
                        b = sp.sympify(lim_sup)
                        
                        # Calcular integral definida
                        integral_def = sp.integrate(f, (x, a, b))
                        st.latex(r"\int_{" + sp.latex(a) + r"}^{" + sp.latex(b) + r"} " + sp.latex(f) + r" \, dx = " + sp.latex(integral_def))
                        
                        # Mostrar el valor numérico flotante si es posible
                        valor_num = integral_def.evalf()
                        st.success(f"Valor numérico aproximado: {valor_num}")
                        
                    except Exception as e_lim:
                        st.error(f"Error en los límites de integración: {e_lim}")

    except Exception as e:
        if func_str:
            st.error(f"Error de sintaxis al evaluar la función: {e}")
        else:
            st.info("Por favor, ingrese una función válida.")
