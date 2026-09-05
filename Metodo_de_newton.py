import math
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np
import sympy as sp

def funcion(x, ecuacion):
    sin = math.sin
    cos = math.cos
    tan = math.tan
    pi = math.pi
    e = math.e
    sqrt = math.sqrt
    exp = math.exp
    log = math.log
    abs_ = abs
    return eval(ecuacion)

def derivar(expresion, variable):
    return sp.diff(expresion, variable)

def metodo_newton(k_inicial, error, ecuacion):
    x = sp.Symbol('x')

    f = sp.sympify(ecuacion)

    max_o_min = 0
    while max_o_min not in [1, 2]:
        try:
            max_o_min = int(input("Si desea encontrar una raiz ingrese 1, si desea encontrar un valor optimo ingrese 2: "))
            if max_o_min not in [1, 2]:
                print("Ingrese un valor valido: 1 ó 2")
        except ValueError:
            print("Por favor ingrese un número válido")

    derivada = derivar(f, x)
    derivada_segunda = derivar(derivada, x)

    k = k_inicial
    k_anterior = 0
    iteraciones = 0

    tabla = []
    tabla.append([(k), f.subs(x, k), derivada.subs(x, k), derivada_segunda.subs(x, k), abs(k)])


    if max_o_min == 1:

        while abs(k - k_anterior) > error:
            iteraciones += 1
            k_anterior = k

            f_val = f.subs(x, k_anterior)
            der_val = derivada.subs(x, k_anterior)

            # Verificar que la derivada no sea cero
            if abs(der_val) < 1e-15:
                print("Error: Derivada demasiado cercana a cero")
                break

            k = k_anterior - float((f_val / der_val))


            tabla.append([k, f.subs(x, k), derivada.subs(x, k), derivada_segunda.subs(x, k), abs(k_anterior-k)])


    else:
        
        while abs(k - k_anterior) > error:
            iteraciones += 1
            k_anterior = k

            der_val = derivada.subs(x, k_anterior)
            der2_val = derivada_segunda.subs(x, k_anterior)

            if abs(der2_val) < 1e-15:
                print("Error: Segunda derivada demasiado cercana a cero")
                break

            k = k_anterior - float((der_val / der2_val))

            tabla.append([(k), f.subs(x, k), derivada.subs(x, k), derivada_segunda.subs(x, k), abs(k_anterior-k)])


    tipo_punto = None
    if max_o_min == 2:
        der2_final = derivada_segunda.subs(x, k)
        if der2_final > 0:
            tipo_punto = "MÍNIMO"
        elif der2_final < 0:
            tipo_punto = "MÁXIMO"
        else:
            tipo_punto = "PUNTO DE INFLEXIÓN"

    return k, iteraciones, tabla, max_o_min, tipo_punto, f

def mostrar_tabla(tabla):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')  
    
    headers = ['x', 'f(x)', 'f*(x)', 'f**(x)', 'error']
    
    table_data = []
    for row in tabla:
        table_data.append([f'{val:.6f}' for val in row])
    
    table = ax.table(cellText=table_data, 
                     colLabels=headers,
                     loc='center',
                     cellLoc='center',
                     colColours=['#f0f0f0']*len(headers))
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    for i, row in enumerate(table_data):
        for j in range(len(headers)):
            if i % 2 == 0:
                table[(i+1, j)].set_facecolor('#fafafa')
            else:
                table[(i+1, j)].set_facecolor('#e8e8e8')
    
    ax.set_title('Tabla de Iteraciones - Método de Newton', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show()

def main():
    print("=" * 60)
    print("MÉTODO DE NEWTON")
    print("=" * 60)
    ecuacion = input("Ingrese la ecuación usando x como variable:  ")
    x = float(input("Ingrese el valor de x:  "))
    error = float(input("Ingrese el error aceptado:  "))
    
    resultado = metodo_newton(x, error, ecuacion)
    if isinstance(resultado, str):
        print(resultado)
    else:
        k, iteraciones, tabla, max_o_min, tipo_punto, f  = resultado
        
        plt.figure(dpi=200)
        x = np.linspace(-10, 10, 1000)
        plt.ylim(-10,10)
        y = []
        for val in x:
            y.append(funcion(val, ecuacion))
        
        plt.plot(x, y, 'b-', label='f(x) ='+ecuacion)
        if max_o_min == 2:
            plt.axhline(y=funcion(k, ecuacion), color='red', linestyle='--', label=f'valor optimo = {k:.4f}')

        else:
            plt.axvline(x=k, color='red', linestyle='--', label=f'raiz = {k:.4f}')
        
        
        plt.grid(True, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Método de Newton - Gráfica de la función')
        plt.legend()
        plt.show()
        
        # Gráfica del error
        plt.figure(figsize=(10, 6))
        errores = [row[4] for row in tabla]
        
        plt.plot(range(1, len(errores) + 1), errores, 'r-o', linewidth=2, markersize=8)
        plt.axhline(y=error, color='green', linestyle='--', linewidth=2, label=f'Tolerancia = {error}')
        plt.grid(True, alpha=0.3)
        plt.xlabel('Iteración')
        plt.ylabel('Error')
        plt.title('Error en el cálculo de la raíz')
        
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.1))
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.legend()
        plt.show()
        
        # Mostrar tabla
        mostrar_tabla(tabla)