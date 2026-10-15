#instruccion: Crear un codigo que imite la mecanica del futdraft en el videojuego FIFA usando python
# necesitamos usar librerias, todos tipo de ciclos y que se cargue desde un archivo que funja como base de datos
import pandas as pd
import random

# 1. CARGA EL ARCHIVO EXCEL DE LOS JUGADORES PARA EL FUTDRAFT

def cargar_jugadores_excel(nombre_archivo):
    df = pd.read_excel(nombre_archivo)
    return df.to_dict(orient="records")


# 2. OBTENER JUGADORES DISPONIBLES POR POSICIÓN

def obtener_disponibles(jugadores, posicion, elegidos):
    disponibles = [
        j for j in jugadores 
        if str(j["Posición"]).upper() == posicion and j["Nombre"] not in elegidos
    ]

    if len(disponibles) == 0:
        disponibles = [j for j in jugadores if j["Nombre"] not in elegidos]

    return disponibles


# 3. REDUCIR A SOLO 4 OPCIONES RANDOM

def seleccionar_4_random(disponibles):
    if len(disponibles) <= 4:
        return disponibles
    return random.sample(disponibles, 4)

# 4. MOSTRAR OPCIONES

def mostrar_opciones(disponibles):
    for i, jugador in enumerate(disponibles):
        print(f"{i+1}. {jugador['Nombre']} | VAL: {jugador['Valoración']} | CLUB: {jugador['Club']}")


# 5. PEDIR ELECCIÓN AL USUARIO

def seleccionar_jugador(disponibles):
    while True:
        entrada = input(f"Elige jugador (1-{len(disponibles)}): ").strip()

        if not entrada.isdigit():
            print("Entrada no es un número. Intenta de nuevo.")
            continue

        idx = int(entrada) - 1
        if 0 <= idx < len(disponibles):
            return disponibles[idx]
        else:
            print("Número fuera de rango. Intenta de nuevo.")


# 6. CONSTRUIR EQUIPO

def construir_equipo(jugadores, posiciones):
    equipo = []
    elegidos = []

    print("Seleccionarás jugadores para las siguientes posiciones:\n")
    print(posiciones)

    for posicion in posiciones:
        print(f"\nSelecciona jugador para posición: {posicion}")

        disponibles = obtener_disponibles(jugadores, posicion, elegidos)

        if len(disponibles) == 0:
            print("No quedan jugadores disponibles.")
            break

        # ➜ esto es para que se limite a los 4 jugadores random y no te de a todos los que estan disponibles
        # en esa posición
        disponibles = seleccionar_4_random(disponibles)

        mostrar_opciones(disponibles)
        elegido = seleccionar_jugador(disponibles)

        equipo.append(elegido)
        elegidos.append(elegido["Nombre"])

    return equipo


# 7. CÁLCULO DE LA QUÍMICA Y LA MEDIA DEL EQUIPO

def calcular_quimica_y_media(equipo):
    total_val = 0
    total_qui = 0

    for jugador in equipo:
        try:
            val_num = float(jugador.get("Valoración", 0))
        except:
            val_num = 0.0

        total_val += val_num

        quimica = 0
        for compa in equipo:
            if compa is not jugador:
                if jugador["Nacionalidad"] == compa["Nacionalidad"]:
                    quimica += 1
                if jugador["Liga"] == compa["Liga"]:
                    quimica += 1
                if jugador["Club"] == compa["Club"]:
                    quimica += 1

        jugador["quimica_individual"] = quimica
        total_qui += quimica

    prom_val = total_val / len(equipo) if equipo else 0
    puntaje_final = prom_val + (total_qui * 0.5)

    return prom_val, total_qui, puntaje_final


# 8. MOSTRAR EL EQUIPO FINAL.

def mostrar_resultados(equipo, prom_val, total_qui, puntaje_final):
    print("\n=========================================")
    print("           RESULTADOS DEL EQUIPO")
    print("=========================================")

    if equipo:
        for j in equipo:
            print(f"{j['Posición']}: {j['Nombre']} | VAL: {j['Valoración']} | QUI: {j['quimica_individual']}")
    else:
        print("No se seleccionó ningún jugador.")

    print("\n--- ESTADÍSTICAS ---")
    print(f"Valoración media: {prom_val:.2f}")
    print(f"Química total: {total_qui}")
    print(f"Puntaje final: {puntaje_final:.2f}")


# 9. MAIN (SIRVE PARA QUE SE VAYAN EJECUTANDO LAS FUNCIONES CUANDO VAYAN SIENDO NECESITADAS)

def main():
    POSICIONES_DRAFT = ["POR", "DFC", "DFC", "LTI", "LTD", "MCD", "MC", "MCO", "EI", "ED", "DC"]

    print("=========================================")
    print(" FUT DRAFT ")
    print("=========================================\n")

    jugadores = cargar_jugadores_excel("jugadores para futdraft.xlsx")
    equipo = construir_equipo(jugadores, POSICIONES_DRAFT)
    prom_val, total_qui, puntaje_final = calcular_quimica_y_media(equipo)
    mostrar_resultados(equipo, prom_val, total_qui, puntaje_final)


if __name__ == "__main__":
    main()
