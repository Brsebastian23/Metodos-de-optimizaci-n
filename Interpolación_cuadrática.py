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

def interpolacion_cuadratica(x0, x1, x2, error, ecuacion):
  max_o_min = 0
  while max_o_min != 1 and max_o_min != 2:
    max_o_min = int(input("Si desea maximizar ingrese 1, si desea minimizar ingrese 2: "))
    if max_o_min != 1 and max_o_min != 2:
      print("Ingrese un valor valido: 1 ó 2")

  if not (x0 < x1 < x2):
    print("Error: los valores deben cumplir que x0<x1<x2 para aplicar el metodo")
    return None

  if max_o_min == 2:
    # Minimizar: x1 debe ser menor que sus vecinos f(x1)<f(x0) y f(x1)<f(x2)
    if f(x1, ecuacion) > f(x0, ecuacion) or f(x1, ecuacion) > f(x2, ecuacion):
      print("El valor x1 no cumple las caracteristicas para aplicar el metodo (no hay minimo entre x0 y x2)")
      return None
  else:
    # Maximizar: x1 debe ser mayor que sus vecinos f(x1)>f(x0) y f(x1)>f(x2)
    if f(x1, ecuacion) < f(x0, ecuacion) or f(x1, ecuacion) < f(x2, ecuacion):
      print("El valor x1 no cumple las caracteristicas para aplicar el metodo (no hay maximo entre x0 y x2)")
      return None

  numerador = f(x0, ecuacion)*(x1**2 - x2**2) + f(x1, ecuacion)*(x2**2 - x0**2) + f(x2, ecuacion)*(x0**2 - x1**2)
  denominador = 2*f(x0, ecuacion)*(x1 - x2) + 2*f(x1, ecuacion)*(x2 - x0) + 2*f(x2, ecuacion)*(x0 - x1)
  x3 = numerador / denominador

  tabla = []
  iteraciones = 0
  if max_o_min == 1:
    while abs(x1-x3)>error:
      tabla.append([x0, f(x0, ecuacion), x1, f(x1, ecuacion), x2, f(x2, ecuacion), x3, f(x3, ecuacion), f(x3, ecuacion)-f(x1, ecuacion), abs(x1-x3)])

      iteraciones += 1
      if x3>x1:
        if f(x3, ecuacion)>f(x1, ecuacion):
          x0 = x1
          x1 = x3
        else:
          x2 = x3
      else:
        if f(x3, ecuacion)>f(x1, ecuacion):
          x2 = x1
          x1 = x3
        else:
          x0 = x3
      numerador = f(x0, ecuacion)*(x1**2 - x2**2) + f(x1, ecuacion)*(x2**2 - x0**2) + f(x2, ecuacion)*(x0**2 - x1**2)
      denominador = 2*f(x0, ecuacion)*(x1 - x2) + 2*f(x1, ecuacion)*(x2 - x0) + 2*f(x2, ecuacion)*(x0 - x1)
      x3 = numerador / denominador

  else:
    while abs(x1-x3)>error:
      tabla.append([x0, f(x0, ecuacion), x1, f(x1, ecuacion), x2, f(x2, ecuacion), x3, f(x3, ecuacion), f(x3, ecuacion)-f(x1, ecuacion), abs(x1-x3)])

      iteraciones += 1
      if x3>x1:
        if f(x3, ecuacion)<f(x1, ecuacion):
          x0 = x1
          x1 = x3
        else:
          x2 = x3
      else:
        if f(x3, ecuacion)<f(x1, ecuacion):
          x2 = x1
          x1 = x3
        else:
          x0 = x3
      numerador = f(x0, ecuacion)*(x1**2 - x2**2) + f(x1, ecuacion)*(x2**2 - x0**2) + f(x2, ecuacion)*(x0**2 - x1**2)
      denominador = 2*f(x0, ecuacion)*(x1 - x2) + 2*f(x1, ecuacion)*(x2 - x0) + 2*f(x2, ecuacion)*(x0 - x1)
      x3 = numerador / denominador

  return x3, iteraciones, tabla, max_o_min

def mostrar_tabla(tabla):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')  
    
    headers = ['x0', 'f(x0)', 'x1', 'f(x1)', 'x2', 'f(x2)', 'x3', 'f(x3)','f(x1)-f(x3)', 'error']
    
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
    
    ax.set_title('Tabla de Iteraciones - Interpolación cuadrática', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show()

def main():

    print("=" * 60)
    print("INTERPOLACIÓN CUADRÁTICA")
    print("=" * 60)
    ecuacion = input("Ingrese la ecuación usando x como variable:  ")
    print("Ahora vamos a definir el rango en donde vamos a buscar el optimo de la función")
    x0 = float(input("Ingrese el valor de X0:  "))
    x1 = float(input("Ingrese el valor de X1  "))
    x2 = float(input("Ingrese el valor de X2  "))
    error = float(input("Ingrese el error aceptado:  "))
    
    resultado = interpolacion_cuadratica(x0, x1, x2, error, ecuacion)
    if resultado is None:
        return
    else:
        x3, iteraciones, tabla, max_min  = resultado
        
        plt.figure(dpi=200)
        x = np.linspace(-10, 10, 1000)
        plt.ylim(-10,10)
        y = []
        for val in x:
            y.append(f(val, ecuacion))
        
        plt.plot(x, y, 'b-', label='f(x) ='+ecuacion)
        plt.axvline(x=x0, color='green', linestyle='-', linewidth=0.5)
        plt.axvline(x=x1, color='green', linestyle='-', linewidth=0.5)
        plt.axvline(x=x2, color='green', linestyle='-', linewidth=0.5)
        plt.axhline(y=f(x3, ecuacion), color='red', linestyle='--', label=f'f(punto optimo) = {f(x3, ecuacion):.4f}')
        plt.axvline(x=x3, color='green', linestyle='--', label=f'punto optimo = {x3:.4f}')
        plt.legend(['optimo', 'x0', 'x1', 'x2'])
        
        
        plt.grid(True, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Busqueda dorada - Gráfica de la función')
        plt.legend()
        plt.show()
        
        # Gráfica del error
        plt.figure(figsize=(10, 6))
        errores = [row[9] for row in tabla]
        
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



if __name__ == "__main__":
    main()
