import sqlite3


class AdministraDB:
    def __init__(self, ruta):
        self.ruta = ruta

    def leeRecords(self):
        '''Este metodo se encarga de consultar los datos guardados
        en la base de datos.'''

        # Consulta a realizar
        consulta = "SELECT * FROM records ORDER BY puntos DESC LIMIT 5"

        # Conecta con la base de datos
        conexion = sqlite3.connect(self.ruta)

        # Crear en cursor de consulta
        cursor = conexion.cursor()

        # Transmitir la consulta para ejecutarla en SQL
        cursor.execute(consulta)

        records = []
        nombres_columnas = []

        for desc_columna in cursor.description:
            nombres_columnas.append(desc_columna[0])

        datos = cursor.fetchall()
        for dato in datos:
            record = {}
            indice = 0
            for nombre in nombres_columnas:
                record[nombre] = dato [indice]
                indice += 1
            records.append(record)

        conexion.close()

        return records

    def almacenaRecord(self, nombre, puntos):
        '''Este metodo sirve para poder guardar un nuevo record
        en la base de datos'''

        # Consulta a realizar para introducir el nuevo record
        consulta = "INSERT INTO records (Nombre,Puntos) VALUES (?,?)"
        
        # Conexion con la base de datos
        conexion = sqlite3.connect(self.ruta)
        
        # Cursor
        cursor = conexion.cursor()

        # Ejecucion de la consulta
        cursor.execute(consulta, (nombre, puntos))

        # Realizacion del commit para guardar
        conexion.commit()
        
        # Cerrar conexion
        conexion.close()

    def puntuacionMayor(self):
        '''Este metodo usa el diccionario generado por leeRecords para recoger unicamente
        el valor de Puntos y luego lo ordena de mayor a menor para obtener el jugador
        que mas puntos hizo'''  
        records = self.leeRecords()
        puntuaciones  = [x["Puntos"] for x in records]           
        puntuaciones.sort(reverse=True)
        
        return puntuaciones[0]
    
        