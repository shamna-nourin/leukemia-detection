from flask import *
from werkzeug.utils import secure_filename

from src.dbconnection import *
from src.newcnn_predict import predict
app=Flask(__name__)
app.secret_key="12345"

@app.route("/")
def main():
    return render_template("login_index.html")

@app.route("/loginfn",methods=['post'])
def loginfn():
    un=request.form['un']
    pwd=request.form['pwd']
    qry="SELECT * FROM `login` WHERE `username`=%s AND `password` =%s"
    val=(un,pwd)
    res=selectone(qry,val)
    if res is None:
        return '''<script>alert("Invalid username or password");window.location='/'</script>'''
    elif res['type']=='admin':
        return '''<script>alert("ADMIN");window.location='/ADMIN_HOME'</script>'''
    elif res['type']=='doctor':
        session['lid']=res['id']

        return '''<script>alert("DOCTOR");window.location='/DOCTOR_HOME'</script>'''
    else:
        return '''<script>alert("Invalid user");window.location='/'</script>'''

#========================ADMIN=========================

@app.route("/ADMIN_HOME",methods=['post','get'])
def ADMIN_HOME():
    return render_template("admin/admin_index.html")

@app.route("/manage_doctor")
def manage_doctor():
    q="SELECT * FROM `doctor`"
    res=selectall(q)
    return render_template("admin/manage doctor.html",data=res)

@app.route("/REGISTRATION_DR")
def REGISTRATION_DR():
    return render_template("admin/REGISTRATION DR.html")

@app.route("/REGISTRATION_DR_post",methods=['post'])
def REGISTRATION_DR_post():
    fname=request.form['textfield']
    lname=request.form['textfield2']
    gen=request.form['gen']
    place=request.form['textfield3']
    post=request.form['textfield4']
    pincode=request.form['textfield5']
    qual=request.form['textfield6']
    specl=request.form['select']
    phn=request.form['textfield8']
    emailid=request.form['textfield9']
    uname=request.form['textfield10']
    pwd=request.form['textfield11']
    cpwd = request.form['textfield12']
    if pwd==cpwd:
        q="INSERT INTO `login` VALUES (NULL,%s,%s,'doctor')"
        val=(uname,pwd)
        id=iud(q,val)

        qq="INSERT INTO `doctor` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val1=(str(id),fname,lname,gen,place,post,pincode,qual,specl,phn,emailid)
        iud(qq,val1)
        return '''<script>alert("Added successfully");window.location='/manage_doctor#about'</script>'''
    else:
        return '''<script>alert("Password and confirm password does not match");window.location='/REGISTRATION_DR#about'</script>'''

@app.route("/delete_doctor")
def delete_doctor():
    lid=request.args.get('id')
    q1="DELETE FROM `doctor` WHERE login_id=%s"
    iud(q1,lid)
    q2="DELETE FROM `login` WHERE id=%s"
    iud(q2,lid)
    return '''<script>alert("deleted successfully");window.location='/manage_doctor#about'</script>'''

@app.route("/edit_doctor")
def edit_doctor():
    lid = request.args.get('id')
    session['did']=lid
    q="SELECT * FROM `doctor` WHERE login_id =%s"
    res=selectone(q,lid)
    print(res)
    return render_template("admin/edit_doctor.html",data=res)

@app.route("/edit_doc_post",methods=['post'])
def edit_doc_post():
    fname=request.form['textfield']
    lname=request.form['textfield2']
    gen=request.form['gen']
    place=request.form['textfield3']
    post=request.form['textfield4']
    pincode=request.form['textfield5']
    qual=request.form['textfield6']
    specl=request.form['select']
    phn=request.form['textfield8']
    emailid=request.form['textfield9']
    qq="UPDATE `doctor` SET `first_name`=%s,`last_name`=%s,`gender`=%s,`place`=%s,`post`=%s,`pin`=%s,`qualification`=%s,`specialisation`=%s,`phone_number`=%s,`email_id`=%s WHERE login_id=%s"
    val1=(fname,lname,gen,place,post,pincode,qual,specl,phn,emailid,session['did'])
    iud(qq,val1)
    return '''<script>alert("Updated successfully");window.location='/manage_doctor#about'</script>'''


@app.route("/MANAGE_SCHEDULE")
def MANAGE_SCHEDULE():
    id=request.args.get('id')
    session['dlid']=id
    q="SELECT * FROM `schedule` WHERE `doctor_id`=%s"
    res=selectall2(q,id)
    print(res)
    return render_template("admin/MANAGE SCHEDULE.html",data=res)

@app.route("/ADD_NEW_SCHEDULE_post",methods=['post'])
def ADD_NEW_SCHEDULEE_post():
    date=request.form['textfield']
    ft=request.form['textfield2']
    tt=request.form['textfield3']
    q="INSERT INTO `schedule` VALUES (NULL,%s,%s,%s,%s)"
    val=(str(session['dlid']),date,ft,tt)
    iud(q,val)
    return '''<script>alert("Added successfully");window.location='/manage_doctor#about'</script>'''

@app.route("/ADD_NEW_SCHEDULE",methods=['post'])
def ADD_NEW_SCHEDULEE():
    return render_template("admin/ADD NEW SCHEDULE.html")

@app.route("/delete_schedule")
def delete_schedule():
    lid=request.args.get('id')
    q1="DELETE FROM `schedule` WHERE id=%s"
    iud(q1,lid)
    return '''<script>alert("deleted successfully");window.location='/MANAGE_SCHEDULE#about'</script>'''


@app.route("/VIEW_USER")
def VIEW_USER():
    q="SELECT * FROM `user`"
    res=selectall(q)
    return render_template("admin/VIEW USER.html",data=res)

@app.route("/VIEW_COMPLAINT_AND_SEND_REPLY")
def VIEW_COMPLAINT_AND_SEND_REPLY():
    q="SELECT `complaint`.*,`user`.`first_name`,`last_name` FROM `complaint` JOIN `user` ON `complaint`.`user_id`=`user`.`login_id`"
    res=selectall(q)
    print(res)
    return render_template("admin/VIEW COMPL&SND RPLY.html",data=res)

@app.route("/REPLY")
def REPLY():
    id=request.args.get('id')
    session['cid']=id
    return render_template("admin/REPLY.html")

@app.route('/reply_post',methods=['post'])
def reply_post():
    rply=request.form['textfield']
    q="UPDATE `complaint` SET `reply`=%s WHERE `id`=%s"
    val=(rply,session['cid'])
    iud(q,val)
    return '''<script>alert("Sended successfully");window.location='/VIEW_COMPLAINT_AND_SEND_REPLY#about'</script>'''

@app.route("/feedbackview")
def feedbackview():
    q="SELECT `feedback`.*,`user`.`first_name`,`last_name` FROM `feedback` JOIN `user` ON `feedback`.`user_id`=`user`.`login_id`"
    res=selectall(q)
    return render_template("admin/FEEDBACKVIEW.html",data=res)





#==========================DOCTOR================================================

@app.route("/DOCTOR_HOME",methods=['post','get'])
def DOCTOR_HOME():
    return render_template("doctor/doctor_index.html")

@app.route("/DOC_VIEW_USER")
def DOC_VIEW_USER():
    q="SELECT * FROM `user`"
    res = selectall(q)
    return render_template("doctor/VIEW USER.html",data=res)

@app.route("/LOAD_IMAGE1")
def LOAD_IMAGE1():
    return render_template("LOAD IMAGE.html")

@app.route("/LOAD_IMAGE")
def LOAD_IMAGE():
    return render_template("doctor/LOAD IMAGE.html")

@app.route("/predict",methods=['post'])
def predictf():
    img=request.files['file']
    fn=secure_filename(img.filename)
    img.save("static/predict/"+fn)
    res=predict("static/predict/"+fn)[0]
    r="Normal"
    if res==1:
        r="1st stage"
    if res==2:
        r=" 2nd stage"
    if res==3:
        r="3rd stage"
    return render_template("result.html",r=r,img=fn)

@app.route("/VIEW_BOOKING_AND_UPDATE_STATUS")
def VIEW_BOOKING_AND_UPDATE_STATUS():
    q="SELECT `booking`.*,`user`.*,`schedule`.* FROM `booking` JOIN `schedule` ON `schedule`.`id`=`booking`.`schedule_doctor_id` JOIN `user` ON `user`.`login_id`=`booking`.`user_id` WHERE `schedule`.`doctor_id`=%s AND `booking`.`status`!='Rejected'"
    res=selectall2(q,session['lid'])
    print(session['lid'],res)
    return render_template("doctor/VIEW BOOKING AND UPDATE STATUS.html",data=res)

@app.route('/accept_booking')
def accept_booking():
    id = request.args.get('id')
    q="UPDATE `booking` SET `status`='Accepted' WHERE `id`=%s"
    res=iud(q,id)
    return '''<script>alert("Acccepted successfully");window.location='/VIEW_BOOKING_AND_UPDATE_STATUS#about'</script>'''

@app.route('/reject_booking')
def reject_booking():
    id = request.args.get('id')
    q="UPDATE `booking` SET `status`='Rejected' WHERE `id`=%s"
    res=iud(q,id)
    return '''<script>alert("Rejected successfully");window.location='/VIEW_BOOKING_AND_UPDATE_STATUS#about'</script>'''


@app.route("/PROVIDE_PRESCRIPTION")
def PROVIDE_PRESCRIPTION():
    id=request.args.get('id')
    session['Pid'] = id
    return render_template("doctor/PROVIDE PRESCRIPTION.html")

@app.route("/VIEW_ENQUIRY")
def VIEW_ENQUIRY():
    q="  SELECT `user`.`first_name`,`last_name`, `enquiry`.* FROM `enquiry` JOIN `user` ON `enquiry`.`from_id`=`user`.`login_id` WHERE `enquiry`.`to_id`=%s"
    res=selectall2(q,session['lid'])
    return render_template("doctor/VIEW ENQUIRY.html",data=res)

@app.route("/ENQUIRY_REPLY")
def ENQUIRY_REPLY():
    id = request.args.get('id')
    session['Eid'] = id
    return render_template("doctor/E_REPLY.html")

@app.route("/upload_prescription",methods=['post'])
def upload_prescription():
    f=request.files['file']
    ff=secure_filename(f.filename).split(".")[-1]
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+"."+ff
    f.save("static/prescription/"+fn)
    qry="INSERT INTO `prescription` VALUES(NULL,%s,%s,CURDATE())"
    val=(fn,session['Pid'])
    iud(qry,val)

    return redirect("/VIEW_BOOKING_AND_UPDATE_STATUS")


@app.route('/ENQUIRY_reply_post',methods=['post'])
def ENQUIRY_reply_post():
    rply=request.form['textfield']
    q="UPDATE `enquiry` SET `reply`=%s WHERE `id`=%s"
    val=(rply,session['Eid'])
    iud(q,val)
    return '''<script>alert("Sended successfully");window.location='/VIEW_ENQUIRY#about'</script>'''

app.run(debug=True)