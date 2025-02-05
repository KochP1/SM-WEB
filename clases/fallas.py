from flask import request, session, redirect, render_template, url_for
import pymysql

class Falla:
    def __init__(self, db):
        self.db = db

    def newFallaSambil(self):
        email = session['email']
        tienda = request.form['tienda']
        name = session['name']
        surname = session['surname']
        area = request.form['area']
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        estado = 'En ejecucion'

        cur = self.db.cursor()
        cur.execute("SELECT * FROM odt")
        fallas = cur.fetchall()
        insertObject = []
        columNamnes = [column[0] for column in cur.description]
        for record in fallas:
            insertObject.append(dict(zip(columNamnes, record)))

        cur.execute("SELECT tienda FROM usuarios_tiendas")
        tiendas = cur.fetchall()
        tiendas = [tienda[0] for tienda in tiendas]

        if area == 'Selecciona un area':
            return render_template('inbox.html', message='Debe seleccionar el area', fallas = insertObject, tiendas = tiendas)
        elif tipo == 'Selecciona un tipo':
            return render_template('inbox.html', message='Debe seleccionar el tipo', fallas = insertObject, tiendas = tiendas)
        elif fecha == None:
            return render_template('inbox.html', message='Todos los campos son obligatorios', fallas = insertObject, tiendas = tiendas)

        try:
            if tienda and area and tipo and descripcion and fecha and tienda != 'Selecciona una tienda':
                sql = "INSERT INTO odt (email, name, surname, tienda, area, tipo, descripcion, fecha, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                data = (email, name, surname, tienda, area, tipo, descripcion, fecha, estado)
                cur.execute(sql, data)
                self.db.commit()
                return redirect(url_for('inbox'))
            else:
                return render_template('inbox.html', message='Todos los campos son obligatorios', fallas = insertObject, tiendas = tiendas)
            
            
        except pymysql.Error as e:
            if "Data too long for column 'descripcion'" in str(e):
                return render_template('inbox.html', message='La descripcion tiene un maximo de 80 caracteres', fallas = insertObject, tiendas = tiendas)
            else:
                return render_template('inbox.html', message='Todos los campos son obligatorios', fallas = insertObject, tiendas = tiendas)
            
    def filtrarFecha(self):
        fecha1 = request.form['fecha-1']
        fecha2 = request.form['fecha-2']
    
        cur = self.db.cursor()
        if fecha1 and fecha2:
            sql = "SELECT * FROM odt WHERE fecha BETWEEN %s AND %s"
            data = (fecha1, fecha2)
            cur.execute(sql, data)
        else:
            cur.execute("SELECT * FROM odt")

        fallas = cur.fetchall()
        insertObject = []
        columNamnes = [column[0] for column in cur.description]
        for record in fallas:
            insertObject.append(dict(zip(columNamnes, record)))
        cur.close()

        return render_template('inbox.html', fallas=insertObject)
    
    def filtrarNombre(self):
        tienda = request.form['tienda']
        cur = self.db.cursor()
        if tienda:
            sql = 'SELECT * FROM odt WHERE tienda = %s' 
            data = (tienda,)
            cur.execute(sql, data)
        else:
           cur.execute("SELECT * FROM odt")
        

        fallas = cur.fetchall()
        insertObject = []
        columNamnes = [column[0] for column in cur.description]
        for record in fallas:
            insertObject.append(dict(zip(columNamnes, record)))
        cur.close()

        return render_template('inbox.html', fallas=insertObject)
    
    def editarFallas(self):
        tienda = request.form['tienda']
        name = request.form['name']
        surname = request.form['surname']
        area = request.form['area']
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        idFalla = request.form['id']

        cur = self.db.cursor()
        cur.execute("SELECT * FROM odt")
        fallas = cur.fetchall()
        insertObject = []
        columNamnes = [column[0] for column in cur.description]
        for record in fallas:
            insertObject.append(dict(zip(columNamnes, record)))

        if area == 'Selecciona un area':
            return render_template('inbox.html', message='Debe seleccionar el area', fallas = insertObject)
        elif tipo == 'Selecciona un tipo':
            return render_template('inbox.html', message='Debe seleccionar el tipo', fallas = insertObject)
        elif fecha == None:
            return render_template('inbox.html', message='Todos los campos son obligatorios', fallas = insertObject)
    
        try:
            if name and surname and tienda and area and tipo and descripcion and fecha:
                cur = self.db.cursor()
                sql = 'UPDATE odt SET name = %s, surname = %s, tienda = %s, area = %s, tipo = %s, descripcion = %s, fecha = %s WHERE id = %s'
                data = (name, surname, tienda, area, tipo, descripcion, fecha, idFalla)
                cur.execute(sql, data)
                self.db.commit()
                cur.close()
                return redirect(url_for('inbox'))
            else:
                return render_template('inbox.html', message='Todos los campos son obligatorios', fallas = insertObject)
        except pymysql.Error as e:
            if "Data too long for column 'descripcion'" in str(e):
                return render_template('inbox.html', message='La descripcion tiene un maximo de 80 caracteres', fallas = insertObject)
            else:
                return render_template('inbox.html', message='Todos los campos son obligatorios', fallas = insertObject)
    
    def borrarFalla(self):
        cur = self.db.cursor()
        id = request.form['id']
        sql = "DELETE FROM odt WHERE id = %s"
        data = (id,)
        cur.execute(sql, data)
        self.db.commit()
        return redirect(url_for('inbox'))
    
    def nuevaFallaTiendas(self):
        email = session['email']
        tienda = session['tienda']
        name = session['name']
        surname = session['surname']
        area = request.form['area']
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        estado = 'En ejecucion'

        cur = self.db.cursor()
        cur.execute("SELECT * FROM odt WHERE email = %s AND estado = %s", (email, estado))
        fallas = cur.fetchall()

        insertObject = []
        columNames = [column[0] for column in cur.description]
        for record in fallas:
            insertObject.append(dict(zip(columNames, record)))

        # Validaciones de los campos del formulario
        if area == 'Selecciona un area':
            return render_template('tiendasUI.html', message='Debe seleccionar el area', fallas=insertObject)
        elif tipo == 'Selecciona un tipo':
            return render_template('tiendasUI.html', message='Debe seleccionar el tipo', fallas=insertObject)
        elif not fecha:
            return render_template('tiendasUI.html', message='Todos los campos son obligatorios', fallas=insertObject)

        try:
            if tienda and area and tipo and descripcion and fecha:
                sql = "INSERT INTO odt (email, name, surname, tienda, area, tipo, descripcion, fecha, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                data = (email, name, surname, tienda, area, tipo, descripcion, fecha, estado)
                cur.execute(sql, data)
                self.db.commit()
                return redirect(url_for('tiendasUI'))
            else:
                return render_template('tiendasUI.html', message='Todos los campos son obligatorios', fallas=insertObject)

        except pymysql.Error as e:
            if "Data too long for column 'descripcion'" in str(e):
                return render_template('tiendasUI.html', message='La descripcion tiene un maximo de 80 caracteres', fallas=insertObject)
            else:
                return render_template('tiendasUI.html', message='Error al insertar la falla', fallas=insertObject)