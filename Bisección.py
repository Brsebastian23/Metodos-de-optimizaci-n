import math
import matplotlib.pyplot as plt
from tabulate import tabulate
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np

def f(x, ecuacion):
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


def biseccion(f, xl, xu, error, ecuacion):
    iteraciones = 0
    
    if f(xl, ecuacion) * f(xu, ecuacion) > 0:
        return 'La funcion no tiene raices en el intervalo dado'
    
    tabla = []
    while abs(xl - xu) > error:
        xr = (xl + xu) / 2
        tabla.append([xu, xl, xr, f(xu, ecuacion), f(xl, ecuacion), f(xr, ecuacion), f(xl, ecuacion)*f(xr, ecuacion), abs(xl-xu)])
        
        if f(xr, ecuacion) == 0:
            break
        elif f(xl, ecuacion) * f(xr, ecuacion) < 0:
            xu = xr
        else:
            xl = xr
        
        iteraciones += 1
    
    # Mostrar tabla
    headers = ['Xu', 'Xl', 'Xr', 'f(Xu)', 'f(Xl)', 'f(Xr)', 'f(Xl)*f(Xr)', 'Error']
    print(tabulate(tabla, headers=headers, floatfmt=".6f"))
    
    return xr, iteraciones, tabla

def mostrar_tabla(tabla):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')  
    
    headers = ['Xu', 'Xl', 'Xr', 'f(Xu)', 'f(Xl)', 'f(Xr)', 'f(Xl)*f(Xr)', 'Error']
    
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
    
    # Título
    ax.set_title('Tabla de Iteraciones - Método de Bisección', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show()

def main():
    print("=" * 60)
    print("BISECCIÓN")
    print("=" * 60)
    
    ecuacion = input("Ingrese la ecuación usando x como variable:  ")
    print("Ahora vamos a definir el rango en donde vamos a buscar la raiz de la función")
    xl = float(input("Ingrese el valor inferior del rango:  "))
    xu = float(input("Ingrese el valor superior del rango:  "))
    error = float(input("Ingrese el error aceptado:  "))
    
    resultado = biseccion(f, xl, xu, error, ecuacion)
    if isinstance(resultado, str):
        print(resultado)
    else:
        raiz, iteraciones, tabla = resultado
        print(f"\nRaíz encontrada: {raiz:.6f}")
        print(f"Iteraciones: {iteraciones}")
        
        plt.figure(figsize=(10, 6))
        x = np.linspace(-4, 2, 1000)
        y = []
        for val in x:
            y.append(f(val, ecuacion))
        
        plt.plot(x, y, 'b-', label='f(x) = x³ + x² + x + 3')
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.axvline(x=raiz, color='red', linestyle='--', label=f'Raíz = {raiz:.4f}')
        
        
        plt.grid(True, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Método de Bisección - Gráfica de la función')
        plt.legend()
        plt.show()
        
        # Gráfica del error
        plt.figure(figsize=(10, 6))
        errores = [row[7] for row in tabla]
        
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