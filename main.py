# Tu implementacion va aqui
import random
import csv

def tirar_dados():
    return [random.randint(1,6) for n in range(5)]
    
def elegir_dados(dados):
    print(f"Dados actuales:{dados}")
    seleccion = input("ingresar el/los indice/s (0-4) de los dados que deseas mantener separados por una coma:").strip()

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

def contar_valores(dados):
    conteos = [0] * 7
    for dado in dados:
        conteos[dado] += 1
    return conteos


def es_escalera(dados):
    ordenados = sorted(dados)
    return ordenados == [1, 2, 3, 4, 5] or ordenados == [2, 3, 4, 5, 6]


def es_full(dados):
    conteos = contar_valores(dados)
    hay_tres = False
    hay_dos = False

    for i in range(1, 7):
        if conteos[i] == 3:
            hay_tres = True
        elif conteos[i] == 2:
            hay_dos = True

    return hay_tres and hay_dos

def es_poker(dados):
    conteos = contar_valores(dados)
    for i in range(1, 7):
        if conteos[i] >= 4:
            return True
    return False


def es_generala(dados):
    conteos = contar_valores(dados)
    for i in range(1, 7):
        if conteos[i] == 5:
            return True
    return False

def calcular_puntaje_categoria(categoria, dados, primera_tirada):
    if categoria == "E":
        if es_escalera(dados):
            return 25 if primera_tirada else 20
        return None

    if categoria == "F":
        if es_full(dados):
            return 35 if primera_tirada else 30
        return None

    if categoria == "P":
        if es_poker(dados):
            return 45 if primera_tirada else 40
        return None

    if categoria == "G":
        if es_generala(dados):
            return 80 if primera_tirada else 50
        return None

    if categoria in ["1", "2", "3", "4", "5", "6"]:
        numero = int(categoria)
        suma = 0
        for dado in dados:
            if dado == numero:
                suma += dado
        return suma

    return 0

def main():
    print("¡Bienvenidos al juego de Generala!")
    jugadores = ["Jugador 1", "Jugador 2"]
    puntajes = [0, 0] 
    categorias_usadas = [[], []]

    for i, jugador in enumerate(jugadores):
        print(f"\nTurno de {jugador}")
        dados = jugar_turno()
        print(f"Dados finales: {dados}")

        # Mostrar categorías disponibles
        print("Categorías disponibles:")
        categorias_disponibles = [cat for cat in ["E", "F", "P", "G", "1", "2", "3", "4", "5", "6"] if cat not in categorias_usadas[i]]
        print(", ".join(categorias_disponibles))

        # Elegir categoría
        while True:
            categoria = input("Elige una categoría para anotar tu puntaje: ").strip().upper()
            if categoria in categorias_disponibles:
                break
            print("Categoría no válida o ya utilizada. Intenta de nuevo.")

        # Calcular puntaje
        primera_tirada = False 
        puntaje = calcular_puntaje_categoria(categoria, dados, primera_tirada)
        print(f"Puntaje obtenido: {puntaje}")

        # Actualizar puntajes y categorías usadas
        puntajes[i] += puntaje
        categorias_usadas[i].append(categoria)

    # Mostrar resultados finales
    print("\nResultados finales:")
    for i, jugador in enumerate(jugadores):
        print(f"{jugador}: {puntajes[i]} puntos")

    

# No cambiar a partir de aqui
if __name__ == "__main__":
    main()
