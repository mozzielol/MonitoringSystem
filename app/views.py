from flask import render_template, flash, redirect, session, url_for, request, g,Response,send_from_directory
from app import app
#from app import db,lm
from .form import LoginForm,SettingForm,PswChangeForm,EmailChangeForm,LcdForm,FaceForm
#from .models import Sensor_Data
#from .models import User
#from flask_login import login_user, logout_user, current_user, login_required
from LiveStreaming import gen_normal,gen_detector,gen_recognizer,gen_face,gen_model_recognizer
#from LiveStreaming import gen_service
import secret
import os
import sys
import time
from edison_control import led,blink,setlcd,sensordata,alarm
#from send_email import sender
from face_rec_model.ExtendedPredictableModel import ExtendedPredictableModel


_MSG_LOGINFAILED = 'Fail to login,please check the username and password'
_MSG_LOGINSUCCESS = 'Login Success'
_MSG_LOGOUT = 'Logout Success'
_MSG_DELETE = 'Success Delete '
_MSG_DELETE_FAIL = 'Failt to Delete '
_MSG_PSW_VERIFY = 'Update Success'
_MSG_PSW_VERIFY_FAILED = 'Verify Failed, Please enter again'
_MSG_USER_DUPLICATE = 'User Already Exist'
_MSG_WARNING = "please see the live stream, the value of light is   "

#lm.login_view = 'login'


@app.route('/')
@app.route('/index')
#@login_required
def index():
    return render_template('index.html',
                           #user=g.user,
                          led_state='On',
                          alarm_state='On')
'''
@app.route('/login',methods=['GET','POST'])
def login():
    global _USERNAME
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.objects(username=username,password=password).first()
        if user:
            login_user(user)
            flash(_MSG_LOGINSUCCESS)
            return redirect(url_for('index'))
        else:
            flash(_MSG_LOGINFAILED)
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@lm.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

@app.before_request
def before_request():
    g.user = current_user


@app.route('/logout')
#@login_required
def logout():
    logout_user()
    flash(_MSG_LOGOUT)
    return redirect(url_for('login'))
'''
@app.route('/setting')
#@login_required
def setting():
    return render_template('setting.html')

@app.route('/addperson',methods=['GET','POST'])
#@login_required
def addperson():
    faceform = FaceForm()
    if faceform.validate_on_submit():
        name = faceform.name.data
        return redirect(url_for('collect_face',name=name))
    return render_template('addperson.html',form_addperson=faceform,name='None')

@app.route('/collect_face/<name>')
#@login_required
def collect_face(name):
    return render_template('collect_face.html',name=name)
    

@app.route('/collect_streaming/<name>')
#@login_required
def collect_streaming(name):
    return Response(gen_face(name),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

'''
@app.route('/manage',methods=['GET','POST'])
#@login_required
def manage():
    form_setting = SettingForm()
    if form_setting.validate_on_submit():
        username_setting = form_setting.username_setting.data
        password_setting = form_setting.password_setting.data
        password_setting_verify = form_setting.password_setting_verify.data
        email_addr_setting = form_setting.email_addr_setting.data
        user = User(username=username_setting,password=password_setting,email_addr=email_addr_setting)
        if password_setting != password_setting_verify:
            flash(_MSG_PSW_VERIFY_FAILED)
        else:
            flash(_MSG_PSW_VERIFY)
            user.save()    
            
    return render_template('manage.html',
                          username=User.objects(),
                          form_setting = form_setting)

@app.route('/delete/<username>')
#@login_required
def user_delete(username):
    user = User.objects(username=username).first()
    if not user:
        flash(_MSG_DELETE_FAIL)
        return redirect(url_for('manage'))
    else:
        user.delete()
        flash(_MSG_DELETE)
        return redirect(url_for('manage'))
    
    
@app.route('/psw_change',methods=['GET','POST'])
#@login_required
def psw_change():
    form_psw = PswChangeForm()
    if form_psw.validate_on_submit():
        password_new = form_psw.password_new.data
        password_new_verify = form_psw.password_new_verify.data
        user = User.objects(username=str(g.user)).first()
        if password_new != password_new_verify:
            flash(_MSG_PSW_VERIFY_FAILED)
        else:
            flash(_MSG_PSW_VERIFY)
            user.update(password=password_new)
    return render_template('ChangePsw.html',
                          user=g.user,
                           username=g.user,
                          form_psw=form_psw)

@app.route('/email_change',methods=['GET','POST'])
#@login_required
def email_change():
    form_email = EmailChangeForm()
    if form_email.validate_on_submit():
        email_new = form_email.email_addr_new.data
        email_new_verify = form_email.email_addr_new_verify.data
        user = User.objects(username=str(g.user)).first()
        if email_new != email_new_verify:
            flash(_MSG_PSW_VERIFY_FAILED)
        else:
            flash(_MSG_PSW_VERIFY)
            user.update(email_addr=email_new)
    return render_template('ChangeEmail.html',
                          user=g.user,
                           username=g.user,
                          form_email=form_email)
'''

@app.route('/livepage')
#@login_required
def livepage():
    return render_template('livestreaming.html')

@app.route('/stream_normal')
#@login_required
def stream_normal():
    return render_template('normal_streaming.html')

@app.route('/normal_streaming')
#@login_required
def normal_streaming():
    return Response(gen_normal(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream_detector')
#@login_required
def stream_detector():
    return render_template('detector_streaming.html')

@app.route('/detector_streaming')
#@login_required
def detector_streaming():
    return Response(gen_detector(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream_recognizer')
#@login_required
def stream_recognizer():
    return render_template('recognizer_streaming.html')

@app.route('/recognizer_streaming')
#@login_required
def recognizer_streaming():
    return Response(gen_recognizer(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream_model_recognizer')
#@login_required
def stream_model_recognizer():
    return render_template('model_recognizer_streaming.html')

@app.route('/model_recognizer_streaming')
#@login_required
def model_recognizer_streaming():
    return Response(gen_model_recognizer(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

'''
@app.route('/service_recognition')
#@login_required
def service_recognition():
    return render_template('service_recognition.html')

@app.route('/recognition_service')
#@login_required
def recognition_service():
    return Response(gen_service(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
'''

@app.route("/img/<dir>/<filename>")
#@login_required
def send_img(dir,filename):
    root_path = '../app/img_detected/'
    path = os.path.join(root_path,dir)
    return send_from_directory(path,filename)


@app.route('/invador_img')
#@login_required
def invador_img():
    image_invadors = os.listdir('./app/img_detected/invador')
    return render_template('Invador.html',dir='invador',invadors=image_invadors)

@app.route('/motion_img')
#@login_required
def motion_img():
    image_motions = os.listdir('./app/img_detected/motion_image')
    return render_template('Motion.html',dir='motion_image',motions=image_motions)

@app.route('/delete_invador/<filename>')
#@login_required
def delete_invador(filename):
    root_path = './app/img_detected/invador'
    delete_path = os.path.join(root_path,filename)
    os.remove(delete_path)
    return redirect(url_for('invador_img'))

@app.route('/delete_motion/<filename>')
#@login_required
def delete_motion(filename):
    root_path = './app/img_detected/motion_image'
    delete_path = os.path.join(root_path,filename)
    os.remove(delete_path)
    return redirect(url_for('motion_img'))


@app.route('/info')
#@login_required
def info_page():
    return render_template('info.html')


# -- control edison
@app.route('/lcd_control')
#@login_required
def lcd_control():
    return redirect(url_for('lcd'))

@app.route('/lcd',methods=['GET','POST'])
#@login_required
def lcd():
    form_lcd = LcdForm()
    if form_lcd.validate_on_submit():
        msg = form_lcd.lcdmsg.data
        setlcd.lcdDisplay(str(msg),(0,255,0)).start()
    return render_template('lcd.html',
                          form_lcd = form_lcd)



@app.route('/led_control')
#@login_required
def led_control():
    led.switch_led()
    return render_template('index.html',
                           
                          led_state=get_led_state(),
                          alarm_state=get_alarm_state())

@app.route('/alarm_control')
#@login_required
def alarm_control():
    alarm.switch_alarm()
    return render_template('index.html',
                           
                          led_state=get_led_state(),
                          alarm_state=get_alarm_state())

def get_led_state():
    return led.get_led_state()
def get_alarm_state():
    return alarm.get_alarm_state()


@app.route('/sensor_data')
#@login_required
def sensor_data():
    light_data = sensordata.light_sensor()
    temperature_and_humidity_sensor = sensordata.TemperatureAndHumiditySensor(0)
    temperature_and_humidity_sensor.measure_temperature_and_humidity()
    temp_celsius = temperature_and_humidity_sensor.temperature_celsius
    temp_fah = temperature_and_humidity_sensor.temperature_fahrenheit
    humidity = temperature_and_humidity_sensor.humidity
        
    
    if sensordata.light_sensor()>40 and secret.emailstate_light==True:
        msg = _MSG_WARNING+str(sensordata.light_sensor())
        #sender('None',msg).start()
        secret.emailstate_light=False

    return render_template('sensor_data.html',
                           
                           light_data = light_data,
                           temp_celsius = temp_celsius,
                           temp_fah = temp_fah,
                           humidity = humidity)

#----------------RNN-------- Test Code. Currently it can only upload images.
'''
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/root/Interim/caption'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            caption='test'
            from tmp.rnn.edison import predict
            import cv2
            img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            caption = predict(img)
            return render_template('rnn.html',filename=filename,caption=caption)
    return render_template('caption.html')
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
'''
