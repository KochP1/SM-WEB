from flask import Flask
from flask import render_template, redirect, request, session, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import pymysql
import pymysql.cursors
from werkzeug.security import generate_password_hash, check_password_hash

class mail:
    def __init__(self, db, app):
        self.db = db

        self.app = app
        self.configure_email()
        self.mail = Mail(self.app)
        self.serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    def configure_email(self):
        """
        Configura los parámetros del servidor de correo electrónico.
        """
        self.app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        self.app.config['MAIL_PORT'] = 587
        self.app.config['MAIL_USE_TLS'] = True
        self.app.config['MAIL_USERNAME'] = 'juanandreskochp@gmail.com'
        self.app.config['MAIL_PASSWORD'] = 'uqpz jftw ckul snxm'
        self.app.config['MAIL_DEFAULT_SENDER'] = 'juanandreskochp@gmail.com'

    def verificar_email_en_bd(self, email):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM login WHERE email = %s", (email,))
        usuario = cur.fetchone()
        cur.close()
        return usuario is not None
    
    def verificar_email_en_bd_tiendas(self, email):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM usuarios_tiendas WHERE email = %s", (email,))
        usuario = cur.fetchone()
        cur.close()
        return usuario is not None
    

    def envioCorreo(self):
        email = request.form['email']

        if self.verificar_email_en_bd(email):
            token = self.serializer.dumps(email, salt='reset-password')
            reset_url = url_for('recovery', token=token, _external=True)
            msg = Message('Restablecer contraseña',
                        sender='tu_correo_electronico',
                        recipients=[email])
            msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}'
            self.mail.send(msg)
            return render_template('forgotPassword.html', message_succes = 'REVISA TU GMAIL\n(Revisa tu bandeja de spam si no lo ves en el inbox)')
        elif self.verificar_email_en_bd_tiendas(email):
            token = self.serializer.dumps(email, salt='reset-password')
            reset_url = url_for('recovery', token=token, _external=True)
            msg = Message('Restablecer contraseña',
                        sender='tu_correo_electronico',
                        recipients=[email])
            msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}'
            self.mail.send(msg)
            return render_template('forgotPassword.html', message_succes = 'REVISA TU GMAIL\n(Revisa tu bandeja de spam si no lo ves en el inbox)')
        else:
            return render_template('forgotPassword.html', message = 'El correo electronico no esta registrado')
    
    def recuperarCont(self):
        email = request.form['email']
        newPassword = request.form['newPassword']
        confirmPassword = request.form['confirmPassword']
        cont_hash = generate_password_hash(newPassword, method='scrypt')

        if self.verificar_email_en_bd(email) and newPassword == confirmPassword:
            cur = cur = self.db.cursor()
            sql = "UPDATE login SET contraseña = %s WHERE email = %s"
            data = (cont_hash, email)
            cur.execute(sql, data)
            self.db.commit()
            cur.close()
            return redirect(url_for('home'))
        elif self.verificar_email_en_bd_tiendas(email) and newPassword == confirmPassword:
            cur = self.db.cursor()
            sql = "UPDATE usuarios_tiendas SET contraseña = %s WHERE email = %s"
            data = (cont_hash, email)
            cur.execute(sql, data)
            self.db.commit()
            cur.close()
            return redirect(url_for('home'))
        elif newPassword != confirmPassword:
            return render_template('recovery.html', message = 'Las contraseña no coinciden')
        else:
            return render_template('recovery.html', message = 'El correo no esta registrado en la base de datos')