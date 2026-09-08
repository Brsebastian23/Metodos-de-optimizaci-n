import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sympy as sp


def maxima_inclinacion(x0, y0, error, ecuacion, x_l, x_u, y_l, y_u):
    x = sp.Symbol('x')
    y = sp.Symbol('y')

    f_sym = sp.sympify(ecuacion)
    dfdx = sp.diff(f_sym, x)
    dfdy = sp.diff(f_sym, y)

    fn = sp.lambdify((x, y), f_sym, modules=['numpy'])
    dfdxn = sp.lambdify((x, y), dfdx, modules=['numpy'])
    dfdyn = sp.lambdify((x, y), dfdy, modules=['numpy'])

    X = x0
    Y = y0

    tabla = []

    f_actual = float(f_sym.subs({x: X, y: Y}))
    gx = float(dfdx.subs({x: X, y: Y}))
    gy = float(dfdy.subs({x: X, y: Y}))
    tabla.append([X, Y, gx, gy, f_actual, 0.0, abs(gx) + abs(gy)])
    trayectoria = [[X, Y]]

    iteraciones = 0

    while True:
        gx = dfdxn(X, Y)
        gy = dfdyn(X, Y)
        norma_grad = float(abs(gx) + abs(gy))

        if norma_grad < error:
            break

        h = sp.Symbol('h')
        xh = X + gx * h
        yh = Y + gy * h
        g_sym = f_sym.subs({x: xh, y: yh})

        g1_sym = sp.diff(g_sym, h)
        g2_sym = sp.diff(g1_sym, h)

        g1 = sp.lambdify(h, g1_sym, modules=['numpy'])
        g2 = sp.lambdify(h, g2_sym, modules=['numpy'])
        gv = sp.lambdify(h, g_sym, modules=['numpy'])

        h_opt, encontro = _hallar_h_optimo(g1, g2, gv)

        nuevo_X = X + gx * h_opt
        nuevo_Y = Y + gy * h_opt
        f_nueva = float(f_sym.subs({x: nuevo_X, y: nuevo_Y}))

        iteraciones += 1
        cambio = abs(f_nueva - f_actual)

        tabla.append([nuevo_X, nuevo_Y, float(gx), float(gy),
                      f_nueva, float(h_opt), cambio])
        trayectoria.append([nuevo_X, nuevo_Y])

        if cambio < error or not encontro:
            X, Y = nuevo_X, nuevo_Y
            f_actual = f_nueva
            break

        X, Y = nuevo_X, nuevo_Y
        f_actual = f_nueva

    tipo = "MAXIMO"
    return (X, Y, f_actual, iteraciones, tabla, trayectoria, fn,
            x_l, x_u, y_l, y_u, tipo)


def _hallar_h_optimo(g1, g2, gv, max_iter_bracket=40, tol=1e-10):
    h0 = 0.0

    try:
        g1_0 = float(g1(h0))
    except Exception:
        return 0.0, False

    if g1_0 <= 0:
        return 0.0, False

    h_prev = h0
    g1_prev = g1_0
    delta = 0.02
    encontro_cruce = False

    for _ in range(max_iter_bracket):
        h_curr = h_prev + delta
        try:
            g1_curr = float(g1(h_curr))
            gv_curr = float(gv(h_curr))
        except Exception:
            break

        if not (np.isfinite(g1_curr) and np.isfinite(gv_curr)):
            break

        if g1_curr <= 0 or g1_prev <= 0:
            encontro_cruce = True
            break

        g1_prev = g1_curr
        h_prev = h_curr
        delta *= 1.7

    if not encontro_cruce:
        return h_prev, False

    a, b = h_prev, h_curr
    ga = g1_prev if h_prev == h0 else None
    ga = g1(a)
    gb = g1(b)

    for _ in range(200):
        if abs(b - a) < tol:
            break
        mid = (a + b) / 2.0
        gmid = g1(mid)
        if ga * gmid <= 0:
            b = mid
            gb = gmid
        else:
            a = mid
            ga = gmid

    h_star = (a + b) / 2.0

    try:
        if float(g2(h_star)) >= 0:
            return h_star, False
    except Exception:
        return h_star, False

    if h_star < 0:
        return 0.0, False

    return h_star, True


def mostrar_tabla(tabla):
    headers = ['x', 'y', 'df/dx', 'df/dy', 'f(x,y)', 'h*', 'Error']

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.axis('off')

    table_data = []
    for row in tabla:
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

    ax.set_title('Tabla de Iteraciones - Metodo de Maxima Inclinacion',
                 fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.show()


def graficar_error(tabla, error):
    plt.figure(figsize=(10, 6))
    errores = [row[6] for row in tabla[1:]]

    plt.plot(range(1, len(errores) + 1), errores,
             'r-o', linewidth=2, markersize=8)
    plt.axhline(y=error, color='green', linestyle='--', linewidth=2,
                label=f'Tolerancia = {error}')
    plt.grid(True, alpha=0.3)
    plt.xlabel('Iteracion')
    plt.ylabel('Error (|Δf|)')
    plt.title('Error en el ascenso - Metodo de Maxima Inclinacion')
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(8))
    plt.legend()
    plt.show()


def graficar_superficie(fn, x_l, x_u, y_l, y_u, trayectoria,
                        x_max, y_max, f_max):
    """
    Gráfica 3D estilo Desmos con iluminación y sombreado
    """
    # ========== PARÁMETROS DE PERSONALIZACIÓN ==========
    figsize = (12, 9)           # Tamaño de la figura
    elev = 25                   # Elevación (Desmos usa ~25°)
    azim = -60                  # Azimut (Desmos usa ~-60°)
    cmap = 'viridis'            # Colormap (el mismo que usa Desmos)
    alpha = 1.0                 # Opacidad total
    res = 100                   # Mayor resolución para suavidad
    
    # Contorno en la base
    mostrar_contorno_base = True
    alpha_contorno = 0.3        # Semitransparente
    
    # Trayectoria
    color_tray = 'red'
    lw_tray = 3
    ms_tray = 8
    alpha_tray = 0.9
    
    # Punto máximo
    color_max = 'gold'
    size_max = 300
    marker_max = '*'
    borde_max = 'black'
    borde_width = 1.5
    
    # Estilo Desmos
    fondo_oscuro = False        # True para fondo oscuro
    mostrar_grid = True
    mostrar_lineas_nivel = False  # Líneas de contorno sobre superficie
    
    # ========== GENERAR MALLA ==========
    XX = np.linspace(x_l, x_u, res)
    YY = np.linspace(y_l, y_u, res)
    XG, YG = np.meshgrid(XX, YY)
    ZG = fn(XG, YG)
    
    # ========== CREAR FIGURA ==========
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    
    # Fondo (opcional)
    if fondo_oscuro:
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
    
    # ========== SUPERFICIE CON ILUMINACIÓN ==========
    # plot_surface con iluminación automática
    surf = ax.plot_surface(XG, YG, ZG, 
                          cmap=cmap, 
                          alpha=alpha,
                          edgecolor='none',
                          antialiased=True,
                          shade=True,        # <--- ¡ILUMINACIÓN!
                          linewidth=0)
    
    # ========== CONTORNO EN LA BASE ==========
    zmin = np.min(ZG)
    z_base = zmin - 0.05 * (np.max(ZG) - zmin)  # Espacio debajo de la superficie
    
    if mostrar_contorno_base:
        # Contorno suave en la base (como Desmos)
        contorno = ax.contourf(XG, YG, ZG, 
                              zdir='z', 
                              offset=z_base, 
                              cmap=cmap, 
                              alpha=alpha_contorno,
                              levels=20)  # Número de niveles
        
        # Líneas de contorno más definidas
        ax.contour(XG, YG, ZG, 
                  zdir='z', 
                  offset=z_base, 
                  cmap=cmap, 
                  alpha=0.5,
                  linewidths=0.5,
                  levels=20)
    
    # ========== LÍNEAS DE NIVEL SOBRE LA SUPERFICIE ==========
    if mostrar_lineas_nivel:
        ax.contour(XG, YG, ZG, 
                  zdir='z', 
                  cmap=cmap, 
                  alpha=0.3,
                  linewidths=0.5)
    
    # ========== TRAYECTORIA ==========
    traj = np.array(trayectoria)
    z_traj = fn(traj[:, 0], traj[:, 1])
    
    # Línea de trayectoria en 3D
    ax.plot(traj[:, 0], traj[:, 1], z_traj, 
            color=color_tray, 
            linewidth=lw_tray,
            alpha=alpha_tray,
            label='Trayectoria')
    
    # Puntos de la trayectoria
    ax.scatter(traj[:, 0], traj[:, 1], z_traj,
              color=color_tray, 
              s=ms_tray**2,
              alpha=alpha_tray,
              edgecolors='white',
              linewidth=0.5)
    
    # Proyección de la trayectoria en la base
    ax.plot(traj[:, 0], traj[:, 1], 
            z_base * np.ones(len(traj)),
            color=color_tray, 
            linestyle='--', 
            linewidth=1.5, 
            alpha=0.4)
    
    # Líneas verticales de proyección (opcional)
    for i in range(0, len(traj), max(1, len(traj)//10)):  # Cada 10% de puntos
        ax.plot([traj[i, 0], traj[i, 0]], 
                [traj[i, 1], traj[i, 1]], 
                [z_base, z_traj[i]], 
                color=color_tray, 
                linestyle=':', 
                alpha=0.2,
                linewidth=0.5)
    
    # ========== PUNTO MÁXIMO ==========
    ax.scatter(x_max, y_max, f_max,
              color=color_max,
              s=size_max,
              marker=marker_max,
              edgecolors=borde_max,
              linewidths=borde_width,
              depthshade=True,      # <--- Sombra en el punto
              label=f'Máximo = ({x_max:.3f}, {y_max:.3f}, {f_max:.3f})',
              zorder=10)            # Asegura que esté encima
    
    # Línea desde el máximo hasta la base
    ax.plot([x_max, x_max], 
            [y_max, y_max], 
            [z_base, f_max],
            color='black', 
            linestyle='--', 
            alpha=0.3,
            linewidth=1)
    
    # ========== BARRA DE COLORES ==========
    cbar = fig.colorbar(surf, shrink=0.6, aspect=20, pad=0.1)
    cbar.set_label('f(x,y)', fontsize=12)
    cbar.ax.tick_params(labelsize=10)
    
    # ========== ETIQUETAS ==========
    ax.set_xlabel('X', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y', fontsize=12, fontweight='bold')
    ax.set_zlabel('f(x,y)', fontsize=12, fontweight='bold')
    
    # ========== TÍTULO ==========
    titulo = f'Superficie f(x,y) - Método de Máxima Inclinación'
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    
    # ========== ÁNGULO DE VISIÓN ==========
    ax.view_init(elev=elev, azim=azim)
    
    # ========== GRID Y ASPECTO ==========
    ax.grid(mostrar_grid, alpha=0.3)
    
    # Ajustar límites para mejor visualización
    ax.set_zlim(z_base, np.max(ZG) * 1.05)
    
    # ========== LEYENDA ==========
    ax.legend(loc='upper left', framealpha=0.9, fontsize=10)
    
    # ========== AJSUTAR ESPACIO ==========
    plt.tight_layout()
    plt.show()


def main():
    print("=" * 60)
    print("METODO DE MAXIMA INCLINACION")
    print("=" * 60)

    ecuacion = input("Ingrese la ecuacion usando x e y como variables:  ")
    print("\nPunto inicial:")
    x0 = float(input("  Ingrese x0: "))
    y0 = float(input("  Ingrese y0: "))
    error = float(input("Ingrese el error aceptado:  "))

    print("\nDefina el rango para GRAFICAR la superficie:")
    x_l = float(input("  Limite inferior de x: "))
    x_u = float(input("  Limite superior de x: "))
    y_l = float(input("  Limite inferior de y: "))
    y_u = float(input("  Limite superior de y: "))

    resultado = maxima_inclinacion(x0, y0, error, ecuacion,
                                   x_l, x_u, y_l, y_u)

    x_max, y_max, f_max, iteraciones, tabla, trayectoria, fn, \
        x_l, x_u, y_l, y_u, tipo = resultado

    print("\n" + "=" * 60)
    print("RESULTADOS")
    print("=" * 60)
    print(f"Iteraciones: {iteraciones}")
    print(f"x = {x_max:.6f}")
    print(f"y = {y_max:.6f}")
    print(f"Valor {tipo} de f: {f_max:.6f}")
    print("=" * 60)

    graficar_error(tabla, error)
    graficar_superficie(fn, x_l, x_u, y_l, y_u, trayectoria,
                        x_max, y_max, f_max)
    mostrar_tabla(tabla)


if __name__ == "__main__":
    main()
