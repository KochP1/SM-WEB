from flask import Flask
from flask import render_template, redirect, request, session, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import pymysql
import pymysql.cursors
from werkzeug.security import generate_password_hash


# INICIALIZACION DE LA APLICACION FLASK
app = Flask(__name__, template_folder="templates")

#app.config["MYSQL_CURSORCLASS"]="dictCursor"
#mysql = MySQL(app)

db = pymysql.connect(
    host='junction.proxy.rlwy.net',
    port=30481,
    user='root',
    password='YRyowWnclqRtxerAfrQBndKOVcyauzzG',
    database='sm'
)
app.config["SECRET_KEY"] = "1145"  # Define la clave secreta antes de acceder a la sesión

# Función para verificar si la conexión a la base de datos es exitosa

try:
        with db.cursor() as cursor:
            # Ejecutar una consulta sencilla para comprobar la conexión
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("Conexion")
            else:
                print("error")
except pymysql.Error as e:
        print(f"Error al conectar a la base de datos: {e}")


# Configuración de Flask-Mail y Serializer
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'juanandreskochp@gmail.com'
app.config['MAIL_PASSWORD'] = 'nlyl open nvhv dtlg'
app.config['MAIL_DEFAULT_SENDER'] = 'juanandreskochp@gmail.com'
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

app.app_context().push()





#                             SM WEB

# MOSTRAR PANTALLA DE INICIO
@app.route("/")
def home():
    return render_template("index.html")

# FUNCION PARA LOS DOS TIPOS DE USUARIOS 
@app.route("/login", methods=["POST"])
def login():

    # INICIO DE SESION
    email = request.form['email']
    contraseña = request.form['contraseña']

    if email and contraseña:
        cur = db.cursor()
        #cur.execute("SELECT * FROM login WHERE email = %s AND contraseña = %s", (email, contraseña))
        cur.execute("SELECT * FROM login WHERE email = %s", (email,))
        user = cur.fetchone()

        if user is not None:
            session['id'] = user[0]
            session['email'] = email
            session['name'] = user[1]
            session['surname'] = user[2]
            session['contraseña'] =  contraseña
            return redirect(url_for('inbox'))

        cur.execute("SELECT * FROM usuarios_tiendas WHERE email = %s", (email,))
        user = cur.fetchone()
        if user is not None:
            session['id'] = user[0]
            session['email'] = email
            session['name'] = user[1]
            session['surname'] = user[2]
            session['contraseña'] =  contraseña
            session['tienda'] = user[3]
            print(session['tienda'])
            return redirect(url_for('tiendasUI'))
        else:
            return render_template('index.html', message="Las credenciales no son correctas")
    



# Template de registro de usuarios
@app.route("/regist", methods=['GET'])
def regist():
    return render_template('regist.html')



# Creacion de usuarios
@app.route("/user_regist", methods=['POST'])
def userRegist():
    name = request.form['name']
    surname = request.form['surname']
    tienda = request.form['tienda']
    email = request.form['email']
    contraseña = request.form['contraseña']
    if len(contraseña) > 12:
        return render_template('regist.html', message = 'La contraseña tiene un maximo de 12 caracteres') 
    tipo = request.form['tipo-usuario']
    cont_hash = generate_password_hash(contraseña, method='scrypt')

    try:

      if tipo == 'tienda':
        sql = "INSERT INTO usuarios_tiendas (name, surname, tienda, email, contraseña) VALUES (%s, %s, %s, %s, %s)"
        data = (name, surname, tienda, email, cont_hash)
      elif tipo == 'sambil':
        sql = "INSERT INTO login (name, surname, email, contraseña) VALUES (%s, %s, %s, %s)"
        data = (name, surname, email, cont_hash)
      else:
        return render_template('regist.html', message = 'Debe escoger el tipo de usuario')

      cur = db.cursor()
      cur.execute(sql, data)
      db.commit()
      cur.close()  # Cerrar el cursor después de ejecutar la consulta

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
        else:
            return render_template('index.html', message=error_message)



# Template del inbox para el departamento de fallas 
@app.route("/inbox", methods=['GET'])
def inbox():
    cur = db.cursor()
    cur.execute("SELECT * FROM odt")
    fallas = cur.fetchall()
    insertObject = []
    columNamnes = [column[0] for column in cur.description]
    for record in fallas:
          insertObject.append(dict(zip(columNamnes, record)))
    cur.close()
    return render_template('inbox.html', fallas = insertObject)


# Funcion para buscar una falla filtrando por fecha
@app.route("/date-filter", methods=['POST'])
def dateFilter():
    fecha1 = request.form['fecha-1']
    fecha2 = request.form['fecha-2']
    
    cur = db.cursor()
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

@app.route("/search", methods = ['POST'])
def searchName():
    tienda = request.form['tienda']
    cur = db.cursor()
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



# Funcion para editar las fallas almacenadas 

@app.route("/edit-falla", methods=['POST'])
def editFalla():
    tienda = request.form['tienda']
    name = request.form['name']
    surname = request.form['surname']
    area = request.form['area']
    tipo = request.form['tipo']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    idFalla = request.form['id']

    cur = db.cursor()
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
          cur = db.cursor()
          sql = 'UPDATE odt SET name = %s, surname = %s, tienda = %s, area = %s, tipo = %s, descripcion = %s, fecha = %s WHERE id = %s'
          data = (name, surname, tienda, area, tipo, descripcion, fecha, idFalla)
          cur.execute(sql, data)
          db.commit()
          cur.close()
          return redirect(url_for('inbox'))
    except pymysql.Error as e:
        if "Data too long for column 'descripcion'" in str(e):
            return render_template('inbox.html', message='La descripcion tiene un maximo de 80 caracteres', fallas = insertObject)
        else:
            return render_template('inbox.html', message='Todos los campos son obligatorios', fallas = insertObject)



# Template para la gestion de usuarios del sambil

@app.route("/editUser", methods=['GET'])
def editUser():
    return render_template('editUser.html')


# Funcion para editar usuarios del sambil
@app.route("/edit-user", methods = ['POST'])
def editUsers():
    ID = session['id']
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    contAct = request.form['contraseña_Act']
    cont = request.form['contraseña']
    if len(cont) > 12:
        return render_template('editUser.html', message = 'La contraseña tiene un maximo de 12 caracteres')

    try:

     if name and surname and email and cont and contAct == session['contraseña']:
        cur = cur = db.cursor()
        sql = "UPDATE login SET name = %s, surname = %s, email = %s, contraseña = %s WHERE id = %s"
        data = (name, surname, email, cont, ID)
        cur.execute(sql, data)
        db.commit()
        cur.close()
        return redirect(url_for('home'))
     elif name and surname and email:
        cur = db.cursor()
        sql = "UPDATE login SET name = %s, surname = %s, email = %s WHERE id = %s"
        data = (name, surname, email, ID)
        cur.execute(sql, data)
        db.commit()
        cur.close()
        return redirect(url_for('home'))
     else:
        return redirect(url_for('editUser', message = "Las contrasenas no coinciden"))
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

# Template para la vista de reportes de fallas

@app.route("/reporte-fallas", methods = ['GET'])
def reporteFallas():
    cur = db.cursor()
    cur.execute("SELECT * FROM odt")
    fallas = cur.fetchall()
    insertObject = []
    columNamnes = [column[0] for column in cur.description]
    for record in fallas:
          insertObject.append(dict(zip(columNamnes, record)))
    cur.close()
    return render_template('reporteFallas.html', fallas = insertObject)

# Template para la vista de reportes de tiendas registradas

@app.route("/reporte-tiendas", methods = ['GET'])
def reporteTiendas():
    cur = db.cursor()
    cur.execute("SELECT * FROM usuarios_tiendas")
    tiendas = cur.fetchall()
    insertObject = []
    columNamnes = [column[0] for column in cur.description]
    for record in tiendas:
          insertObject.append(dict(zip(columNamnes, record)))
    cur.close()

    return render_template("reporteTiendas.html", tiendas = insertObject)

# Template para las tiendas
@app.route("/tiendasUI", methods=['GET'])
def tiendasUI():
    email = session['email']
    cur = db.cursor()
    cur.execute("SELECT * FROM odt WHERE email = %s", [email])
    fallas = cur.fetchall()

    insertObject = []
    columNamnes = [column[0] for column in cur.description]
    for record in fallas:
        insertObject.append(dict(zip(columNamnes, record)))
    cur.close()
    return render_template('tiendasUI.html', fallas = insertObject)



# Agregar nueva falla
@app.route("/new-falla", methods=['POST'])
def newFalla():
    email = session['email']
    tienda = session['tienda']
    name = session['name']
    surname = session['surname']
    area = request.form['area']
    tipo = request.form['tipo']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']

    cur = db.cursor()
    cur.execute("SELECT * FROM odt WHERE email = %s", [email])
    fallas = cur.fetchall()

    insertObject = []
    columNamnes = [column[0] for column in cur.description]
    for record in fallas:
        insertObject.append(dict(zip(columNamnes, record)))

    if area == 'Selecciona un area':
            return render_template('tiendasUI.html', message='Debe seleccionar el area', fallas = insertObject)
    elif tipo == 'Selecciona un tipo':
            return render_template('tiendasUI.html', message='Debe seleccionar el tipo', fallas = insertObject)
    elif fecha == None:
            return render_template('tiendasUI.html', message='Todos los campos son obligatorios', fallas = insertObject)

    try:
     if tienda and area and tipo and descripcion and fecha:
         sql = "INSERT INTO odt (email, name, surname, tienda, area, tipo, descripcion, fecha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
         data = (email, name, surname, tienda, area, tipo, descripcion, fecha)
         cur.execute(sql, data)
         db.commit()
         return redirect(url_for('tiendasUI'))
         
    except pymysql.Error as e:
        if "Data too long for column 'descripcion'" in str(e):
            return render_template('tiendasUI.html', message='La descripcion tiene un maximo de 80 caracteres', fallas = insertObject)
        else:
            return render_template('tiendasUI.html', message='Todos los campos son obligatorios', fallas = insertObject)




# Template para la gestiion de usuarios de las tiendas
@app.route("/editUserTiendas", methods=['GET'])
def editUserTiendas():
    return render_template('editUserTiendas.html')


# Funcion para editar usuarios de las tiendas
@app.route("/edit-user-tiendas", methods = ['POST'])
def editUsersTiendasFunc():
    idTiendas = request.form['id']
    name = request.form['name']
    surname = request.form['surname']
    tienda = request.form['tienda']
    email = request.form['email']
    cont_act = request.form['contraseña_Act']           
    cont = request.form['contraseña']
    if len(cont) > 12:
        return render_template('editUserTiendas.html', message = 'La contraseña tiene un maximo de 12 caracteres')

    try:
     if name and surname and tienda and email:
       if cont_act == session['contraseña']:
          cur = db.cursor()
          sql = "UPDATE usuarios_tiendas SET name = %s, surname = %s, tienda = %s, email = %s, contraseña = %s WHERE idTiendas = %s"
          data = (name, surname, tienda, email, cont, idTiendas)
          cur.execute(sql, data)
          db.commit()
          cur.close()
          return redirect(url_for('home'))
       else:
          return redirect(url_for('editUserTiendas'), message='Contraseña incorrecta')
     else:
        return redirect(url_for('editUserTiendas'), message='Los campos Nombre, apellido y Email no deben estar vacíos')
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

# Eliminar falla
@app.route("/delete-falla", methods=['POST'])
def deleteFalla():
    cur = db.cursor()
    id = request.form['id']
    sql = "DELETE FROM odt WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    db.commit()
    return redirect(url_for('inbox'))

# Template para olvidaste tu contrasena

@app.route("/forgot", methods = ['GET'])
def forgot():
    return render_template('forgotPassword.html')

# Funcion para verificar si el usuario existe en la base de datos de usuarios sambil
def verificar_email_en_bd(email):
    cur = db.cursor()
    cur.execute("SELECT * FROM login WHERE email = %s", (email,))
    usuario = cur.fetchone()
    cur.close()
    return usuario is not None

# Funcion para verificar si el usuario existe en la base de datos de usuarios tiendas
def verificar_email_en_bd_tiendas(email):
    cur = db.cursor()
    cur.execute("SELECT * FROM usuarios_tiendas WHERE email = %s", (email,))
    usuario = cur.fetchone()
    cur.close()
    return usuario is not None

# Funcion para el envio del correo de recuperacion

@app.route("/forgot-password", methods = ['POST'])
def forgotPassword():
    email = request.form['email']

    if verificar_email_en_bd(email):
        token = serializer.dumps(email, salt='reset-password')
        reset_url = url_for('recovery', token=token, _external=True)
        msg = Message('Restablecer contraseña',
                      sender='tu_correo_electronico',
                      recipients=[email])
        msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}'
        mail.send(msg)
        return render_template('forgotPassword.html', message_succes = 'REVISA TU GMAIL\n(Revisa tu bandeja de spam si no lo ves en el inbox)')
    elif verificar_email_en_bd_tiendas(email):
        token = serializer.dumps(email, salt='reset-password')
        reset_url = url_for('recovery', token=token, _external=True)
        msg = Message('Restablecer contraseña',
                      sender='tu_correo_electronico',
                      recipients=[email])
        msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}'
        mail.send(msg)
        return render_template('forgotPassword.html', message_succes = 'REVISA TU GMAIL\n(Revisa tu bandeja de spam si no lo ves en el inbox)')
    else:
        return render_template('forgotPassword.html', message = 'El correo electronico no esta registrado')
    

# Template de recuperacion de usuario
@app.route("/recovery", methods = ['GET'])
def recovery():
    return render_template('recovery.html')

# Funcion de recuperacion de usuario
@app.route("/recovery-password", methods = ['POST'])
def recoveryPassword():
    email = request.form['email']
    newPassword = request.form['newPassword']
    confirmPassword = request.form['confirmPassword']

    if verificar_email_en_bd(email) and newPassword == confirmPassword:
        cur = cur = db.cursor()
        sql = "UPDATE login SET contraseña = %s WHERE email = %s"
        data = (newPassword, email)
        cur.execute(sql, data)
        db.commit()
        cur.close()
        return redirect(url_for('home'))
    elif verificar_email_en_bd_tiendas(email) and newPassword == confirmPassword:
        cur = db.cursor()
        sql = "UPDATE usuarios_tiendas SET contraseña = %s WHERE email = %s"
        data = (newPassword, email)
        cur.execute(sql, data)
        db.commit()
        cur.close()
        return redirect(url_for('home'))
    elif newPassword != confirmPassword:
        return render_template('recovery.html', message = 'Las contraseña no coinciden')
    else:
        return render_template('recovery.html', message = 'El correo no esta registrado en la base de datos')


# Cierre de sesion
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)