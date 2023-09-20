from flask import*

from src.dbconnection import *
from werkzeug.utils import secure_filename
import os

from src.dbconnection import *
from src.newcnn1 import predict

app=Flask(__name__)
app.secret_key="aaa"

@app.route('/login',methods=['post'])
def login():
    username = request.form['username']
    password = request.form['password']
    a="SELECT * FROM `login` WHERE `username`=%s AND `password` =%s AND `type`='user'"
    val = (username,password)
    res = selectone(a,val)
    if res is None:
        return jsonify({"task":"invalid"})
    else:
        return jsonify({"task":"valid","type":res['type'],"id":str(res['id'])})

@app.route("/register",methods=['post'])
def register():
    print(request.form)
    fname=request.form['firstname']
    lname=request.form['lastname']
    dob=request.form['dob']
    gen=request.form['gender']
    place=request.form['place']
    post=request.form['post']
    pincode=request.form['pin']
    phn=request.form['contact']
    emailid=request.form['email']
    uname=request.form['username']
    pwd=request.form['password']
    cpwd = request.form['cpsw']
    if pwd==cpwd:
        print("qqqq")
        q="INSERT INTO `login` VALUES (NULL,%s,%s,'user')"
        val=(uname,pwd)
        id=iud(q,val)
        qq="INSERT INTO `user` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val1=(str(id),fname,lname,dob,gen,place,post,pincode,phn,emailid)
        iud(qq,val1)
        return jsonify({'task':'success'})
    else:
        print("eee")
        return jsonify({'task':'invalid'})

@app.route("/view_doc",methods=['post'])
def VIEW_DOCTOR():
     q = "SELECT * FROM `doctor`"
     res = selectall(q)
     return jsonify(res)


@app.route("/VIEW_SCHEDULE_AND_BOOK",methods=['post'])
def VIEW_SCHEDULE_AND_BOOK():
    q="SELECT `schedule`.*,`doctor`.`first_name`,`last_name` FROM `doctor` JOIN `doctor` ON `schedule`.`user_id`=`user`.`login_id`"
    res=selectall(q)
    print(res)
    return jsonify(res)

@app.route('/user_view_doc_schedule', methods=['POST'])
def user_view_doc_schedule():
    did=request.form['did']
    q="SELECT * FROM `schedule` WHERE `doctor_id`=%s"
    res=selectall2(q,did)
    return jsonify(res)

@app.route('/book_doc', methods=['POST'])
def book_doc():
    lid=request.form['lid']
    shid=request.form['shid']
    qq="select * from `booking` where `user_id`=%s and `schedule_doctor_id`=%s and `date`=curdate()"
    val1=(lid,shid)
    re=selectone(qq,val1)
    if re is None:
        q="insert into `booking` values (null,%s,%s,curdate(),'pending')"
        val=(lid,shid)
        iud(q,val)
        return jsonify({"task":"success"})
    else:
        return jsonify({"task":"exist"})

@app.route('/view_schedule_booking', methods=['POST'])
def view_schedule_booking():
    lid=request.form['lid']
    q="select `booking`.*,`schedule`.*,`doctor`.`first_name`,`last_name` from `booking` join `schedule` on `booking`.`schedule_doctor_id`=`schedule`.`id` join `doctor` on `doctor`.`login_id`=`schedule`.`doctor_id` where `booking`.`user_id`=%s"
    res=selectall2(q,lid)
    print(res)
    return jsonify(res)

@app.route('/sendfeedbacks', methods=['POST'])
def sendfeedbacks():
    lid=request.form['lid']
    feed=request.form['feed']
    q="INSERT INTO `feedback` VALUES (NULL,%s,%s,CURDATE())"
    v=(lid,feed)
    iud(q,v)
    return jsonify({"task":"success"})

@app.route('/view_complaint_reply',methods=['post'])
def view_complaint_reply():
    lid=request.form['lid']
    qry="select * from `complaint` where `user_id`=%s"
    res=selectall2(qry,lid)
    return jsonify(res)

@app.route('/send_complaint',methods=['post'])
def send_complaint():
    lid=request.form['lid']
    complaint=request.form['com']
    qry="INSERT INTO `complaint`  VALUES (null,%s,%s,CURDATE(),'pending')"
    val=(lid,complaint)
    res=iud(qry,val)
    return jsonify({'task': 'valid'})

@app.route("/predict_res",methods=['post'])
def predict_res():
    img=request.files['file']
    fn=secure_filename(img.filename)
    img.save(r"C:\Users\User\Desktop\Main Project\leukemia\src\static\1.jpg")
    res = predict('static/1.jpg')
    r="Normal"
    if res==1:
        r="1st stage"
    if res==2:
        r=" 2nd stage"
    if res==3:
        r="3rd stage"
    print(r)
    return jsonify({"task": "success", "r": r, "img": fn})

@app.route('/view_pre', methods=['POST'])
def view_pre():
    bid=request.form['bid']
    print(bid)
    q="select * from `prescription` where `booking_id`=%s"
    res=selectall2(q,bid)
    print(res)
    return jsonify(res)

@app.route('/view_enq_reply', methods=['POST'])
def view_enq_reply():
    lid=request.form['lid']
    q="select `enquiry`.*,`doctor`.`first_name`,`last_name` as `name` from `enquiry` join `doctor` on `doctor`.`login_id`=`enquiry`.`to_id` where `enquiry`.`from_id`=%s"
    res=selectall2(q,lid)
    print(res)
    return jsonify(res)

@app.route('/send_enq', methods=['POST'])
def send_enq():
    did=request.form['did']
    lid=request.form['lid']
    enq=request.form['enq']
    q="INSERT INTO `enquiry` VALUES (NULL,%s,%s,CURDATE(),%s,'pending')"
    v=(lid,did,enq)
    iud(q,v)
    return jsonify({"task":"success"})



app.run(host='0.0.0.0',port=5000)