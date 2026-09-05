import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def f(punto, ecuacion):
    ns = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'pi': math.pi, 'e': math.e, 'sqrt': math.sqrt,
        'exp': math.exp, 'log': math.log, 'abs_': abs,
    }
    for i, val in enumerate(punto, start=1):
        ns[f'x{i}'] = val
    if len(punto) >= 1:
        ns['x'] = punto[0]
    if len(punto) >= 2:
        ns['y'] = punto[1]

    return eval(ecuacion, {"__builtins__": {}}, ns)


def busqueda_aleatoria(ecuacion, limites, max_o_min, n_puntos, semilla):
    dimension = len(limites)

    if semilla is None:
        semilla = random.randint(0, 1000000)
    rng = random.Random(int(semilla))

    mejor_valor = -1e9 if max_o_min == 1 else 1e9
    mejor_punto = [limites[i][0] for i in range(dimension)]

    tabla = []
    for j in range(n_puntos):
        punto = []
        for i, (xl, xu) in enumerate(limites):
            r = rng.random()  # [0,1)
            xi = xl + (xu - xl) * r
            punto.append(xi)

        fn = f(punto, ecuacion)

        if max_o_min == 1:
            if fn > mejor_valor:
                mejor_valor = fn
                mejor_punto = punto[:]
        else:
            if fn < mejor_valor:
                mejor_valor = fn
                mejor_punto = punto[:]

        tabla.append(punto + [fn, mejor_valor])

    return mejor_punto, mejor_valor, tabla, max_o_min, dimension, semilla


def mostrar_tabla(tabla, dimension):
    ultimas = tabla[-10:]

    headers = [f'x{i+1}' for i in range(dimension)]
    headers += ['f(x)', 'Mejor f']

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.axis('off')

    table_data = []
    for row in ultimas:
        table_data.append([f'{val:.6f}' for val in row])

    table = ax.table(cellText=table_data,
                     colLabels=headers,
                     loc='center',
                     cellLoc='center',
                     colColours=['#f0f0f0'] * len(headers))

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)

    for i in range(len(table_data)):
        for j in range(len(headers)):
            if i % 2 == 0:
                table[(i + 1, j)].set_facecolor('#fafafa')
            else:
                table[(i + 1, j)].set_facecolor('#e8e8e8')

    ax.set_title('Últimas 10 muestras - Búsqueda Aleatoria',
                 fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.show()


def graficar_superficie_2d(ecuacion, limites, mejor_punto, mejor_valor):
    (x_l, x_u), (y_l, y_u) = limites
    res = 80
    x_vals = np.linspace(x_l, x_u, res)
    y_vals = np.linspace(y_l, y_u, res)
    X, Y = np.meshgrid(x_vals, y_vals)

    Z = np.zeros_like(X)
    for i in range(res):
        for j in range(res):
            Z[i, j] = f([X[i, j], Y[i, j]], ecuacion)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9, edgecolor='none')
    fig.colorbar(surf, shrink=0.5, aspect=10)

    ax.scatter(mejor_punto[0], mejor_punto[1], mejor_valor,
               color='red', s=140, marker='*', linewidths=2,
               label=f'Óptimo = ({mejor_punto[0]:.3f}, {mejor_punto[1]:.3f}) = {mejor_valor:.3f}')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x,y)')
    ax.set_title('Superficie f(x,y) - Búsqueda Aleatoria\nf = ' + ecuacion)
    ax.legend()
    plt.tight_layout()
    plt.show()


def main():
    print("=" * 60)
    print("BÚSQUEDA ALEATORIA MULTIDIMENSIONAL")
    print("=" * 60)

    dimension = int(input("Ingrese el número de variables (dimensión): "))
    if dimension < 1:
        print("La dimensión debe ser al menos 1.")
        return

    if dimension == 2:
        ecuacion = input("Ingrese la ecuación usando x, y (o x1, x2):  ")
    elif dimension == 1:
        ecuacion = input("Ingrese la ecuación usando x (o x1):  ")
    else:
        ecuacion = input(f"Ingrese la ecuación usando x1, x2, ..., x{dimension}:  ")

    max_o_min = 0
    while max_o_min not in [1, 2]:
        try:
            max_o_min = int(input("Si desea maximizar ingrese 1, si desea minimizar ingrese 2: "))
            if max_o_min not in [1, 2]:
                print("Ingrese un valor válido: 1 ó 2")
        except ValueError:
            print("Por favor ingrese un número válido")

    limites = []
    for i in range(dimension):
        print(f"\nVariable x{i+1}:")
        xl = float(input(f"  Límite inferior de x{i+1}: "))
        xu = float(input(f"  Límite superior de x{i+1}: "))
        limites.append((xl, xu))

    n_puntos = int(input("\nIngrese el número de muestras aleatorias (n): "))

    semilla_in = input("Ingrese una semilla entera para reproducibilidad (0 ó vacío = aleatoria): ")
    try:
        semilla = int(semilla_in)
        if semilla == 0:
            semilla = None
    except ValueError:
        semilla = None

    mejor_punto, mejor_valor, tabla, max_o_min, dimension, semilla = \
        busqueda_aleatoria(ecuacion, limites, max_o_min, n_puntos, semilla)

    tipo = 'MÁXIMO' if max_o_min == 1 else 'MÍNIMO'

    print("\n" + "=" * 60)
    print(f"RESULTADOS (semilla usada: {int(semilla)})")
    print("=" * 60)
    print(f"Total de muestras evaluadas: {len(tabla)}")
    for i, v in enumerate(mejor_punto, start=1):
        print(f"x{i} = {v:.6f}")
    print(f"Valor {tipo} encontrado: {mejor_valor:.6f}")
    print("=" * 60)

    # --- Gráfica del error: decrece hacia 0 ---
    # error_k = |mejor_valor_final - mejor_acumulado_k|
    errores = [abs(mejor_valor - row[dimension + 1]) for row in tabla]

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(errores) + 1), errores,
             'r-o', linewidth=2, markersize=4)
    plt.grid(True, alpha=0.3)
    plt.xlabel('Número de muestra')
    plt.ylabel('Error (|óptimo final − mejor acumulado|)')
    plt.title(f'Error de convergencia - Búsqueda Aleatoria ({tipo})')
    plt.axhline(y=0, color='green', linestyle='--', linewidth=1, label='Error = 0 (óptimo final)')
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(8))
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(10))
    plt.legend()
    plt.show()

    # --- Gráfica superficie 3D: SOLO si es 2D ---
    if dimension == 2:
        graficar_superficie_2d(ecuacion, limites, mejor_punto, mejor_valor)
    else:
        print("=" * 60)
        print(f"Nota: El problema es un hiperplano de {dimension} dimensiones,")
        print("no se puede graficar la superficie en 3D. Solo se muestra")
        print("la gráfica de error y la tabla de muestras.")
        print("=" * 60)

    # --- Tabla con SOLO las últimas 10 muestras ---
    mostrar_tabla(tabla, dimension)


if __name__ == "__main__":
    main()
