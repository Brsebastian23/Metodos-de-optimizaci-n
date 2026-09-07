import os

import Bisección
import Falsa_posición
import Busqueda_dorada
import Interpolación_cuadrática
import Metodo_de_newton
import Busqueda_aleatoria
import maxima_inclinacion

def mostrar_menu():
    """Muestra el menú principal"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print("="*50)
    print("MÉTODOS DE OPTIMIZACIÓN")
    print("="*50)
    print("1. Bisección")
    print("2. Falsa Posición")
    print("3. Búsqueda Dorada")
    print("4. Interpolación Cuadrática")
    print("5. Método de Newton")
    print("6. Busqueda aleatoria")
    print("7. Máxima inclinación")
    print("0. Salir")
    print("="*50)

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "0":
            print("¡Hasta luego!")
            break
            
        elif opcion == "1":
            Bisección.main()
            pass
            
        elif opcion == "2":
            Falsa_posición.main()
            pass
            
        elif opcion == "3":
            Busqueda_dorada.main()
            pass
            
        elif opcion == "4":
            Interpolación_cuadrática.main()
            pass
            
        elif opcion == "5":
            Metodo_de_newton.main()
            pass

        elif opcion == "6":
            Busqueda_aleatoria.main()
            pass
        elif opcion == "7":
            maxima_inclinacion.main()
            pass
        else:
            print("Opción inválida")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()