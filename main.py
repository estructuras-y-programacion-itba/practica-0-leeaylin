# Tu implementacion va aqui
import random
import csv

def tirar_dados():
    return [random.randint(1,6) for _ in range(5)]
    
def elegir_dados(dados):
    print("Dados actuales:", dados)

    while True:
        seleccion = input("Ingresa los valores de los dados que deseas mantener separados por coma: ").strip()
        if seleccion == "":
            valores = []
            break
        try:
            valores = [int(i) for i in seleccion.split(",")]
            copia = dados[:]
            valido = True
            for valor in valores:
                if valor in copia:
                    copia.remove(valor)
                else:
                    valido = False
                    break
            if valido:
                break
            else:
                print("Has ingresado valores que no coinciden con los dados actuales. Intenta de nuevo.")

        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar números separados por comas.")

    copia = dados[:]
    dados_guardados = []

    for valor in valores:
        copia.remove(valor)
        dados_guardados.append(valor)

    nuevos_dados = [random.randint(1, 6) for _ in range(5 - len(dados_guardados))]

    print("Dados guardados:", dados_guardados)
    print("Dados nuevos:", nuevos_dados)

    resultado_final = dados_guardados + nuevos_dados
    return resultado_final

def jugar_turno():
    print("Comienza el turno del jugador.")
    dados = tirar_dados()
    print("Primera tirada:", dados)

    primera_tirada = True
    for tirada in range(2):
        decision = input("¿Desea relanzar los dados? (s/n): ").strip().lower()

        while decision != "s" and decision != "n":
            print("Opción inválida.")
            decision = input("¿Desea relanzar los dados? (s/n): ").strip().lower()

        if decision == "n":
            return dados, primera_tirada

        dados = elegir_dados(dados)
        primera_tirada = False

        print("Nueva tirada:", dados)

    return dados, primera_tirada

                
def contar_valores(dados):
    if isinstance(dados[0], list):
        dados = dados[0]

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

def crear_planilla():
    planilla = [
        [None]*10,
        [None]*10
    ]
    return planilla


def mostrar_planilla(planilla):
    categorias = ["E","F","P","G","1","2","3","4","5","6"]
    print("\nPLANILLA")
    print("Jugada\tJ1\tJ2")

    for i in range(10):
        j1 = planilla[0][i]
        j2 = planilla[1][i]
        if j1 is None:
            j1 = "-"
        if j2 is None:
            j2 = "-"
        print(f"{categorias[i]}\t{j1}\t{j2}")


def guardar_csv(planilla):
    categorias = ["E","F","P","G","1","2","3","4","5","6"]
    archivo = open("jugadas.csv","w")
    archivo.write("jugada,j1,j2\n")
    for i in range(10):
        j1 = planilla[0][i]
        j2 = planilla[1][i]
        if j1 is None:
            j1 = ""
        if j2 is None:
            j2 = ""
        archivo.write(categorias[i] + "," + str(j1) + "," + str(j2) + "\n")
    archivo.close()


def categorias_disponibles(planilla, jugador):
    disponibles = []
    for i in range(10):
        if planilla[jugador][i] is None:
            disponibles.append(i)
    return disponibles


def total_jugador(planilla, jugador):
    total = 0
    for valor in planilla[jugador]:
        if valor is not None:
            total += valor
    return total


def planilla_completa(planilla):
    for jugador in range(2):
        for valor in planilla[jugador]:
            if valor is None:
                return False
    return True

def main():
    print("¡Bienvenidos al juego de Generala!")

    categorias = ["E","F","P","G","1","2","3","4","5","6"]

    planilla = crear_planilla()

    guardar_csv(planilla)

    while not planilla_completa(planilla):

        for jugador in range(2):
            disponibles = categorias_disponibles(planilla, jugador)
            if len(disponibles) == 0:
                continue
            print(f"\nTurno del Jugador {jugador+1}")
            dados, primera_tirada = jugar_turno()
            print(f"Dados finales: {dados}")

            if es_generala(dados):
                print("¡GENERALA!")
            print("Categorías disponibles:")
            for i in disponibles:
                print(categorias[i], end=" ")
            print()

            while True:
                categoria = input("Elige categoría: ").strip().upper()
                if categoria in categorias:
                    indice = categorias.index(categoria)
                    if indice in disponibles:
                        break
                print("Categoría inválida o ya usada.")

            puntaje = calcular_puntaje_categoria(categoria, dados, primera_tirada)
            if puntaje is None:
                puntaje = 0
            print("Puntaje obtenido:", puntaje)
            planilla[jugador][indice] = puntaje
            guardar_csv(planilla)
            mostrar_planilla(planilla)

    print("\nRESULTADOS FINALES")

    total_j1 = total_jugador(planilla,0)
    total_j2 = total_jugador(planilla,1)

    print("Jugador 1:", total_j1)
    print("Jugador 2:", total_j2)

    if total_j1 > total_j2:
        print("Ganó Jugador 1")
    elif total_j2 > total_j1:
        print("Ganó Jugador 2")
    else:
        print("Empate")

# No cambiar a partir de aqui
if __name__ == "__main__":
    main()
