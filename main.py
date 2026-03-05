# Tu implementacion va aqui
import random
import csv

def tirar_dados():
    return [random.randint(1,6) for n in range(5)]
    
def elegir_dados(dados):
    print(f"Dados actuales:{dados}")
    seleccion = input("ingresar el/los indice/s (0-5) de los dados que deseas mantener separados por una coma:").strip()

    indices = []
    for i in seleccion.split(","):
        try:
            indice = int(i)  # Intentamos convertir el valor a entero
            indices.append(dados[i])  # Si es válido, lo agregamos a la lista
        except ValueError:
            print(f"'{i}' no es un número válido y será ignorado.")  # Informamos al usuario

    dados_mantenidos = []
    for i in indices:
        if 0 <= i < len(dados): # Verificamos que el índice esté dentro del rango válido
            dados_mantenidos.append(dados[i]) # Agregamos el dado correspondiente a la lista

    # Calculo cuántos dados deben volver a lanzarse
    dados_nuevos = len(dados) - len(dados_mantenidos)
    nuevos_dados = [random.randint(1, 6) for i in range(dados_nuevos)]  # Lanzar nuevos dados

    # Combinar los dados mantenidos con los nuevos lanzados
    resultado_final = dados_mantenidos + nuevos_dados
    print(f"Resultado final: {resultado_final}")
    return resultado_final

def jugar_turno():
    print("Comienza el turno del jugador.")
    dados = tirar_dados()
    print(f"Primera tirada: {dados}")

    for tirada in range(2): #dos lanzamientos
        while True:
            decision = input("Desea relanzar los dados? (s/n): ").strip().lower()
            if decision == "s":
                dados = elegir_dados(dados)
                break
            elif decision == "n":
                return dados
            else:
                print("Opcion invalida. Reingrese 's' o 'n'.")
                #!!!!!!!Chequear aca, la parte del bucle y que se vuelven a pedir el input hasta que sea uno valido. 


# # No cambiar a partir de aqui
# if __name__ == "__main__":
#     main()
