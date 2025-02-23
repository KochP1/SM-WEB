from flask import render_template
import pandas as pd
from io import BytesIO
from flask import send_file

class Reportes:
    def __init__(self, db):
        self.db = db
    

    # Reportes de fallas
    def capturarReportes(self):
        cur = self.db.cursor()
        cur.execute("SELECT nombre, apellido, tienda, area, tipo, descripcion, fecha, estado FROM odt")
        reportes = cur.fetchall()
        self.insertReportes = []
        columNamnes = [column[0] for column in cur.description]
        for record in reportes:
            self.insertReportes.append(dict(zip(columNamnes, record)))
        cur.close()

    def mostrarReportes(self):
        self.capturarReportes()
        return render_template('reporteFallas.html', reportes = self.insertReportes)
    
    def generar_excel(self):
        """
        Genera un archivo Excel con los reportes de fallas.
        """
        self.capturarReportes()

        # Convertir los datos a un DataFrame de Pandas
        df = pd.DataFrame(self.insertReportes)

        # Crear un archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Reportes")

        # Preparar el archivo para la descarga
        output.seek(0)
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="reportes.xlsx"
        )
    
    

    # Reportes de tiendas
    def capturarReportesTiendas(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM usuarios_tiendas")
        tiendas = cur.fetchall()
        self.insertTiendas = []
        columNamnes = [column[0] for column in cur.description]
        for record in tiendas:
            self.insertTiendas.append(dict(zip(columNamnes, record)))
        cur.close()
    
    def mostrarReportesTiendas(self):
        self.capturarReportesTiendas()
        return render_template("reporteTiendas.html", tiendas = self.insertTiendas)