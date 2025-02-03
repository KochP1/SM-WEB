from flask import request, session, redirect, render_template, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

class Usuario:
    def __init__(self, db):
        self.db = db

    def login(self):
        """
        Maneja el inicio de sesión de los usuarios.
        Verifica las credenciales en las tablas `login` y `usuarios_tiendas`.
        """
        email = request.form['email']
        contraseña = request.form['contraseña']

        if email and contraseña:
            cur = self.db.cursor()

            # Verificar en la tabla `login` (usuarios Sambil)
            cur.execute("SELECT * FROM login WHERE email = %s", (email,))
            user = cur.fetchone()

            if user is not None and check_password_hash(user[4], contraseña):
                session['id'] = user[0]
                session['email'] = email
                session['name'] = user[1]
                session['surname'] = user[2]
                session['contraseña'] = user[4]
                cur.close()
                return redirect(url_for('inbox'))

            # Verificar en la tabla `usuarios_tiendas` (usuarios Tiendas)
            cur.execute("SELECT * FROM usuarios_tiendas WHERE email = %s", (email,))
            user = cur.fetchone()

            if user is not None and check_password_hash(user[5], contraseña):
                session['id'] = user[0]
                session['email'] = email
                session['name'] = user[1]
                session['surname'] = user[2]
                session['tienda'] = user[3]
                session['contraseña'] = user[5]
                cur.close()
                return redirect(url_for('tiendasUI'))

            cur.close()

        return render_template('index.html', message="Las credenciales no son correctas")

    def userRegist(self):
        """
        Maneja el registro de nuevos usuarios.
        Valida los datos y los inserta en las tablas `login` o `usuarios_tiendas`.
        """
        name = request.form['name']
        surname = request.form['surname']
        tienda = request.form['tienda']
        email = request.form['email']
        contraseña = request.form['contraseña']
        clave = request.form['clave']
        tipo = request.form['tipo-usuario']

        if len(contraseña) > 12:
            return render_template('regist.html', message='La contraseña tiene un máximo de 12 caracteres')

        cont_hash = generate_password_hash(contraseña, method='scrypt')

        try:
            cur = self.db.cursor()

            if tipo == 'tienda':
                # Verificar si el nombre de la tienda ya existe
                cur.execute("SELECT tienda FROM usuarios_tiendas WHERE tienda = %s", (tienda,))
                if cur.fetchone():
                    cur.close()
                    return render_template('regist.html', message='El nombre de la tienda ya existe')

                # Insertar en la tabla `usuarios_tiendas`
                sql = "INSERT INTO usuarios_tiendas (name, surname, tienda, email, contraseña) VALUES (%s, %s, %s, %s, %s)"
                data = (name, surname, tienda, email, cont_hash)
            elif tipo == 'sambil':
                # Insertar en la tabla `login`
                sql = "INSERT INTO login (name, surname, email, contraseña, claveAcc) VALUES (%s, %s, %s, %s, %s)"
                data = (name, surname, email, cont_hash, clave)
            else:
                cur.close()
                return render_template('regist.html', message='Debe escoger el tipo de usuario')

            # Ejecutar la consulta
            cur.execute(sql, data)
            self.db.commit()
            cur.close()

            return render_template('index.html')

        except pymysql.Error as e:
            error_message = "Error de MySQL al ejecutar la consulta: {}".format(e)

            if "Data too long for column 'name'" in str(e):
                return render_template('regist.html', message='El nombre tiene un máximo de 20 caracteres')
            elif "Data too long for column 'surname'" in str(e):
                return render_template('regist.html', message='El apellido tiene un máximo de 25 caracteres')
            elif "Data too long for column 'tienda'" in str(e):
                return render_template('regist.html', message='La tienda tiene un máximo de 25 caracteres')
            elif "Data too long for column 'email'" in str(e):
                return render_template('regist.html', message='El email tiene un máximo de 45 caracteres')
            elif 'Cannot add or update a child row: a foreign key constraint fails (`sm`.`login`, CONSTRAINT `Acces` FOREIGN KEY (`claveAcc`) REFERENCES `Acceso` (`claveAcc`))':
                return render_template('regist.html', message='La clave de acceso no es correcta')
            else:
                return render_template('regist.html', message=e)
            
    def editUsersTiendasFunc(self):
        idTiendas = session['id']
        name = request.form['name']
        surname = request.form['surname']
        tienda = request.form['tienda']
        email = request.form['email']
        contAct = request.form['contraseña_Act']
        cont = request.form['contraseña']
        cont_hash = generate_password_hash(cont, method='scrypt')

        if len(cont) > 12:
            return render_template('editUserTiendas.html', message='La contraseña tiene un máximo de 12 caracteres')

        try:
            if name and surname and email and tienda:
                cur = self.db.cursor()
                if cont and contAct:
                    if check_password_hash(session['contraseña'], contAct):
                        sql = "UPDATE usuarios_tiendas SET name = %s, surname = %s, tienda = %s, email = %s, contraseña = %s WHERE idTiendas = %s"
                        data = (name, surname, tienda, email, cont_hash, idTiendas)
                    else:
                        return render_template('editUserTiendas.html', message="La contraseña es incorrecta")
                else:
                    sql = "UPDATE usuarios_tiendas SET name = %s, surname = %s, tienda = %s, email = %s WHERE idTiendas = %s"
                    data = (name, surname, tienda, email, idTiendas)

                cur.execute(sql, data)
                self.db.commit()
                cur.close()
                return redirect(url_for('home'))
            else:
                return render_template('editUserTiendas.html', message="Todos los campos son obligatorios")
        except pymysql.Error as e:
            error_message = "Error de MySQL al ejecutar la consulta: {}".format(e)

            if "Data too long for column 'name'" in str(e):
                return render_template('editUserTiendas.html', message='El nombre tiene un máximo de 20 caracteres')
            elif "Data too long for column 'surname'" in str(e):
                return render_template('editUserTiendas.html', message='El apellido tiene un máximo de 25 caracteres')
            elif "Data too long for column 'tienda'" in str(e):
                return render_template('editUserTiendas.html', message='La tienda tiene un máximo de 25 caracteres')
            elif "Data too long for column 'email'" in str(e):
                return render_template('editUserTiendas.html', message='El email tiene un máximo de 45 caracteres')
            else:
                return render_template('index.html', message=error_message)
    
    def editSambilUser(self):
        ID = session['id']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        contAct = request.form['contraseña_Act']
        cont = request.form['contraseña']
        cont_hash = generate_password_hash(cont, method='scrypt')
        if len(cont) > 12:
            return render_template('editUser.html', message = 'La contraseña tiene un maximo de 12 caracteres')

        try:
            if name and surname and email:
                if check_password_hash(session['contraseña'], contAct):
                    cur = self.db.cursor()
                    sql = "UPDATE login SET name = %s, surname = %s, email = %s, contraseña = %s WHERE id = %s"
                    data = (name, surname, email, cont_hash, ID)
                    cur.execute(sql, data)
                    self.db.commit()
                    return redirect(url_for('home'))
                else:
                    return render_template('editUser.html', message="La contraseña es incorrecta")
            else:
                cur = self.db.cursor()
                sql = "UPDATE login SET name = %s, surname = %s, email = %s WHERE id = %s"
                data = (name, surname, email, ID)
                cur.execute(sql, data)
                self.db.commit()
                cur.close()
                return redirect(url_for('home'))
        except pymysql.Error as e:
            error_message = "Error de MySQL al ejecutar la consulta: {}".format(e)

            if "Data too long for column 'name'" in str(e):
                return render_template('editUser.html', message='El nombre tiene un máximo de 20 caracteres')
            elif "Data too long for column 'surname'" in str(e):
                return render_template('editUser.html', message='El apellido tiene un máximo de 25 caracteres')
            elif "Data too long for column 'email'" in str(e):
                return render_template('editUser.html', message='El email tiene un máximo de 45 caracteres')
            else:
                return render_template('index.html', message=error_message)
    
    def cierreSesion(self):
        session.clear()
        return redirect(url_for('home'))