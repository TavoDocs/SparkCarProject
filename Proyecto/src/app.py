import cv2

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash


from config import config

# Models:
from models.ModelUser import ModelUser
from models.ModelVisitante import ModelVisitante

# Entities:
from models.entities.User import User

# read the images
img1 = cv2.imread("static/assets/libre.png")
img2 = cv2.imread("static/assets/ocupado.png")
img3 = cv2.imread("static/assets/especial.png")
img4 = cv2.imread("static/assets/vacio.png")
img5 = cv2.imread("static/assets/wall.png")
img6 = cv2.imread("static/assets/sitio.png")

def concat_vh(list_2d):
	
	# return final image
	return cv2.vconcat([cv2.hconcat(list_h)
						for list_h in list_2d])
# image resizing
img1_s = cv2.resize(img1, dsize = (0,0),
					fx = 0.5, fy = 0.5)
img2_s = cv2.resize(img2, dsize = (0,0),
					fx = 0.5, fy = 0.5)
img3_s = cv2.resize(img3, dsize = (0,0),
					fx = 0.5, fy = 0.5)
img4_s = cv2.resize(img4, dsize = (0,0),
					fx = 0.5, fy = 0.5)
img5_s = cv2.resize(img5, dsize = (0,0),
					fx = 0.5, fy = 0.5)
img6_s = cv2.resize(img6, dsize = (0,0),
					fx = 0.5, fy = 0.5)
Status_Est = []
Status_img_Est = [img1_s,img2_s, img3_s, img6_s]

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['email'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                cursor = db.connection.cursor()
                sql = """SELECT role FROM user 
                    WHERE email = '{}'""".format(user.email)
                cursor.execute(sql)
                row = cursor.fetchone()
                print(row)
                if row[0] == 'admin':
                    return redirect(url_for('mainadmin'))
                else:
                    return redirect(url_for('homeuser'))
            else:
                flash("Invalid password...")
                return render_template('auth/loginutec.html')
        else:
            flash("User not found...")
            return render_template('auth/loginutec.html')
    else:
        return render_template('auth/loginutec.html')

@app.route('/login1', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        user = User(0, request.form['email'], '')
        logged_user = ModelVisitante.login(db, user)
        if logged_user != None:
            login_user(logged_user)  
            return redirect(url_for('homevisitante'))
        else:
            flash("User not found...")
            return render_template('auth/login_visitante.html')
    else:
        return render_template('auth/login_visitante.html')

@app.route('/homevisitante')
def homevisitante():
    return render_template('homevisitante.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/mainadmin')
def mainadmin():
    cur = db.connection.cursor()
    cur.execute('select * from user')
    data = cur.fetchall()
    return render_template('inicio.html',usuarios=data)

@app.route('/add_user',methods=['POST'])
def add_user():
    if request.method == 'POST':
        cod = request.form['codigo']
        nom = request.form['nombre']
        nom = generate_password_hash(nom)
        email = request.form['correo']
        perf = request.form['perfil']
        print('INSERT', id, cod, nom, email, perf)
        cur = db.connection.cursor()
        cur.execute('insert into user(email, password, fullname, role) values(%s,%s,%s,%s)', (cod, nom, email, perf))
        db.connection.commit()
        flash('Usuario Insertado correctamente')
        return redirect(url_for('mainadmin'))

@app.route('/edit_user/<id>')
def edit_user(id):
    cur = db.connection.cursor()
    cur.execute('select * from user where id = %s',{id})
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html', usuario=data[0])

@app.route('/update_user/<id>',methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        cod = request.form['email']
        nom = request.form['password']
        nom = generate_password_hash(nom)
        email = request.form['fullname']
        perf = request.form['rol']
        print('UPDATE_USER', id, cod, nom, email, perf)
        cur = db.connection.cursor()
        cur.execute("""
            update user
            set email = %s,
                password = %s,
                fullname = %s,
                role = %s
            where id = %s
        """,(cod, nom, email, perf, id) )
        db.connection.commit()
        # flash('Usuario actualizado correctamente')
        return redirect(url_for('mainadmin'))

@app.route('/delete_user/<string:id>')
def delete_user(id):
    cur = db.connection.cursor()
    cur.execute('delete from user where id = {0}'.format(id))
    db.connection.commit()
    flash('Usuario Eliminado correctamente')
    return redirect(url_for('mainadmin'))

@app.route('/adminevento')
def adminevento():
    cur = db.connection.cursor()
    cur.execute('select * from eventos')
    data = cur.fetchall()
    return render_template('adminevento.html',eventos=data) 

@app.route('/add_event',methods=['POST'])
def add_event():
    if request.method == 'POST':
        titu = request.form['titulo']
        date = request.form['fecha']
        space = request.form['espacios']
        desc = request.form['descripcion']
        print('INSERT', id, titu, date, space, desc)
        cur = db.connection.cursor()
        cur.execute('insert into eventos(titulo, fecha, espacios, descripcion) values(%s,%s,%s,%s)', (titu, date, space, desc))
        db.connection.commit()
        flash('Evento Insertado correctamente')
        for i in range (int(space)):
            cur = db.connection.cursor()
            cur.execute('UPDATE status SET estado = 2 WHERE NOT estado = 2 LIMIT 1')
            db.connection.commit()

        return redirect(url_for('adminevento'))

@app.route('/editevento/<id>')
def edit_event(id):
    cur = db.connection.cursor()
    cur.execute('select * from eventos where id = %s',{id})
    data = cur.fetchall()
    print(data[0])
    return render_template('editevento.html', evento=data[0])

@app.route('/updateevento/<id>',methods=['POST'])
def update_event(id):
    if request.method == 'POST':
        titu = request.form['titulo']
        date = request.form['fecha']
        space = request.form['espacios']
        desc = request.form['descripcion']
        print('UPDATE_EVENT', id, titu, date, space, desc)
        cur = db.connection.cursor()
        cur.execute("""
            update eventos
            set titulo = %s,
                fecha = %s,
                espacios = %s,
                descripcion = %s
            where id = %s
        """,(titu, date, space, desc, id) )
        db.connection.commit()
        # flash('Evento actualizado correctamente')
        return redirect(url_for('adminevento')) 

@app.route('/deleteevento/<string:id>')
def deleteevento(id):
    cur = db.connection.cursor()
    cur.execute('UPDATE status SET estado = 0 where estado = 2')
    db.connection.commit()
    cur = db.connection.cursor()
    cur.execute('delete from eventos where id = {0}'.format(id))
    db.connection.commit()
    flash('Evento Eliminado correctamente')
    return redirect(url_for('adminevento'))          

@app.route('/homeuser')
@login_required
def homeuser():
    cur = db.connection.cursor()
    cur.execute('select estado from status')

    result = cur.fetchall()
    Status_Est = []
    for row in result:
        for field in row:
            Status_Est.append(field)
    
    espacios_libres= 0
    for i in range (len(Status_Est)):
        if Status_Est[i] == 0:
            espacios_libres = 1 + espacios_libres

    if espacios_libres == 0:
        flash("Estacionamiento Lleno, lo sentimos")
        
    return render_template('homeuser.html')

@app.route('/utecespacios1')
@login_required
def utecespacios1():
    cur = db.connection.cursor()
    cur.execute('select estado from status')

    result = cur.fetchall()
    Status_Est = []
    for row in result:
        for field in row:
            Status_Est.append(field)
    
    espacios_libres= 0
    for i in range (len(Status_Est)):
        if Status_Est[i] == 0:
            espacios_libres = 1 + espacios_libres

    img_tile = concat_vh([[Status_img_Est[Status_Est[0]], Status_img_Est[Status_Est[1]], Status_img_Est[Status_Est[2]], Status_img_Est[Status_Est[3]], Status_img_Est[Status_Est[4]], Status_img_Est[Status_Est[5]], Status_img_Est[Status_Est[6]], Status_img_Est[Status_Est[7]], Status_img_Est[Status_Est[8]], Status_img_Est[Status_Est[9]], Status_img_Est[Status_Est[10]], img5_s, img5_s, img5_s, img5_s, img5_s],
					  [img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s],
					  [img4_s, Status_img_Est[Status_Est[11]], Status_img_Est[Status_Est[12]], Status_img_Est[Status_Est[13]], Status_img_Est[Status_Est[14]], Status_img_Est[Status_Est[15]], Status_img_Est[Status_Est[16]], Status_img_Est[Status_Est[17]], Status_img_Est[Status_Est[18]], Status_img_Est[Status_Est[19]], Status_img_Est[Status_Est[20]], Status_img_Est[Status_Est[21]], Status_img_Est[Status_Est[22]], Status_img_Est[Status_Est[23]], Status_img_Est[Status_Est[24]], img4_s],
					  [img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s],
					  [img4_s, Status_img_Est[Status_Est[25]], Status_img_Est[Status_Est[26]], Status_img_Est[Status_Est[27]], Status_img_Est[Status_Est[28]], Status_img_Est[Status_Est[29]], Status_img_Est[Status_Est[30]], Status_img_Est[Status_Est[31]], Status_img_Est[Status_Est[32]], Status_img_Est[Status_Est[33]], img5_s, img5_s, img5_s, img5_s, img5_s, img5_s]])
    # Guarda como una imagen png el mapa 
    cv2.imwrite("static/assets/E2.png", img6_s)
    cv2.imwrite("static/assets/E1.jpg", img_tile)
    return render_template('utecespacios1.html', free = espacios_libres )

@app.route('/utecespacios2')
@login_required
def utecespacios2():
    return render_template('utecespacios2.html')

@app.route('/utecEstRap')
@login_required
def utecEstRap():
    cur = db.connection.cursor()
    cur.execute('select estado from status')

    result = cur.fetchall()
    Status_Est = []
    for row in result:
        for field in row:
            Status_Est.append(field)

    for i in range(len(Status_Est)):
        if Status_Est[i] == 0:
           Status_Est[i] = 3
           break



    img_tile = concat_vh([[Status_img_Est[Status_Est[0]], Status_img_Est[Status_Est[1]], Status_img_Est[Status_Est[2]], Status_img_Est[Status_Est[3]], Status_img_Est[Status_Est[4]], Status_img_Est[Status_Est[5]], Status_img_Est[Status_Est[6]], Status_img_Est[Status_Est[7]], Status_img_Est[Status_Est[8]], Status_img_Est[Status_Est[9]], Status_img_Est[Status_Est[10]], img5_s, img5_s, img5_s, img5_s, img5_s],
					  [img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s],
					  [img4_s, Status_img_Est[Status_Est[11]], Status_img_Est[Status_Est[12]], Status_img_Est[Status_Est[13]], Status_img_Est[Status_Est[14]], Status_img_Est[Status_Est[15]], Status_img_Est[Status_Est[16]], Status_img_Est[Status_Est[17]], Status_img_Est[Status_Est[18]], Status_img_Est[Status_Est[19]], Status_img_Est[Status_Est[20]], Status_img_Est[Status_Est[21]], Status_img_Est[Status_Est[22]], Status_img_Est[Status_Est[23]], Status_img_Est[Status_Est[24]], img4_s],
					  [img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s],
					  [img4_s, Status_img_Est[Status_Est[25]], Status_img_Est[Status_Est[26]], Status_img_Est[Status_Est[27]], Status_img_Est[Status_Est[28]], Status_img_Est[Status_Est[29]], Status_img_Est[Status_Est[30]], Status_img_Est[Status_Est[31]], Status_img_Est[Status_Est[32]], Status_img_Est[Status_Est[33]], img5_s, img5_s, img5_s, img5_s, img5_s, img5_s]])
    # Guarda como una imagen png el mapa 
    cv2.imwrite("static/assets/E1.jpg", img_tile)
    cur.execute('select nombre from status where estado = 0 LIMIT 1')
    result = cur.fetchall()
    return render_template('utecEstRap.html',pipipi=result[0])

@app.route('/funcion2')
@login_required
def funcion2():
    cur = db.connection.cursor()
    cur.execute('select * from eventos')
    data = cur.fetchall()
    return render_template('tablaevento.html',eventos=data)




@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config['TESTING'] = False
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
