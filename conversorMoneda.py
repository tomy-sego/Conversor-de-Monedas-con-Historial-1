import json

# Tasas de cambio fijas: valores respecto al USD
conversion_rates = {
    "USD": {"USD": 1, "EUR": 0.92, "ARS": 875.50, "BRL": 5.15},
    "EUR": {"USD": 1.09, "EUR": 1, "ARS": 950.20, "BRL": 5.60},
    "ARS": {"USD": 0.00114, "EUR": 0.00105, "ARS": 1, "BRL": 0.0059},
    "BRL": {"USD": 0.194, "EUR": 0.179, "ARS": 170.0, "BRL": 1}
}

monedas_disponibles = list(conversion_rates.keys())

def validar_monto(monto_str):
    try:
        monto = float(monto_str)
        if monto < 0:
            raise ValueError("El monto no puede ser negativo.")
        return monto
    except ValueError:
        print("Monto inválido. Ingrese un número positivo.")
        return None

def validar_moneda(moneda):
    if moneda in monedas_disponibles:
        return True
    print("Moneda no válida. Elija entre:", ", ".join(monedas_disponibles))
    return False

def convertir_moneda(monto, moneda_origen, moneda_destino):
    tasa = conversion_rates[moneda_origen][moneda_destino]
    return monto * tasa

def guardar_historial(monto, moneda_origen, resultado, moneda_destino):
    conversion = {
        "origen": f"{monto} {moneda_origen}",
        "destino": f"{round(resultado, 2)} {moneda_destino}"
    }

    try:
        with open("historial.json", "r", encoding="utf-8") as f:
            historial = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        historial = []

    historial.append(conversion)

    with open("historial.json", "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4)

def mostrar_historial():
    try:
        with open("historial.json", "r", encoding="utf-8") as f:
            historial = json.load(f)
            if historial:
                print("\nHistorial de conversiones:")
                for item in historial:
                    print(f"{item['origen']} → {item['destino']}")
            else:
                print("No hay conversiones guardadas.")
    except FileNotFoundError:
        print("No se encontró el archivo de historial.")

def main():
    while True:
        print("\n--- Conversor de Monedas ---")
        print("1. Convertir moneda")
        print("2. Ver historial")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            monto = None
            while monto is None:
                monto_input = input("Ingrese el monto: ")
                monto = validar_monto(monto_input)

            moneda_origen = input("Ingrese la moneda de origen (USD, EUR, ARS, BRL): ").upper()
            if not validar_moneda(moneda_origen):
                continue

            moneda_destino = input("Ingrese la moneda de destino (USD, EUR, ARS, BRL): ").upper()
            if not validar_moneda(moneda_destino):
                continue

            resultado = convertir_moneda(monto, moneda_origen, moneda_destino)
            print(f"\nResultado: {round(resultado, 2)} {moneda_destino}")
            guardar_historial(monto, moneda_origen, resultado, moneda_destino)

        elif opcion == "2":
            mostrar_historial()

        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
