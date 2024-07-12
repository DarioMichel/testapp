from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, make_response
from flask_mysqldb import MySQL, MySQLdb
from flask_bcrypt import bcrypt
import io
import xlwt
import pdfkit
import base64

AdminStateApp = Flask(__name__)
AdminStateApp.secret_key = 'adminstate@123'

AdminStateApp.config['MYSQL_HOST'] = 'localhost'
AdminStateApp.config['MYSQL_USER'] = 'root'
AdminStateApp.config['MYSQL_PASSWORD'] = 'Steve1305'
AdminStateApp.config['MYSQL_DB'] = 'medistik'
AdminStateApp.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(AdminStateApp)

@AdminStateApp.route('/')
def index():
    return render_template("login.html")

@AdminStateApp.route('/grafica')
def grafica():
    return render_template("grafica.html")

@AdminStateApp.route('/verReportes')
def verReportes():
    selReporte = mysql.connection.cursor()
    selReporte.execute("SELECT * FROM reporte ORDER BY reporte.Prioridad ASC")
    r = selReporte.fetchall()
    selReporte.close()
    return render_template('reportes.html', reporte = r)

@AdminStateApp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        UsTrabajador = request.form['UsTrabajador']
        ClaveT = request.form['ClaveT'].encode('utf-8')
        selUsuarioT = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        selUsuarioT.execute("SELECT * FROM empleadolo WHERE UsTrabajador = %s", (UsTrabajador,))
        u = selUsuarioT.fetchone()
        selUsuarioT.close()

        if u is not None:
            if bcrypt.hashpw(ClaveT, u["ClaveT"].encode('utf-8')) == u["ClaveT"].encode('utf-8'):
                session['NombreT'] = u["NombreT"]
                return redirect(url_for('sReporte'))
            else:
                flash('Clave Incorrecta, Intenta De Nuevo')
                return redirect(request.url)
        else:
            UsAlmacen = UsTrabajador
            Password = ClaveT
            selAlmacen = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            selAlmacen.execute("SELECT * FROM empleadoal WHERE UsAlmacen = %s", (UsAlmacen,))
            a = selAlmacen.fetchone()
            selAlmacen.close()
            if a is not None:
                if bcrypt.hashpw(Password, a["Password"].encode('utf-8')) == a["Password"].encode('utf-8'):
                    session['NombreUs'] = a["NombreUs"]
                    return redirect(url_for('sReporteal'))
                else:
                    flash('Clave Incorrecta, Intenta De Nuevo')
                    return redirect(request.url)
            else:
                flash('ERROR USUARIO NO EXISTE')
                return redirect(request.url)
    else:
        return render_template('login.html')

@AdminStateApp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        NombreT      = request.form['NombreT']
        UsTrabajador = request.form['UsTrabajador']
        PuestoT      = request.form['PuestoT']
        ClaveT       = request.form['ClaveT'].encode('utf-8')
        ClaveCifrada = bcrypt.hashpw(ClaveT, bcrypt.gensalt())
        regTrabajador = mysql.connection.cursor()
        regTrabajador.execute("INSERT INTO empleadolo (NombreT, UsTrabajador, PuestoT, ClaveT) VALUES(%s, %s, %s, %s)",(NombreT.upper(), UsTrabajador, PuestoT, ClaveCifrada))
        mysql.connection.commit()
        return redirect(url_for('login'))

@AdminStateApp.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template('login.html')

 #----------------------------CRUD PRODUCTO---------------------------------------------

@AdminStateApp.route('/sReporte', methods=["GET", "POST"])
def sReporte():
    selReporte = mysql.connection.cursor()
    selReporte.execute("SELECT * FROM reporte ORDER BY reporte.Prioridad ASC")
    r = selReporte.fetchall()
    selReporte.close()
    return render_template('dashboard.html', reporte = r)

@AdminStateApp.route('/acReporte/<IdReporte>', methods=["GET", "POST"])
def acReporte():
    if request.method == 'GET':
        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM `reporte` ORDER BY `reporte`.`IdReporte` DESC LIMIT 1")
        r = selReporte.fetchall()
        selReporte.close()

        selContenido = mysql.connection.cursor()
        selContenido.execute("SELECT * FROM reporte WHERE IdReporte = %s",(IdReporte,))
        c = selContenido.fetchall()
        selContenido.close()
        return render_template('actReporte.html', r = r,c = c)
    else:
        Contenedor    = request.form['Contenedor']
        Articulo      = request.form['Articulo']
        Descripcion   = request.form['Descripcion']
        Ubicacion     = request.form['Ubicacion']
        Lote          = request.form['Lote']
        Qty           = request.form['Qty']
        UM            = request.form['UM']
        Caducidad     = request.form['Caducidad']
        Temperatura   = request.form['Temperatura']

        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte ORDER BY IdReporte DESC LIMIT 1 ")
        r = selReporte.fetchall()
        selReporte.close()

        IdReporte     = r['IdReporte']
        insContenido = mysql.connection.cursor()
        insContenido.execute("INSERT INTO contenido (IdReporte, Contenedor, Articulo, Descripcion, Ubicacion, Lote, Qty, UM, Caducidad, Temperatura) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(IdReporte, Contenedor, Articulo, Descripcion, Ubicacion, Lote, Qty, UM, Caducidad, Temperatura))
        mysql.connection.commit()
        insContenido.close()
    return redirect(url_for('acReporte'))


#----------------------------i reporte inner join-------- SELECT * FROM reporte INNER JOIN contenido ON reporte.IdReporte = contenido.IdContenido -------------------------------------
@AdminStateApp.route('/formulario', methods = ["GET", "POST"])
def formulario():
    return render_template("formReport.html")
    
@AdminStateApp.route('/iReporte', methods = ["GET", "POST"])
def iReporte():
    if request.method == 'GET':
        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte")
        r = selReporte.fetchall()
        selReporte.close()

        selContenido = mysql.connection.cursor()
        selContenido.execute("SELECT * FROM contenido")
        c = selContenido.fetchall()
        selContenido.close()
        return render_template('formReport.html', r = r,c = c)
    else:
        SerClienteF    = request.form['SerClienteF']
        clienteF       = request.form['clienteF']
        TServicioF     = request.form['TServicioF']
        DestinoF       = request.form['DestinoF']
        VentanaF       = request.form['VentanaF']
        FechaF         = request.form['FechaF']
        Estatus        = request.form['Estatus']
        Prioridad      = request.form['Prioridad']
        Transportista  = request.form['Transportista']
        Comentarios   = request.form['Comentarios']
        Termino       = request.form['Termino']
        Revision      = request.form['Revision']
            
        Contenedor    = request.form['Contenedor']
        Articulo      = request.form['Articulo']
        Descripcion   = request.form['Descripcion']
        Ubicacion     = request.form['Ubicacion']
        Lote          = request.form['Lote']
        Qty           = request.form['Qty']
        UM            = request.form['UM']
        Caducidad     = request.form['Caducidad']
        Temperatura   = request.form['Temperatura']
    
        insReporte = mysql.connection.cursor()
        insReporte.execute("INSERT INTO reporte (SerClienteF, clienteF, TServicioF, DestinoF, VentanaF, FechaF, Estatus, Prioridad, Transportista, Comentarios, Termino, Revision) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(SerClienteF, clienteF, TServicioF, DestinoF, VentanaF, FechaF, Estatus, Prioridad, Transportista, Comentarios,Termino, Revision))
        mysql.connection.commit()
        insReporte.close()

        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte ORDER BY IdReporte DESC LIMIT 1 ")
        idr = selReporte.fetchone()
        selReporte.close()

        IdReporte     = idr['IdReporte']
        insContenido = mysql.connection.cursor()
        insContenido.execute("INSERT INTO contenido (IdReporte, Contenedor, Articulo, Descripcion, Ubicacion, Lote, Qty, UM, Caducidad, Temperatura) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(IdReporte, Contenedor, Articulo, Descripcion, Ubicacion, Lote, Qty, UM, Caducidad, Temperatura))
        mysql.connection.commit()
        insContenido.close()
        return redirect(url_for('verReportes'))

@AdminStateApp.route('/sformulario', methods = ["GET", "POST"])
def sformulario():
    if request.method == 'GET':
        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte ORDER BY reporte.IdReporte DESC LIMIT 1")
        r = selReporte.fetchone()
        selReporte.close()

        IdReporte     = r['IdReporte']
        selContenido = mysql.connection.cursor()
        selContenido.execute("SELECT * FROM `contenido` WHERE `contenido`.`IdReporte` = %s",(IdReporte,))
        c = selContenido.fetchall()
        selContenido.close()
        return render_template("uReporte.html", r=r, c=c)
    else:
        Contenedor    = request.form['Contenedor']
        Articulo      = request.form['Articulo']
        Descripcion   = request.form['Descripcion']
        Ubicacion     = request.form['Ubicacion']
        Lote          = request.form['Lote']
        Qty           = request.form['Qty']
        UM            = request.form['UM']
        Caducidad     = request.form['Caducidad']
        Temperatura   = request.form['Temperatura']

        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte ORDER BY IdReporte DESC LIMIT 1 ")
        idr = selReporte.fetchone()
        selReporte.close()

        IdReporte     = idr['IdReporte']
        insContenido = mysql.connection.cursor()
        insContenido.execute("INSERT INTO contenido (IdReporte, Contenedor, Articulo, Descripcion, Ubicacion, Lote, Qty, UM, Caducidad, Temperatura) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(IdReporte, Contenedor, Articulo, Descripcion, Ubicacion, Lote, Qty, UM, Caducidad, Temperatura))
        mysql.connection.commit()
        insContenido.close()
        return redirect(url_for('verReportes'))

@AdminStateApp.route('/sformulario4', methods = ["POST"])
def sformulario4():
        IdReporte     = request.form['IdReporte']
        SerClienteF   = request.form['SerClienteF']
        clienteF      = request.form['clienteF']
        TServicioF    = request.form['TServicioF']
        DestinoF      = request.form['DestinoF']
        VentanaF      = request.form['VentanaF']
        FechaF        = request.form['FechaF']
        Estatus       = request.form['Estatus']
        Prioridad     = request.form['Prioridad']
        Transportista = request.form['Transportista']
        Comentarios   = request.form['Comentarios']
        Termino       = request.form['Termino']
        Revision      = request.form['Revision']

        actReporte = mysql.connection.cursor()
        actReporte.execute("UPDATE reporte SET SerClienteF = %s, clienteF = %s, TServicioF = %s, DestinoF = %s, VentanaF = %s, FechaF = %s, Estatus = %s, Prioridad = %s, Transportista = %s, Comentarios = %s, Termino = %s, Revision = %s WHERE `reporte`.`IdReporte` = %s",(SerClienteF, clienteF, TServicioF, DestinoF, VentanaF, FechaF, Estatus, Prioridad, Transportista, Comentarios, Termino ,Revision, IdReporte))
        mysql.connection.commit()
        actReporte.close()
        return redirect(url_for('verReportes'))

@AdminStateApp.route('/sformulario2', methods = ["POST"])
def sformulario2():
        IdReporte     = request.form['IdReporte']
        SerClienteF   = request.form['SerClienteF']
        clienteF      = request.form['clienteF']
        TServicioF    = request.form['TServicioF']
        DestinoF      = request.form['DestinoF']
        VentanaF      = request.form['VentanaF']
        FechaF        = request.form['FechaF']
        Estatus       = request.form['Estatus']
        Prioridad     = request.form['Prioridad']
        Transportista = request.form['Transportista']
        Comentarios   = request.form['Comentarios']

        actReporte = mysql.connection.cursor()
        actReporte.execute("UPDATE reporte SET SerClienteF = %s, clienteF = %s, TServicioF = %s, DestinoF = %s, VentanaF = %s, FechaF = %s, Estatus = %s, Prioridad = %s, Transportista = %s, Comentarios = %s WHERE `reporte`.`IdReporte` = %s",(SerClienteF, clienteF, TServicioF, DestinoF, VentanaF, FechaF, Estatus, Prioridad, Transportista, Comentarios, IdReporte))
        mysql.connection.commit()
        actReporte.close()
        return redirect(url_for('verReportes'))

@AdminStateApp.route('/editar/<IdReporte>', methods=["GET"])
def editar(IdReporte):
    if request.method == 'GET':
        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte WHERE IdReporte = %s",(IdReporte,))
        r = selReporte.fetchall()
        selReporte.close()

        selContenido = mysql.connection.cursor()
        selContenido.execute("SELECT * FROM contenido WHERE contenido.IdReporte = %s",(IdReporte,))
        c = selContenido.fetchall()
        selContenido.close()
        return render_template('uReporte.html', r = r, c = c)
    else:
        IdContenido   = request.form['IdContenido']
        Contenedor    = request.form['Contenedor']
        Articulo      = request.form['Articulo']
        Descripcion   = request.form['Descripcion']
        Ubicacion     = request.form['Ubicacion']
        Lote          = request.form['Lote']
        Qty           = request.form['Qty']
        UM            = request.form['UM']
        Caducidad     = request.form['Caducidad']
        Temperatura   = request.form['Temperatura']

        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte WHERE IdReporte = %s",(IdReporte,))
        r = selReporte.fetchall()
        selReporte.close()

        IdReporte     = r['IdReporte']
        actContenido = mysql.connection.cursor()
        actContenido.execute("UPDATE contenido SET Contenedor = %s, Articulo = %s, Descripcion = %s, Ubicacion = %s, Lote = %s, Qty = %s, UM = %s, Caducidad = %s, Temperatura = %s WHERE IdContenido = %s",(Contenedor, Articulo, Descripcion, Ubicacion, Lote, Qty, UM, Caducidad, Temperatura, IdContenido))
        mysql.connection.commit()
        actContenido.close()
    return redirect(url_for('verReportes'))

@AdminStateApp.route('/uReporte', methods=["GET","POST"])
def uReporte():
        IdReporte      = request.form['IdReporte']
        SerClienteF    = request.form['SerClienteF']
        clienteF       = request.form['clienteF']
        TServicioF     = request.form['TServicioF']
        DestinoF       = request.form['DestinoF']
        VentanaF       = request.form['VentanaF']
        FechaF         = request.form['FechaF']
        Estatus        = request.form['Estatus']
        Prioridad      = request.form['Prioridad']
        Transportista  = request.form['Transportista']
        actReporte = mysql.connection.cursor()
        actReporte.execute("UPDATE reporte SET SerClienteF = %s, clienteF = %s, TServicioF = %s, DestinoF = %s, VentanaF = %s, FechaF = %s, Estatus = %s, Prioridad = %s, Transportista = %s  WHERE IdReporte = %s",(SerClienteF, clienteF, TServicioF, DestinoF, VentanaF, FechaF, Estatus, Prioridad, Transportista, IdReporte))
        mysql.connection.commit()
        actReporte.close()
        return redirect(url_for('verReportes'))

@AdminStateApp.route('/dReporte/<string:IdReporte>', methods=["GET"])
def dReporte(IdReporte):
    delReporte = mysql.connection.cursor()
    delReporte.execute("DELETE FROM reporte WHERE IdReporte = %s", (IdReporte,))
    mysql.connection.commit()
    return redirect(url_for('verReportes'))  

@AdminStateApp.route('/dContenido/<string:IdContenido>', methods=["GET"])
def dContenido(IdContenido):
    delContenido = mysql.connection.cursor()
    delContenido.execute("DELETE FROM `contenido` WHERE `contenido`.`IdContenido`= %s", (IdContenido,))
    mysql.connection.commit()
    return redirect(url_for('verReportes'))  
 #---------------------------- R E P O R T E - D E - E X E C E L ---------------------------------------------
@AdminStateApp.route('/rExecel/<IdReporte>', methods=["GET"])
def rExecel(IdReporte): 
    selReporte = mysql.connection.cursor()
    selReporte.execute("SELECT * FROM reporte WHERE IdReporte = %s",(IdReporte,))
    r = selReporte.fetchall()
    selReporte.close()
    

    selContenido = mysql.connection.cursor()
    selContenido.execute("SELECT * FROM contenido WHERE contenido.IdReporte = %s",(IdReporte,))
    c = selContenido.fetchall()
    selContenido.close()
    
    output = io.BytesIO()
    workbook = xlwt.Workbook()
    sh = workbook.add_sheet('Nota de Reporte')

    sh.write(1, 1, 'Servicio al cliente:')
    sh.write(1, 6, 'Fecha de embarque:')
    sh.write(3, 1, 'Oden de prioridad:')
    sh.write(3, 6, 'Estatus:')
    sh.write(4, 1, 'Cliente:')
    sh.write(5, 1, 'Destino:')
    sh.write(6, 1, 'Transportista:')
    #sh.write(8, 0, 'Comentarios:')
    sh.write(4, 6, 'Tipo de servicio:')
    sh.write(5, 6, 'Ventana:')
    

    sh.write(12, 0, 'No.')
    sh.write(12, 1, 'Contenedor')
    sh.write(12, 2, 'Articulo')
    sh.write(12, 3, 'Descripcion')
    sh.write(12, 4, 'Ubicacion')
    sh.write(12, 5, 'Lote')
    sh.write(12, 6, 'Qty')
    sh.write(12, 7, 'UM')
    sh.write(12, 8, 'Caducidad')
    sh.write(12, 9, 'Temperatura')
    
#    sh.write(0,8, '/static/img/lmedistik.png', {'x_offset': 3, 'y_offset': 5})
    
    idx = 0
    for row in r:
        sh.write(1, 3, row['SerClienteF'])
        sh.write(4, 2, row['clienteF'])
        sh.write(5, 2, row['DestinoF'])
        sh.write(4, 8, row['TServicioF'])
        sh.write(5, 7, row['VentanaF'])
        sh.write(1, 8, row['FechaF'])
        sh.write(3, 7, row['Estatus'])
        sh.write(3, 3, row['Prioridad'])
        sh.write(6, 2, row['Transportista'])
        #sh.write(8, 1, row['Comentarios'])
        idx += 1

    idx = 0
    for row in c:
        sh.write(13, 0, row['IdContenido'])
        sh.write(13, 1, row['Contenedor'])
        sh.write(13, 2, row['Articulo'])
        sh.write(13, 3, row['Descripcion'])
        sh.write(13, 4, row['Ubicacion'])
        sh.write(13, 5, row['Lote'])
        sh.write(13, 6, row['Qty'])
        sh.write(13, 7, row['UM'])
        sh.write(13, 8, row['Caducidad'])
        sh.write(13, 9, row['Temperatura'])
        idx += 1

    workbook.save(output)
    output.seek(0)
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Nota_de_Reporte.xls"})

  #  return render_template('uReporte.html', r = r, c = c)


# ------------------------------- ALMACEN -------------------------------------------

@AdminStateApp.route('/sReporteal', methods=["GET", "POST"])
def sReporteal():
    selReporte = mysql.connection.cursor()
    selReporte.execute("SELECT * FROM reporte ORDER BY reporte.Prioridad ASC")
    r = selReporte.fetchall()
    selReporte.close()
    return render_template('dashboardal.html', reporte = r)

@AdminStateApp.route('/verReportes1')
def verReportes1():
    selReporte = mysql.connection.cursor()
    selReporte.execute("SELECT * FROM reporte ORDER BY reporte.Prioridad ASC")
    r = selReporte.fetchall()
    selReporte.close()
    return render_template('reportesal.html', reporte = r)

@AdminStateApp.route('/sformulario3', methods = ["GET", "POST"])
def sformulario3():
    if request.method == 'GET':
        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte ORDER BY reporte.IdReporte DESC LIMIT 1")
        r = selReporte.fetchone()
        selReporte.close()

        IdReporte     = r['IdReporte']
        selContenido = mysql.connection.cursor()
        selContenido.execute("SELECT * FROM `contenido` WHERE `contenido`.`IdReporte` = %s",(IdReporte,))
        c = selContenido.fetchall()
        selContenido.close()
        return render_template("uReporte.html", r=r, c=c)
    else:
        Contenedor    = request.form['Contenedor']
        Articulo      = request.form['Articulo']
        Descripcion   = request.form['Descripcion']
        Ubicacion     = request.form['Ubicacion']
        Lote          = request.form['Lote']
        Qty           = request.form['Qty']
        UM            = request.form['UM']
        Caducidad     = request.form['Caducidad']
        Temperatura   = request.form['Temperatura']

        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte ORDER BY IdReporte DESC LIMIT 1 ")
        idr = selReporte.fetchone()
        selReporte.close()

        IdReporte     = idr['IdReporte']
        insContenido = mysql.connection.cursor()
        insContenido.execute("INSERT INTO contenido (IdReporte, Contenedor, Articulo, Descripcion, Ubicacion, Lote, Qty, UM, Caducidad, Temperatura) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(IdReporte, Contenedor, Articulo, Descripcion, Ubicacion, Lote, Qty, UM, Caducidad, Temperatura))
        mysql.connection.commit()
        insContenido.close()
        return redirect(url_for('verReportes1'))

@AdminStateApp.route('/sformulario5', methods = ["POST"])
def sformulario5():
        IdReporte     = request.form['IdReporte']
        SerClienteF   = request.form['SerClienteF']
        clienteF      = request.form['clienteF']
        TServicioF    = request.form['TServicioF']
        DestinoF      = request.form['DestinoF']
        VentanaF      = request.form['VentanaF']
        FechaF        = request.form['FechaF']
        Estatus       = request.form['Estatus']
        Prioridad     = request.form['Prioridad']
        Transportista = request.form['Transportista']
        Comentarios   = request.form['Comentarios']
        Termino       = request.form['Termino']
        Revision      = request.form['Revision']

        actReporte = mysql.connection.cursor()
        actReporte.execute("UPDATE reporte SET SerClienteF = %s, clienteF = %s, TServicioF = %s, DestinoF = %s, VentanaF = %s, FechaF = %s, Estatus = %s, Prioridad = %s, Transportista = %s, Comentarios = %s, Termino = %s, Revision = %s WHERE `reporte`.`IdReporte` = %s",(SerClienteF, clienteF, TServicioF, DestinoF, VentanaF, FechaF, Estatus, Prioridad, Transportista, Comentarios, Termino ,Revision, IdReporte))
        mysql.connection.commit()
        actReporte.close()
        return redirect(url_for('verReportes1'))

@AdminStateApp.route('/editar1/<IdReporte>', methods=["GET"])
def editar1(IdReporte):
    if request.method == 'GET':
        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte WHERE IdReporte = %s",(IdReporte,))
        r = selReporte.fetchall()
        selReporte.close()

        selContenido = mysql.connection.cursor()
        selContenido.execute("SELECT * FROM contenido WHERE contenido.IdReporte = %s",(IdReporte,))
        c = selContenido.fetchall()
        selContenido.close()
        return render_template('uReporte1.html', r = r, c = c)
    else:
        IdContenido   = request.form['IdContenido']
        Contenedor    = request.form['Contenedor']
        Articulo      = request.form['Articulo']
        Descripcion   = request.form['Descripcion']
        Ubicacion     = request.form['Ubicacion']
        Lote          = request.form['Lote']
        Qty           = request.form['Qty']
        UM            = request.form['UM']
        Caducidad     = request.form['Caducidad']
        Temperatura   = request.form['Temperatura']

        selReporte = mysql.connection.cursor()
        selReporte.execute("SELECT * FROM reporte WHERE IdReporte = %s",(IdReporte,))
        r = selReporte.fetchall()
        selReporte.close()

        IdReporte     = r['IdReporte']
        actContenido = mysql.connection.cursor()
        actContenido.execute("UPDATE contenido SET Contenedor = %s, Articulo = %s, Descripcion = %s, Ubicacion = %s, Lote = %s, Qty = %s, UM = %s, Caducidad = %s, Temperatura = %s WHERE IdContenido = %s",(Contenedor, Articulo, Descripcion, Ubicacion, Lote, Qty, UM, Caducidad, Temperatura, IdContenido))
        mysql.connection.commit()
        actContenido.close()
    return redirect(url_for('verReportes1'))


if __name__ == '__main__':
    #AdminStateApp.secret_key = 'adminstate@123'
    AdminStateApp.run#(port=3002, debug=True)