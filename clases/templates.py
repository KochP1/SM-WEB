from flask import Flask
from flask import render_template, redirect, request, session, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import pymysql
import pymysql.cursors

class Templates:
    def __init__(self, db):
        self.db = db


    def mostrarFallas(self):
        cur = self.db.cursor()
        cur.execute("SELECT tienda FROM usuarios_tiendas")
        self.tiendas = cur.fetchall()
        self.tiendas = [tienda[0] for tienda in self.tiendas]

        cur.execute("SELECT * FROM odt")
        fallas = cur.fetchall()
        self.insertObject = []
        columNamnes = [column[0] for column in cur.description]
        for record in fallas:
            self.insertObject.append(dict(zip(columNamnes, record)))
        cur.close()

    def getInbox(self):
        self.mostrarFallas()
        return render_template('inbox.html', fallas = self.insertObject, tiendas = self.tiendas)
    
    def mostrarFallasTiendas(self):
        email = session['email']
        cur = self.db.cursor()
        cur.execute("SELECT * FROM odt WHERE email = %s", [email])
        fallas_tiendas = cur.fetchall()

        self.insertObjectSesion = []
        columNamnes = [column[0] for column in cur.description]
        for record in fallas_tiendas:
            self.insertObjectSesion.append(dict(zip(columNamnes, record)))
        cur.close()
    
    def getTiendasUI(self):
        self.mostrarFallasTiendas()
        return render_template('tiendasUI.html', fallas = self.insertObjectSesion)