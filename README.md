Proyecto de Gestión de Países (Python)

Universidad Tecnológica Nacional (UTN)
Carrera: Tecnicatura Universitaria en Programación a Distancia
Asignatura: Programación I
Participantes: Gaston Duarte, Selene Araceli Miño
Profesores: [Nombres de los docentes]

Objetivo del Proyecto

La aplicación tiene como objetivo gestionar información detallada sobre distintos países a partir de la lectura y escritura en un archivo de datos CSV (para lo cual se utiliza la biblioteca nativa csv de Python).

El sistema interactúa con el usuario mediante una interfaz de consola clara, intuitiva y robusta, diseñada para capturar errores de ingreso de datos, guiar al usuario en cada paso y evitar cierres inesperados de la aplicación mediante un estricto control de excepciones y validaciones.

Características Principales

El sistema cuenta con un menú interactivo que permite realizar las siguientes operaciones:
Carga automática de datos desde un archivo CSV.
Agregar nuevos países persistiendo la información directamente en el archivo.
Eliminar registros controlando posibles duplicados.
Actualizar datos de población y superficie de los países existentes.
Buscar países mediante coincidencias parciales de texto.
Filtrar registros de forma avanzada por continente, población o superficie.
Ordenar el conjunto de datos bajo distintos criterios de ordenamiento.
Visualizar estadísticas clave del conjunto de datos.

Estructura y Modularización de la Aplicación
El proyecto se estructuró bajo el principio de modularización, distribuyendo la lógica en funciones específicas para facilitar el mantenimiento y la lectura del código. El punto de entrada principal (main) de la aplicación se gestiona desde la función menu_principal().

Descripción de las Funciones:

cargar_paises(): Lee el archivo CSV utilizando el modo de lectura ("r") y la codificación utf-8 para garantizar la correcta visualización de caracteres especiales (ñ, tildes, etc.). La información recolectada se almacena en memoria dentro de una lista de diccionarios llamada dataset_paises.

agregar_pais(): Permite dar de alta un nuevo país. Trabaja con el archivo en modo de anexado ("a") para escribir la nueva fila al final del archivo sin alterar los registros existentes.

eliminar_pais(): Busca el registro que se desea remover utilizando índices de listas y lo elimina mediante el método .pop(). En caso de encontrar países duplicados (por ejemplo, cargados por error), el sistema detecta la situación y le permite al usuario elegir de forma segura cuál de los dos registros desea eliminar.

actualizar_datos(): Permite modificar la información de población o superficie de un país en el dataset, realizando la búsqueda a través del valor de la clave "Nombre".

buscar_pais(): Muestra la información completa de un país. Implementa una búsqueda por coincidencia parcial de caracteres (por ejemplo, al ingresar un término de búsqueda corto como "Arg", el sistema es capaz de encontrar y mostrar la información de "Argentina").

filtrar_paises(): Permite segmentar el conjunto de datos según tres criterios: por continente, por rango de población o por rango de superficie (estableciendo valores mínimos y máximos).

ordenar_paises(): Ordena la información de forma visual sin modificar el archivo original utilizando la función sorted(). El usuario puede elegir entre un orden alfabético (A-Z), por rango de población (ascendente o descendente) o por superficie (de mayor a menor). Para lograr esto, se emplean expresiones lambda y variables booleanas (True/False) en el parámetro reverse.

mostrar_estadisticas(): Procesa y resume la información de los países registrados mostrando:
El país con mayor y menor población (usando las funciones integradas max() y min()).
El promedio general de población y superficie (usando sum() y len()).
La cantidad de países agrupados por continente (utilizando un diccionario y el método .get() para contar las frecuencias de forma eficiente).

salir(): Finaliza la ejecución del programa de forma controlada.

Sistema de Validaciones y Control de Errores

Para garantizar que el programa sea robusto frente a ingresos incorrectos por parte del usuario, se implementó un sistema de validación que actúa en cada solicitud de datos:

Validación de espacios vacíos: Evita que el usuario presione ENTER directamente dejando campos vacíos.

Validación de caracteres especiales: Bloquea el ingreso de símbolos inválidos en campos de texto o numéricos.

Validación de tipos de datos: Asegura que se ingresen únicamente letras donde se requiere texto, y números donde se requieren datos numéricos (como población o superficie).

Bucle de persistencia (while True): Los menús y las entradas de datos se encuentran envueltos en bucles infinitos que se repiten de manera amigable hasta que el usuario ingrese una opción válida.

Estructura try - except: Toda la interacción y los posibles errores inesperados de conversión de tipos se controlan mediante excepciones de Python (ValueError). Esto evita que la aplicación sufra cierres abruptos ante cualquier imprevisto técnico.
