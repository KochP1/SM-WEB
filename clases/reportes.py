from flask import request, session, redirect, render_template, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

class Reportes:
    def __init__(self, db):
        self.db = db
    
    def capturarReportes(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM odt")
        reportes = cur.fetchall()
        self.insertReportes = []
        columNamnes = [column[0] for column in cur.description]
        for record in reportes:
            self.insertReportes.append(dict(zip(columNamnes, record)))
        cur.close()

    def mostrarReportes(self):
        self.capturarReportes()
        print(self.insertReportes)
        return render_template('reporteFallas.html', reportes = self.insertReportes)
    
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