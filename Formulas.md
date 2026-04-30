# Formulario de Métodos Numéricos

## Punto Fijo Acelerado (Aceleración de Aitken)
* **Fórmula de iteración:** La fórmula central del método toma tres elementos consecutivos de una secuencia para calcular un valor acelerado mediante la siguiente ecuación:
  $$x_n^{\ast} = x_n - \frac{(x_{n+1} - x_n)^2}{x_{n+2} - 2x_{n+1} + x_n}$$
* **Errores y Convergencia:** El método se basa en cómo se reduce el error entre aproximaciones sucesivas, denotado como $|e_{n+1}| = C|e_n|^p$, donde $C$ es una constante independiente de $n$, y $p$ es el orden de convergencia.
* **Tolerancias:** Los límites de error se pueden establecer como tolerancia en el error absoluto:
  $$|x_{n+1} - x_n| \le \epsilon$$
  O en el error relativo:
  $$\frac{|x_{n+1} - x_n|}{|x_{n+1}|} \le \epsilon$$

---

## Método de Newton-Raphson
* **Fórmula de iteración:** Se basa en la aproximación lineal de la función mediante su derivada, definida por:
  $$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$
* **Errores y Convergencia:** Este método posee un orden de convergencia cuadrática, lo que lo hace muy rápido si el punto inicial está cerca de la raíz real. Sin embargo, puede divergir si la derivada es cero o si el valor inicial está muy lejos del valor esperado.

---

## Reconstrucción de funciones con Polinomios de Lagrange
* **Fórmula general:** El polinomio de Lagrange para un conjunto de puntos $n$ se construye con la fórmula:
  $$P(x) = \sum_{i=0}^{n} y_i L_i(x)$$
* **Bases de Lagrange:** Las bases $L_i(x)$ se definen como:
  $$L_i(x) = \prod_{j=0, j \neq i}^{n} \frac{x - x_j}{x_i - x_j}$$
* **Error de interpolación local:** Evaluado entre la función real y el polinomio en el intervalo $x_0 < \xi < x_n$:
  $$E(x) = f(x) - P(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} \prod_{i=0}^{n} (x - x_i)$$
* **Cota global de error:** Requiere determinar el valor máximo absoluto en la derivada $M_{n+1} = \max|f^{(n+1)}(\xi)|$ y se aplica de la siguiente forma:
  $$|E(x)| \le \frac{M_{n+1}}{(n+1)!} \prod_{i=0}^{n} |x - x_i|$$

---

## Diferencia Finita en un punto
* **Diferencias finitas progresivas:**
  $$f'(x_i) = \frac{f(x_{i+1}) - f(x_i)}{h}$$
  $$f''(x_i) = \frac{f(x_{i+2}) - 2f(x_{i+1}) + f(x_i)}{h^2}$$
* **Diferencias finitas regresivas:**
  $$f'(x_i) = \frac{f(x_i) - f(x_{i-1})}{h}$$
  $$f''(x_i) = \frac{f(x_i) - 2f(x_{i-1}) + f(x_{i-2})}{h^2}$$
* **Diferencias finitas centrales:**
  $$f'(x_i) = \frac{f(x_{i+1}) - f(x_{i-1})}{2h}$$
  $$f''(x_i) = \frac{f(x_{i+1}) - 2f(x_i) + f(x_{i-1})}{h^2}$$

---

## Método del Trapecio Compuesto
* **Fórmula de integración:** Se divide el área en $n$ subintervalos utilizando un tamaño de paso $h = \frac{b-a}{n}$. La fórmula de aproximación es:
  $$\int_{a}^{b} f(x) dx \approx \frac{h}{2} \left[ f(a) + 2 \sum_{i=1}^{n-1} f(a+ih) + f(b) \right]$$
* **Error de Truncamiento:** El error de la forma compuesta está determinado por:
  $$E_T = -\frac{(b-a)^3}{12n^2} f''(\xi)$$

---

## Método de Simpson 1/3
* **Regla Simple:** Evaluada en 3 puntos, con $h = \frac{b-a}{2}$:
  $$\int_{a}^{b} f(x) dx \approx \frac{h}{3} \left[ f(a) + 4f\left( \frac{a+b}{2} \right) + f(b) \right]$$
* **Regla Compuesta:** Donde $n$ debe ser par y $h = \frac{b-a}{n}$:
  $$\int_{a}^{b} f(x) dx \approx \frac{h}{3} \left[ f(a) + 4 \sum_{\text{impares}} f(a+ih) + 2 \sum_{\text{pares}} f(a+ih) + f(b) \right]$$
* **Errores de truncamiento:** 
  * Para la regla simple:
    $$E = -\frac{(b-a)^5}{2880} f^{(4)}(\xi) = -\frac{h^5}{90} f^{(4)}(\xi)$$
  * Para la regla compuesta (error global):
    $$E_{\text{comp}} = -\frac{(b-a)^5}{180n^4} f^{(4)}(\xi) = -\frac{b-a}{180} h^4 f^{(4)}(\xi)$$

---

## Ecuaciones Diferenciales de Runge-Kutta (Concepto general)
* **Definición General:** Métodos sistemáticos iterativos que predicen la nueva pendiente combinando evaluaciones en varios puntos dentro de un paso constante.
* **Error de Truncamiento:** El efecto del tamaño de paso para determinar la precisión (caso polinómico general) se expresa como:
  $$R_n = \frac{y^{(n+1)}(\xi)}{(n+1)!} h^{n+1}$$

---

## Método de Euler
* **Fórmula Simple:** Realiza una predicción moviéndose a lo largo de un segmento de recta siguiendo la pendiente inicial $f(x_n, y_n)$:
  $$y_{n+1} = y_n + hf(x_n, y_n)$$
* **Fórmula de Euler Mejorado (Heun):** Corrige y promedia la pendiente de prueba para lograr mayor precisión:
  $$y_{n+1} = y_n + \frac{h}{2} \Big( f(x_n, y_n) + f(x_{n+1}, y^{\ast}) \Big)$$
  *(Donde el valor predicho inicialmente es $y^{\ast} = y_n + hf(x_n, y_n)$)*

---

## Ecuación de Runge-Kutta 4 (RK4)
* **Fórmula general iterativa:** Busca mejorar drásticamente la precisión de la trayectoria ponderando cuatro pendientes distintas dentro del intervalo:
  $$y_{n+1} = y_n + \frac{h}{6} (k_1 + 2k_2 + 2k_3 + k_4)$$
* **Cálculo de las pendientes (k):**
  $$k_1 = f(x_n, y_n)$$
  $$k_2 = f\left(x_n + \frac{1}{2}h, y_n + \frac{1}{2}k_1 h\right)$$
  $$k_3 = f\left(x_n + \frac{1}{2}h, y_n + \frac{1}{2}k_2 h\right)$$
  $$k_4 = f(x_n + h, y_n + k_3 h)$$
