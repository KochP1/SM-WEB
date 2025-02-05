from flask import Flask
from flask import render_template
import pymysql
import pymysql.cursors
from clases.user import Usuario
from clases.fallas import Falla
from clases.templates import Templates
from clases.mail_server import mail
from clases.reportes import Reportes


# INICIALIZACION DE LA APLICACION FLASK
app = Flask(__name__, template_folder="templates")

db = pymysql.connect(
    host='junction.proxy.rlwy.net',
    port=30481,
    user='root',
    password='YRyowWnclqRtxerAfrQBndKOVcyauzzG',
    database='sm2.0'
)
app.config["SECRET_KEY"] = "1145"  # Define la clave secreta antes de acceder a la sesión

# Instancia de la clase Usuario
usuario_manager = Usuario(db)
fallas_manager = Falla(db)
templates_manager = Templates(db)
mail_manager = mail(db, app)
reportes_manager = Reportes(db)

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




app.app_context().push()





#                             SM WEB

# MOSTRAR PANTALLA DE INICIO
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    return usuario_manager.login()



# Template de registro de usuarios
@app.route("/regist", methods=['GET'])
def regist():
    return render_template('regist.html')



# Creacion de usuarios
@app.route("/user_regist", methods=['POST'])
def userRegist():
    return usuario_manager.userRegist()



# Template del inbox para el departamento de fallas 
@app.route("/inbox", methods=['GET'])
def inbox():
    return templates_manager.getInbox()


# Agregar nueva falla
@app.route("/new-falla-sambil", methods=['POST'])
def newFallaSambil():
    return fallas_manager.newFallaSambil()


# Funcion para buscar una falla filtrando por fecha
@app.route("/date-filter", methods=['POST'])
def dateFilter():
    return fallas_manager.filtrarFecha()

# Buscar fallas por nombre de tienda

@app.route("/search", methods = ['POST'])
def searchName():
    return fallas_manager.filtrarNombre()



# Funcion para editar las fallas almacenadas 

@app.route("/edit-falla", methods=['POST'])
def editFalla():
    return fallas_manager.editarFallas()



# Template para la gestion de usuarios del sambil

@app.route("/editUser", methods=['GET'])
def editUser():
    return render_template('editUser.html')


# Funcion para editar usuarios del sambil
@app.route("/edit-user", methods = ['POST'])
def editUsers():
    return usuario_manager.editSambilUser()

# Template para la vista de reportes de fallas

@app.route("/reporte-fallas", methods = ['GET'])
def reporteFallas():
    return reportes_manager.mostrarReportes()

@app.route("/descargar_excel", methods = ['GET'])
def descargar_excel():
    return reportes_manager.generar_excel()

# Template para la vista de reportes de tiendas registradas

@app.route("/reporte-tiendas", methods = ['GET'])
def reporteTiendas():
    return reportes_manager.mostrarReportesTiendas()

# Template para las tiendas
@app.route("/tiendasUI", methods=['GET'])
def tiendasUI():
    return templates_manager.getTiendasUI()



# Agregar nueva falla
@app.route("/new-falla", methods=['POST'])
def newFalla():
    return fallas_manager.nuevaFallaTiendas()


# Solucionar una falla

@app.route("/estado-falla", methods = ['POST'])
def solucionar():
    return fallas_manager.solucionarFalla()


# Template para la gestion de usuarios de las tiendas
@app.route("/editUserTiendas", methods=['GET'])
def editUserTiendas():
    return render_template('editUserTiendas.html')


# Funcion para editar usuarios de las tiendas
@app.route("/edit-user-tiendas", methods=['POST'])
def editUsersTiendasFunc():
        return usuario_manager.editUsersTiendasFunc()
        
# Eliminar falla usuarios administradores
@app.route("/delete-falla", methods=['POST'])
def deleteFalla():
        return fallas_manager.borrarFalla()


# Template para olvidaste tu contrasena

@app.route("/forgot", methods = ['GET'])
def forgot():
    return render_template('forgotPassword.html')



# Funcion para el envio del correo de recuperacion

@app.route("/forgot-password", methods = ['POST'])
def forgotPassword():
    return mail_manager.envioCorreo()
    

# Template de recuperacion de usuario
@app.route("/recovery", methods = ['GET'])
def recovery():
    return render_template('recovery.html')

# Funcion de recuperacion de usuario
@app.route("/recovery-password", methods = ['POST'])
def recoveryPassword():
    return mail_manager.recuperarCont()


# Cierre de sesion
@app.route("/logout")
def logout():
    return usuario_manager.cierreSesion()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)