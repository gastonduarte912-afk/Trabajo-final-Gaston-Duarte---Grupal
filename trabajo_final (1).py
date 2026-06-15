#Importamos bibliotecas externas, para los archivos csv y caracteres especiales
import csv
import re

#Función para re imprimir el menú las veces que sean necesarias
def imprimir_menu():
    print("""
    1) Agregar un país.
    2) Actualizar datos de Población y Superficie de un País.
    3) Buscar un País por su nombre.
    4) Filtrar País.
    5) Ordenar Países.
    6) Estadísticas.
    7) Eliminar país.
    8) Salir.
    """)

#Función para validar caracteres especiales
def caracteres_especiales(texto):
    if re.match(r'^[^a-zA-Z0-9]+$', texto):
        raise ValueError("Error. Ingresó un caracter especial.")

#Validación de espacios vacíos
def val_espacio_vacio(texto):
    if texto.strip() == "":
        raise ValueError("Error. No puede ingresar espacios vacíos.")

#Validación para números 
def validar_not_is_alpha(texto):
    if texto.isalpha():
        raise ValueError("Error. Debe ingresar un número válido.")


#Validación para strings  
def validar_not_is_digit(texto):
    if texto.isdigit():
        raise ValueError("Error. Ingresó un número.")
    
#Creamos la función para leer el archivo CSV
def cargar_paises_csv(nombre_archivo):
    paises = []
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                #Validamos que en caso de filas vacías el programa pueda continuar
                if not fila or None in fila.values() or "" in fila.values():
                    continue

                paises.append({
                    "Nombre": fila["Nombre"],
                    "Poblacion": int(fila["Poblacion"]),
                    "Superficie": int(fila["Superficie"]),
                    "Continente": fila["Continente"]
                })

    except (FileNotFoundError, KeyError, ValueError):
        with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Nombre", "Poblacion", "Superficie", "Continente"])
    
    return paises

#Creamos la lista de diccionario como dataset
dataset_paises = cargar_paises_csv("paises.csv")

#Creamos la función para agregar países a la lista
def agregar_pais(nombre_archivo):
    while True:
        try:
            nombre = input("Ingrese el nombre del país: ").lower().strip()
            val_espacio_vacio(nombre)
            caracteres_especiales(nombre)
            validar_not_is_digit(nombre)
            break
        except ValueError as e:
                print(e)

    while True: 
        try:        
            poblacion = input("Ingrese la población: ").strip()
            val_espacio_vacio(poblacion)
            caracteres_especiales(poblacion)
            if not poblacion.isdigit():
                raise ValueError("Error. La población debe contener solo números.")
            break
        except ValueError as e:
                print(e)
    while True:
            try:
                superficie = input("Ingrese la superficie: ").strip()
                val_espacio_vacio(superficie)
                caracteres_especiales(superficie)
                if not superficie.isdigit():
                    raise ValueError("Error. La superficie debe contener solo números.")
                break
            except ValueError as e:
                print(e)
    while True:
        try:
            continente = input("Ingrese el continente: ").lower().strip()
            val_espacio_vacio(continente)
            caracteres_especiales(continente)
            validar_not_is_digit(continente)
            break

        except ValueError as e:
                print(e)

    poblacion = int(poblacion)
    superficie = int(superficie)

    try:
        with open(nombre_archivo, "a", newline="", encoding="utf-8") as archivo:
            agregar_linea = csv.writer(archivo)

            agregar_linea.writerow([nombre, poblacion, superficie, continente])

            dataset_paises.append({
                    "Nombre": nombre,
                    "Poblacion": poblacion,
                    "Superficie": superficie,
                    "Continente": continente
                })    

            print("País agregado correctamente.")

    except Exception as e:
        print(f"Error al guardar en el archivo: {e}")

#Creamos la función para eliminar un país si es necesario 
def eliminar_pais(nombre_archivo):
    print("Eliminar un País")
    while True:
        try:
            nombre_buscar = input("Ingrese el nombre del país que desea eliminar: ").strip().lower()
            val_espacio_vacio(nombre_buscar)
            caracteres_especiales(nombre_buscar)
            validar_not_is_digit(nombre_buscar)
            break
        except ValueError as e:
            print(e)

    #Buscamos coincidencias, trabajando con los índices
    coincidencias = []
    for idx, pais in enumerate(dataset_paises):
        if pais["Nombre"].lower() == nombre_buscar:
            coincidencias.append((idx, pais))

    if not coincidencias:
        print(f"Error: El país '{nombre_buscar.title()}' no se encuentra en la lista.")
        return

    #Utilizamos el método pop para eliminar el país
    if len(coincidencias) == 1:
        idx_eliminar = coincidencias[0][0]
        pais_eliminado = dataset_paises.pop(idx_eliminar)
        print(f"Se ha eliminado el país: {pais_eliminado['Nombre'].title()}")
    
    else:
        print(f"Se encontraron {len(coincidencias)} registros para '{nombre_buscar.title()}':")
        print(f"{'N°':<3} | {'Nombre':<20} | {'Población':<15} | {'Superficie (km²)':<18} | {'Continente':<15}")
        print("-" * 80)
        for i, (idx, pais) in enumerate(coincidencias, 1):
            print(f"{i:<3} | {pais['Nombre'].title():<20} | {pais['Poblacion']:<15,} | {pais['Superficie']:<18,} | {pais['Continente'].title():<15}")

        #Si ocurre más de una coincidencia
        while True:
            try:
                seleccion = input("Seleccione el N° del registro que desea eliminar (o 0 para cancelar): ").strip()
                val_espacio_vacio(seleccion)
                caracteres_especiales(seleccion)
                validar_not_is_alpha(seleccion)
                seleccion = int(seleccion)

                if seleccion == 0:
                    print("Operación cancelada.")
                    return
                if seleccion < 1 or seleccion > len(coincidencias):
                    raise ValueError(f"Error. Seleccione un número entre 1 y {len(coincidencias)}.")
                break
            except ValueError as e:
                print(e)

        idx_real = coincidencias[seleccion - 1][0]
        pais_eliminado = dataset_paises.pop(idx_real)
        print(f"Se ha eliminado el registro de {pais_eliminado['Nombre'].title()} con población de {pais_eliminado['Poblacion']:,}.")

    #Se actualiza el archivo csv
    try:
        with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
            columnas = ["Nombre", "Poblacion", "Superficie", "Continente"]
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader() 
            escritor.writerows(dataset_paises) 
        print("¡El archivo CSV ha sido actualizado correctamente!")
    except Exception as e:
        print(f"Error al guardar los cambios en el archivo: {e}")


#Actualizar datos de un país   
def actualizar_datos(nombre_archivo):
    while True:
        try:
            nombre_buscar = input("Ingrese el nombre del país que desea actualizar: ").lower()
            val_espacio_vacio(nombre_buscar)
            caracteres_especiales(nombre_buscar)
            validar_not_is_digit(nombre_buscar)
            break
        except ValueError as e:
            print(e)

    #Creamos una variable para el país encontrado
    pais_encontrado = None

    for pais in dataset_paises:
        if pais["Nombre"].lower() == nombre_buscar.lower():
            #Reemplazamos el valor de país encontrado con la coincidencia
            pais_encontrado = pais
            break

    if not pais_encontrado:
        print(f"Error: El país '{nombre_buscar}' no se encuentra en la lista.")
        return
        
    print(f"Actualizando datos de: {pais_encontrado['Nombre']}")
    print("""
        1) Actualizar la Población.
        2) Actualizar la Superficie.  
        """)
    
    while True:
        try:
            opcion = input("Ingrese una opción (1-2): ")
            val_espacio_vacio(opcion)
            caracteres_especiales(opcion)
            validar_not_is_alpha(opcion)
            
            opcion = int(opcion)

            if opcion < 1 or opcion > 2:
                raise ValueError("Error. Debe seleccionar una opción (1-2).")
            
            break   
        except ValueError as e:
                print(e)
    #Actualizar población
    if opcion == 1:
        while True:
            try:
                nueva_poblacion = input(f"Ingrese la nueva población para {pais_encontrado['Nombre']}: ")
                val_espacio_vacio(nueva_poblacion)
                caracteres_especiales(nueva_poblacion)
                if not nueva_poblacion.isdigit():
                    raise ValueError("La población debe contener solo números.")
                pais_encontrado["Poblacion"] = int(nueva_poblacion)
                break
            except ValueError as e:
                print(e)
    
    #Actualizar superficie
    else:
        while True:
            try:
                nueva_superficie = input(f"Ingrese la nueva superficie para {pais_encontrado['Nombre']}: ").strip()
                val_espacio_vacio(nueva_superficie)
                caracteres_especiales(nueva_superficie)
                if not nueva_superficie.isdigit():
                    raise ValueError("Error. La superficie debe contener solo números.")
                    
                pais_encontrado["Superficie"] = int(nueva_superficie)
                break
            except ValueError as e:
                print(e)

    #Actualizar los datos en el archivo csv    
    try:
        with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
            columnas = ["Nombre", "Poblacion", "Superficie", "Continente"]
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader() 
            escritor.writerows(dataset_paises) 
                
        print(f"¡Datos de {pais_encontrado['Nombre']} actualizados correctamente!")
        
    except Exception as e:
        print(f"Error al intentar escribir en el archivo: {e}")

#Buscar la información de un país
def buscar_pais():
    print("Buscar País.")
    while True:
        try:
            busqueda = input("Ingrese el nombre (o parte del nombre) del país: ").strip().lower()
            val_espacio_vacio(busqueda)
            caracteres_especiales(busqueda)
            validar_not_is_digit(busqueda)
            break
        except ValueError as e:
            print(e)

    #Guarda las coincidencias
    coincidencias = []

    for pais in dataset_paises:
        if busqueda.lower() in pais["Nombre"].lower():
            coincidencias.append(pais)

    if coincidencias:
        print(f"Se encontraron {len(coincidencias)} coincidencia(s):")
        print("-" * 75)
        print(f"{'Nombre':<20} | {'Población':<15} | {'Superficie (km²)':<18} | {'Continente':<15}")
        print("-" * 75)
        for pais in coincidencias:
            print(f"{pais['Nombre']:<20} | {pais['Poblacion']:<15,} | {pais['Superficie']:<18,} | {pais['Continente']:<15}")
        print("-" * 75)
    else:
        print(f"No se encontraron países que coincidan con '{busqueda}'.")

#Filtros
def filtrar_paises():
    print("Filtrar Países")
    print("""
    1) Filtrar por Continente.
    2) Filtrar por Rango de Población.
    3) Filtrar por Rango de Superficie.
    """)
    
    while True:
        try:
            opcion = input("Ingrese una opción (1-3): ").strip()
            val_espacio_vacio(opcion)
            caracteres_especiales(opcion)
            validar_not_is_alpha(opcion)
            
            opcion = int(opcion)
            if opcion < 1 or opcion > 3:
                raise ValueError("Error. Debe seleccionar una opción entre (1-3).")
            break
        except ValueError as e:
            print(e)
    #Guarda los resultados
    resultados = []

    #Busca países por continente
    if opcion == 1:
        while True:
            try:
                continente_buscar = input("Ingrese el continente a filtrar: ").strip().lower()
                val_espacio_vacio(continente_buscar)
                caracteres_especiales(continente_buscar)
                validar_not_is_digit(continente_buscar)
                break
            except ValueError as e:
                print(e)
        
        for pais in dataset_paises:
            if continente_buscar.lower() in pais["Continente"].lower():
                resultados.append(pais)

    #Filtra por rango de población, usando max y min
    elif opcion == 2:
        while True:
            try:
                pob_min = input("Ingrese la población mínima: ").strip()
                val_espacio_vacio(pob_min)
                caracteres_especiales(pob_min)
                if not pob_min.isdigit():
                    raise ValueError("Error. La población mínima debe contener solo números enteros.")
                pob_min = int(pob_min)
                break
            except ValueError as e:
                print(e)
        
        while True:
            try:
                pob_max = input("Ingrese la población máxima: ").strip()
                val_espacio_vacio(pob_max)
                caracteres_especiales(pob_max)
                if not pob_max.isdigit():
                    raise ValueError("Error. La población máxima debe contener solo números enteros.")
                pob_max = int(pob_max)
                
                if pob_max < pob_min:
                    raise ValueError("Error. La población máxima no puede ser menor que la mínima.")
                break
            except ValueError as e:
                print(e)

        #Agrega la información a la lista resultados 
        for pais in dataset_paises:
            if pob_min <= pais["Poblacion"] <= pob_max:
                resultados.append(pais)

    #Filtra por rango de superficies, usando max y min
    elif opcion == 3:
        while True:
            try:
                sup_min = input("Ingrese la superficie mínima (km²): ").strip()
                val_espacio_vacio(sup_min)
                caracteres_especiales(sup_min)
                if not sup_min.isdigit():
                    raise ValueError("Error. La superficie mínima debe contener solo números enteros.")
                sup_min = int(sup_min)
                break
            except ValueError as e:
                print(e)
        
        while True:
            try:
                sup_max = input("Ingrese la superficie máxima (km²): ").strip()
                val_espacio_vacio(sup_max)
                caracteres_especiales(sup_max)
                if not sup_max.isdigit():
                    raise ValueError("Error. La superficie máxima debe contener solo números enteros.")
                sup_max = int(sup_max)
                
                if sup_max < sup_min:
                    raise ValueError("Error. La superficie máxima no puede ser menor que la mínima.")
                break
            except ValueError as e:
                print(e)

        for pais in dataset_paises:
            if sup_min <= pais["Superficie"] <= sup_max:
                resultados.append(pais)
    #Imprime los resultados
    if resultados:
        print(f"Se encontraron {len(resultados)} país(es) con el filtro seleccionado:")
        print("-" * 75)
        print(f"{'Nombre':<20} | {'Población':<15} | {'Superficie (km²)':<18} | {'Continente':<15}")
        print("-" * 75)
        for pais in resultados:
            print(f"{pais['Nombre']:<20} | {pais['Poblacion']:<15,} | {pais['Superficie']:<18,} | {pais['Continente']:<15}")
        print("-" * 75)
    else:
        print("No se encontraron países que cumplan con los criterios de filtrado especificados.")

#Función para ordenar países
def ordenar_paises():
    if not dataset_paises:
        print("No hay países registrados para ordenar.")
        return

    print("Ordenar Países")
    print("""
    1) Ordenar alfabéticamente (A-Z).
    2) Ordenar por rango de población.
    3) Ordenar por superficie de mayor a menor.
    """)
    while True:
        try:
            opcion = input("Seleccione una opción de ordenamiento (1-3): ").strip()
            val_espacio_vacio(opcion)
            caracteres_especiales(opcion)
            validar_not_is_alpha(opcion)
            opcion = int(opcion)
            if opcion < 1 or opcion > 3:
                raise ValueError("Error. Debe seleccionar una opción entre (1-3).")
            break
        except ValueError as e:
            print(e)

    if opcion == 1:
        # Orden alfabético de la A a la Z
        paises_ordenados = sorted(dataset_paises, key=lambda x: x["Nombre"].lower())
        criterio_texto = "Alfabéticamente (A-Z)"

    elif opcion == 2:
        # Orden por población (rango descendente o ascendente)
        print("""
        Seleccione el sentido del rango de población:
        1) De menor a mayor (Ascendente).
        2) De mayor a menor (Descendente).
        """)
        while True:
            try:
                sentido = input("Seleccione una opción (1-2): ").strip()
                val_espacio_vacio(sentido)
                caracteres_especiales(sentido)
                validar_not_is_alpha(sentido)
                sentido = int(sentido)
                if sentido < 1 or sentido > 2:
                    raise ValueError("Error. Debe seleccionar una opción entre 1 y 2.")
                break
            except ValueError as e:   
                print(e)
        
        reversa = (sentido == 2)
        paises_ordenados = sorted(dataset_paises, key=lambda x: x["Poblacion"], reverse=reversa)
        criterio_texto = "Rango de Población (De mayor a menor)" if reversa else "Rango de Población (De menor a mayor)"

    elif opcion == 3:
        #Orden por superficie de mayor a menor
        paises_ordenados = sorted(dataset_paises, key=lambda x: x["Superficie"], reverse=True)
        criterio_texto = "Superficie (De mayor a menor)"

    print(f"\nLista de países ordenada por: {criterio_texto}")
    print("-" * 75)
    print(f"{'Nombre':<20} | {'Población':<15} | {'Superficie (km²)':<18} | {'Continente':<15}")
    print("-" * 75)
    for pais in paises_ordenados:
        nombre_formateado = pais['Nombre'].title()
        continente_formateado = pais['Continente'].title()
        print(f"{nombre_formateado:<20} | {pais['Poblacion']:<15,} | {pais['Superficie']:<18,} | {continente_formateado:<15}")
    print("-" * 75)

#Función para mostrar estadísticas
def mostrar_estadisticas():
    if not dataset_paises:
        print("No hay países registrados para generar estadísticas.")
        return

    while True:
        print("""
               MENÚ DE ESTADÍSTICAS:
        1) País con mayor y menor población.
        2) Promedio de población y superficie.
        3) Cantidad de países por continente.
        4) Volver al menú principal.
        """)
        try:
            opcion = input("Seleccione una opción de estadísticas (1-4): ").strip()
            val_espacio_vacio(opcion)
            caracteres_especiales(opcion)
            validar_not_is_alpha(opcion)
            opcion = int(opcion)

            if opcion < 1 or opcion > 4:
                raise ValueError("Error. Debe seleccionar una opción entre (1-4).")

            #Utilizamos max y min para ver los países con mayor y menor población
            if opcion == 1:
                pais_mas_poblado = max(dataset_paises, key=lambda x: x["Poblacion"])
                pais_menos_poblado = min(dataset_paises, key=lambda x: x["Poblacion"])
                print("PAÍSES EXTREMOS EN POBLACIÓN")
                print(f"País con MAYOR población: {pais_mas_poblado['Nombre'].title()} ({pais_mas_poblado['Poblacion']:,} hab.)")
                print(f"País con MENOR población: {pais_menos_poblado['Nombre'].title()} ({pais_menos_poblado['Poblacion']:,} hab.)")

            #Cálculos de promedios
            elif opcion == 2:
                total_pob = sum(p["Poblacion"] for p in dataset_paises)
                total_sup = sum(p["Superficie"] for p in dataset_paises)
                promedio_pob = total_pob / len(dataset_paises)
                promedio_sup = total_sup / len(dataset_paises)
                print("PROMEDIOS GENERALES")
                print(f"Promedio de Población:  {promedio_pob:,.2f} habitantes.")
                print(f"Promedio de Superficie: {promedio_sup:,.2f} km².")

            #Conteo de países por continente
            elif opcion == 3:
                conteo_continentes = {}
                for pais in dataset_paises:
                    cont = pais["Continente"].title()
                    conteo_continentes[cont] = conteo_continentes.get(cont, 0) + 1
                print("CANTIDAD DE PAÍSES POR CONTINENTE")
                for continente, cantidad in conteo_continentes.items():
                    print(f" - {continente:<20}: {cantidad} país(es)")

            #Opción para volver al menú principal
            elif opcion == 4:
                break 

            input("Presione ENTER para continuar en Estadísticas...")

        except ValueError as e:
            print(e)
            input("Presione ENTER para continuar...")

#Función para detener la ejecución de la aplicación
def salir():
    while True:
        try:
            print("Sesión finalizada.")
            break
        except ValueError as e:
                    print(e)

#Función para el menú principal, donde llamamos a las funciones para cada opción
def menu():
    while True:
        imprimir_menu()
        try:
            opcion = input("Ingrese una opción del menú(1-8): ")

            #Validaciones para las entradas del usuario
            val_espacio_vacio(opcion)

            caracteres_especiales(opcion)

            validar_not_is_alpha(opcion)

            opcion = int(opcion)

            if opcion < 1 or opcion > 8:
                raise ValueError("La opción debe estar entre (1-8)")
            
            if opcion == 1:
                agregar_pais("paises.csv")
            
            if opcion == 2:
                actualizar_datos("paises.csv")
            
            if opcion == 3:
                buscar_pais()

            if opcion == 4:
                filtrar_paises()
            
            if opcion == 5:
                ordenar_paises()
            
            if opcion == 6:
                mostrar_estadisticas()

            if opcion == 7:
                eliminar_pais("paises.csv")

            if opcion == 8:
                salir()
                break

        except ValueError as e:
            print(e)
            
#Ejecución del menú principal
menu()


