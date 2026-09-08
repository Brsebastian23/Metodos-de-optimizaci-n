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

def busqueda_dorada(xl, xu, error, ecuacion):
  max_o_min = 0
  while max_o_min != 1 and max_o_min != 2:
    max_o_min = int(input("Si desea maximizar ingrese 1, si desea minimizar ingrese 2"))
    if max_o_min != 1 and max_o_min != 2:
      print("Ingrese un valor valido: 1 ó 2")

  fi = (1+math.sqrt(5))/2



  tabla = []
  iteraciones = 0
  d = (1/fi)*(xu-xl)
  x1 = xl + d
  x2 = xu - d
  if max_o_min == 1:
    while abs(x2-x1)>error:
      d = (1/fi)*(xu-xl)
      x1 = xl + d
      x2 = xu - d
      iteraciones += 1
      tabla.append([xu, xl, f(xu, ecuacion), f(xl, ecuacion), f(x2, ecuacion)-f(x1, ecuacion), abs(x2-x1)])
      if f(x2, ecuacion)>f(x1, ecuacion):
        xl=xl
        xu = x1
      else:
        xu = xu
        xl = x2
  else:
    while abs(x2-x1)>error:
      d = (1/fi)*(xu-xl)
      x1 = xl + d
      x2 = xu - d
      iteraciones += 1
      tabla.append([xu, xl, f(xu, ecuacion), f(xl, ecuacion), f(x2, ecuacion)-f(x1, ecuacion), abs(x2-x1)])
      if f(x2, ecuacion)<f(x1, ecuacion):
        xl=xl
        xu = x1
      else:
        xu = xu
        xl = x2

  return xl, iteraciones, tabla, max_o_min


def mostrar_tabla(tabla):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')  
    
    headers = ['Xu', 'Xl', 'f(Xu)', 'f(Xl)', 'f(X2)-f(X1)', 'Error']
    
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
    
    ax.set_title('Tabla de Iteraciones - Busqueda dorada', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show()

def main():

    print("=" * 60)
    print("BUSQUEDA DORADA")
    print("=" * 60)
    ecuacion = input("Ingrese la ecuación usando x como variable:  ")
    print("Ahora vamos a definir el rango en donde vamos a buscar el optimo de la función")
    x_lower = float(input("Ingrese el valor inferior del rango:  "))
    x_upper = float(input("Ingrese el valor superior del rango:  "))
    error = float(input("Ingrese el error aceptado:  "))
    
    resultado = busqueda_dorada(x_lower, x_upper, error, ecuacion)
    if isinstance(resultado, str):
        print(resultado)
    else:
        xl, iteraciones, tabla, max_o_min = resultado
        
        plt.figure(dpi=200)
        x = np.linspace(-10, 10, 1000)
        plt.ylim(-10,10)
        y = []
        for val in x:
            y.append(f(val, ecuacion))
        
        plt.plot(x, y, 'b-', label='f(x) ='+ecuacion)
        plt.axvline(x=x_lower, color='green', linestyle='-', linewidth=0.5)
        plt.axvline(x=x_upper, color='green', linestyle='-', linewidth=0.5)
        plt.axhline(y=f(xl,ecuacion), color='red', linestyle='--', label=f'f(valor optimo) = {f(xl, ecuacion):.4f}')
        plt.axvline(x=xl, color='green', linestyle='--', label=f'valor optimo = {xl:.4f}')
        
        
        plt.grid(True, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Busqueda dorada - Gráfica de la función')
        plt.legend()
        plt.show()
        
        # Gráfica del error
        plt.figure(figsize=(10, 6))
        errores = [row[5] for row in tabla]
        
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