from flask import Flask
from flask import render_template,session,request,redirect
from flask_mysqldb import MySQL
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

mysql=MySQL(app)

api_sendgrid="sendgrid api "

app.config['MYSQL_HOST']='remotemysql.com'
app.config['MYSQL_USER']='9JtF7WHjWK'
app.config['MYSQL_PASSWORD']='nNAXVhfFtY'
app.config['MYSQL_DB']='9JtF7WHjWK'
app.secret_key='a'
@app.route('/')
def startapp():
    return redirect('/login')
@app.route('/adminagentdetails')
def admin_agent_details():
    is_admin_agent = False
    is_admin_user_detals = True
    is_admin_details = False
    auname = session.get('adminusername')
    apassword = session.get('adminpassword')

    if auname == app.config['MYSQL_USER']:
        if apassword == app.config['MYSQL_PASSWORD']:
            cursor = mysql.connection.cursor()
            cursor.execute("show tables;")
            record = cursor.fetchall()
            cursor.execute("select * from Users;")
            table1=cursor.fetchall()
            cursor.execute("select * from agentdetails;")
            table2=cursor.fetchall()
            cursor.execute("select * from agentnumbers;")
            table3=cursor.fetchall()
            cursor.execute("select * from userquestions;")
            table4=cursor.fetchall()
            cursor.execute("select * from agentquestions;")
            table5=cursor.fetchall()
            cursor.execute("select * from questions;")
            table6=cursor.fetchall()
            print("Hello")
            return render_template('adminpannel.html', adminusername=auname, record=record, admin_agent=is_admin_agent,
                                   admin_user_detals=is_admin_user_detals,
                                   admin_details=is_admin_details,table4=table4,table3=table3,table2=table2,table1=table1,table5=table5,table6=table6)
    else:
        return render_template('admin.html')
@app.route('/adminagentreg')
def adminagentregister():
    auname = session.get('adminusername')
    apassword = session.get('adminpassword')

    if auname == app.config['MYSQL_USER']:
        if apassword == app.config['MYSQL_PASSWORD']:
            is_admin_agent = True
            is_admin_user_detals = False
            is_admin_details = False
            return render_template('adminpannel.html',admin_agent=is_admin_agent,admin_user_detals=is_admin_user_detals,admin_details=is_admin_details)
    else:
        return render_template('admin.html')

@app.route('/adminagentdatain',methods=['POST'])
def adminagentdetailsintake():
    is_admin_agent=True
    is_admin_user_detals=False
    is_admin_details=False
    if request.method=='POST':
        otp_str="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        agent_acces_token=""
        for _ in range(6):
            agent_acces_token+=otp_str[random.randint(1,35)]
        print(agent_acces_token)
        agentemailreq=str(request.form['agentaccgen'])
        curser = mysql.connection.cursor()
        curser.execute("select * from agentnumbers where email="+" "+"\'"+agentemailreq+"\'"+";")
        records=curser.fetchall()
        if(len(records) != 0):
            return render_template('adminpannel.html', admin_agent=is_admin_agent,
                                   admin_user_detals=is_admin_user_detals, admin_details=is_admin_details,emailerr="Email Already Exists")
        try:
            message = Mail(
                from_email='appmanaging84@gmail.com',
                to_emails=agentemailreq,
                subject='Acess Token For Regestration',
                html_content='<h1>Access Token For Regestration</h1><br/><br/>' + agent_acces_token
            )
            sg = SendGridAPIClient(api_sendgrid)
            response = sg.send(message)
            print(response.status_code)
            print("INSERT INTO `agentnumbers` (`aggentid`, `email`, `activation`, `accstatus`) VALUES (NULL, "+"\'"+agentemailreq+"\'"+','+"\'"+agent_acces_token+"\'"+','+"\'"+"0"+"\'"+");")
            curser.execute("INSERT INTO `agentnumbers` (`aggentid`, `email`, `activation`, `accstatus`) VALUES (NULL, "+"\'"+agentemailreq+"\'"+','+"\'"+agent_acces_token+"\'"+','+"\'"+"0"+"\'"+");")
            mysql.connection.commit()
            return render_template('adminpannel.html', admin_agent=is_admin_agent,admin_user_detals=is_admin_user_detals,
                                    admin_details=is_admin_details,upmsg="Created Sucessfully")

        except Exception as e :
            return render_template('adminpannel.html',  admin_agent=is_admin_agent,admin_user_detals=is_admin_user_detals,
                                    admin_details=is_admin_details, email_err="Please Check Email",mail_exception=e)

@app.route('/agentregestration')
def agent_registeration():
    return render_template('agentlogin.html')
@app.route('/agentregestrationdata',methods=['POST'])
def agent_register_data():
    if request.method== "POST":
        acctocken = str(request.form['acctoken'])
        regname = str(request.form['regname'])
        regemail= str(request.form['regemail'])
        regusername= str(request.form['regusername'])
        regpassword= str(request.form['regpassword'])
        regconformpassword= str(request.form['regconformpassword'])
        regphonenumber= str(request.form['regphonenumber'])
        curser=mysql.connection.cursor()
        curser.execute("select * from agentdetails where ausername="+"\'"+regusername+"\'"+";")
        userrecord=curser.fetchall()
        if(len(userrecord)!=0):
            return render_template('agentlogin.html',usererr="Username Already Exists")
        print(regemail)
        print("select * from agentnumbers where email="+"\'"+regemail+"\'"+";")
        curser.execute("select * from agentnumbers where email="+"\'"+regemail+"\'"+";")
        records = curser.fetchall()
        print("he")
        print(records)
        if(len(records)==0):
            return render_template('agentlogin.html',err_email_msg="Please Use Email Id Having Access Id")
        else:
            if(records[0][3]==1):
                return render_template('agentlogin.html',errmsg="Account Created Already With Given Accces Id")
            else:
                if regpassword!= regconformpassword:
                    return render_template('agentlogin.html', passmsg='Plesse Re enter Password Correctly')
                if acctocken==records[0][2]:
                    print("INSERT INTO `agentquestions` (`aqid`, `auser`, `nquestions`) VALUES (NULL,"+"\'"+regusername+"\'"+",'0');")
                    curser.execute("INSERT INTO `agentquestions` (`aqid`, `auser`, `nquestions`) VALUES (NULL,"+"\'"+regusername+"\'"+",'0');")
                    curser.execute("INSERT INTO `agentdetails` (`agid`, `ausername`, `apassword`, `aemail`, `aname`, `amobilenum`) VALUES (NULL, "+"\'"+regusername+"\'"+','+"\'"+regpassword+"\'"+','+"\'"+regemail+"\'"+','+"\'"+regname+"\'"+','+"\'"+regphonenumber+"\'"+");")
                    curser.execute("UPDATE `agentnumbers` SET `accstatus` = "+"\'"+"1"+"\'" + " WHERE `agentnumbers`.`email` = "+"\'"+regemail+"\';")
                    mysql.connection.commit()
                    return render_template('agentlogin.html',sucessmsg='Sucessfully Regestered ')
                else:
                    return render_template('agentlogin.html',accmsg="Enter Valid Access Token")
@app.route('/admin')
def admin():
    is_admin_agent = False
    is_admin_user_detals = False
    is_admin_agent_details = False
    is_admin_details = True
    auname = session.get('adminusername')
    apassword = session.get('adminpassword')

    if auname == app.config['MYSQL_USER']:
        if apassword == app.config['MYSQL_PASSWORD']:
            session['adminusername'] = auname
            session['adminpassword'] = apassword
            cursor = mysql.connection.cursor()
            cursor.execute("show tables;")
            record = cursor.fetchall()
            print("Hello")
            return render_template('adminpannel.html', adminusername=auname, record=record, admin_agent=is_admin_agent,
                                   admin_user_detals=is_admin_user_detals, admin_agent_details=is_admin_agent_details,
                                   admin_details=is_admin_details)
    else:
        return render_template('admin.html')
@app.route('/adminlogout')
def adminlogout():
    session.pop('adminusername')
    session.pop('adminpassword')
    return redirect('/admin')
@app.route('/admindata',methods=['POST'])
def admin_data():
    is_admin_agent = False
    is_admin_user_detals = False
    is_admin_agent_details = False
    is_admin_details = True
    if request.method=='POST':
        auname=str(request.form['auname'])
        apassword=str(request.form['apassword'])
        if auname==app.config['MYSQL_USER']:
            if apassword==app.config['MYSQL_PASSWORD']:
                session['adminusername'] = auname
                session['adminpassword'] = apassword
                cursor=mysql.connection.cursor()
                cursor.execute("show tables;")
                record=cursor.fetchall()
                print("Hello")
                return render_template('adminpannel.html',adminusername=auname,record=record,admin_agent=is_admin_agent,admin_user_detals=is_admin_user_detals,admin_agent_details=is_admin_agent_details,admin_details=is_admin_details)
            else:
                return render_template('admin.html',msg='Login Failed')
        else:
            return render_template('admin.html',msg='Login Failed')
@app.route('/login')
def login():
    uname = session.get('sessusername')
    passwo = session.get('sesspassword')
    print(uname)
    print(passwo)
    typeofuser = session.get('usertype')
    if typeofuser == 'rcustomer':
        try:
            curser = mysql.connection.cursor()
            curser.execute(
                "select * from Users where username=" + "\'" + uname + "\'" + "and passw=" + "\'" + passwo + "\';")
            records = curser.fetchall()
            print(records)
            print("hell cursor")
            if len(records) == 0:
                print("Hii")
                return render_template('log.html')
            else:
                is_question = False
                is_profile = True
                is_review = False
                return render_template('customerpannel.html', msg="Hello Customer", record=records,is_profile=is_profile,is_question=is_question,is_review=is_review)
        except:
            print("Exception")
            return render_template('log.html')
    if typeofuser == 'ragent':
        try:
            curser = mysql.connection.cursor()
            curser.execute(
                "select * from agentdetails where ausername=" + "\'" + uname + "\'" + "and apassword=" + "\'" + passwo + "\';")
            records = curser.fetchall()
            print(records)
            print("hell cursor")
            if len(records) == 0:
                print("Hii")
                return render_template('log.html')
            else:
                is_answer = False
                is_agent_profile = True
                return render_template('agentpannel.html', msg="Hello Customer", record=records,is_answer=is_answer,is_agent_profile=is_agent_profile)
        except:
            return render_template('log.html')
    else:
        return render_template('log.html')


@app.route('/logout')
def logout():
    try:
        session.pop('sessusername')
        session.pop('sesspassword')
        session.pop('usertype')
        return redirect('/login')
    except:
        return render_template('log.html')
@app.route('/logindata',methods=['POST'])
def logindata():
    if request.method=='POST':
        rcusorag=request.form['agentcustomerradio']
        if rcusorag=='rcustomer':
            uname=str(request.form['uname'])
            passwo=str(request.form['passwo'])
            try:
                curser=mysql.connection.cursor()
                curser.execute("select * from Users where username="+"\'"+uname+"\'"+"and passw="+"\'"+passwo+"\';")
                records=curser.fetchall()
                print("hell cursor")
                if len(records) == 0:
                    return render_template('log.html',msg="Login Failed")
                else:
                    print(records[0][1])
                    session['sessusername']=records[0][2]
                    session['sesspassword']=records[0][3]
                    session['usertype']=rcusorag
                    is_question = False
                    is_profile = True
                    is_review = False
                    return render_template('customerpannel.html',msg="Hello Customer",record=records,is_profile=is_profile,is_question=is_question,is_review=is_review)
                print(records)
            except:
                return render_template('log.html')
        else:
            uname = str(request.form['uname'])
            passwo = str(request.form['passwo'])
            try:
                curser = mysql.connection.cursor()
                curser.execute(
                    "select * from agentdetails where ausername=" + "\'" + uname + "\'" + "and apassword=" + "\'" + passwo + "\';")
                records = curser.fetchall()
                print("hell cursor")
                if len(records) == 0:
                    return render_template('log.html', msg="Login Failed")
                else:
                    print(records[0][2])
                    print(records[0][1])
                    session['sessusername'] = records[0][1]
                    session['sesspassword'] = records[0][2]
                    session['usertype'] = rcusorag
                    is_answer = False
                    is_agent_profile = True
                    print("True")
                    return render_template('agentpannel.html', msg="Hello Customer", record=records,
                                           is_answer=is_answer, is_agent_profile=is_agent_profile)
            except:
                return render_template('log.html')
@app.route('/answerquestions')
def answerquestions():
    agentusername = session.get("sessusername")
    passwo = session.get('sesspassword')
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "select * from agentdetails where ausername=" + "\'" + agentusername + "\'" + "and apassword=" + "\'" + passwo + "\';")
    except:
        return render_template('log.html')
    records = cursor.fetchall()
    print(records)
    print("hell cursor")
    if len(records) == 0:
        print("Hii")
        return render_template('log.html')
    else:
        is_answer = True
        is_agent_profile = False
        cursor.execute("select * from agentdetails where ausername=" + "\'" + agentusername + "\';")
        agent_records = cursor.fetchall()
        aemail = agent_records[0][3]
        print(aemail)
        cursor.execute("SELECT * FROM `questions` WHERE status='0' AND aemail=" + "\'" + aemail + "\';")
        question_records = cursor.fetchall()
        return render_template('agentpannel.html', msg="Hello Customer", question_records=question_records,
                               is_answer=is_answer, is_agent_profile=is_agent_profile, record=agent_records)
@app.route('/update',methods=['POST'])
def updateanswers():
    if request.method=='POST':
        is_answer = True
        is_agent_profile = False
        uname=request.form['userquestion']
        answer=request.form['answer']
        qid=request.form['qid']
        print(uname)
        print(answer)
        cursor = mysql.connection.cursor()
        agentusername = session.get("sessusername")
        cursor = mysql.connection.cursor()
        cursor.execute("select * from agentdetails where ausername=" + "\'" + agentusername + "\';")
        agent_records = cursor.fetchall()
        aemail = agent_records[0][3]
        print(aemail)
        print(answer)
        cursor.execute("UPDATE questions SET answer="+"\'"+answer+"\'"+" WHERE aemail="+"\'"+aemail+"\'"+" AND qid="+"\'"+qid+"\';")
        cursor.execute(
            "UPDATE questions SET status=" + "\'" +'1'+ "\'" + " WHERE aemail=" + "\'" + aemail + "\'" + " AND qid=" + "\'" + qid + "\';")
        mysql.connection.commit()
        cursor.execute("SELECT * FROM `questions` WHERE status='0' AND aemail=" + "\'" + aemail + "\';")
        question_records = cursor.fetchall()
        cursor.execute("select * from Users where username="+"\'"+uname+"\';")
        user_records=cursor.fetchall()
        print(user_records[0][4])
        user_message = Mail(
            from_email='appmanaging84@gmail.com',
            to_emails=user_records[0][4],
            subject='Customer Care Registery',
            html_content='<h1>Our Agent Have Given Answer To Our Question Please Check In Managment Portal</h1><br/><br/>'
        )
        sg = SendGridAPIClient(api_sendgrid)
        response = sg.send(user_message)
        print(response.status_code)
        return render_template('agentpannel.html', msg="Hello Customer", question_records=question_records,
                               is_answer=is_answer, is_agent_profile=is_agent_profile, record=agent_records)
@app.route('/askquestion')
def askquestion():
    uname = session.get('sessusername')
    passwo = session.get('sesspassword')
    curser = mysql.connection.cursor()
    try:
        curser.execute(
            "select * from Users where username=" + "\'" + uname + "\'" + "and passw=" + "\'" + passwo + "\';")
    except:
        return render_template('log.html')
    records = curser.fetchall()
    print(records)
    print("hell cursor")
    if len(records) == 0:
        print("Hii")
        return render_template('log.html')
    else:
        is_question = True
        is_profile = False
        is_review = False
        return render_template('customerpannel.html', is_profile=is_profile, is_question=is_question,
                               is_review=is_review)
@app.route('/recieve',methods=['POST'])
def recievequestion():
    if request.method=='POST':
        question = request.form['question']
        uname=session.get('sessusername')
        print(uname)
        print(question)
        cursor = mysql.connection.cursor()
        cursor.execute("select * from agentquestions;")
        record = cursor.fetchall()
        question_count=record[0][2]
        print(question_count)
        cursor.execute("select min(nquestions) from agentquestions;")
        min_count = cursor.fetchall()
        print(min_count[0][0])
        cursor.execute("select * from agentquestions where nquestions="+"\'"+str(min_count[0][0])+"\';")
        qrecords = cursor.fetchall()
        cursor.execute("select * from userquestions where quser="+"\'"+uname+"\';")
        user_record=cursor.fetchall()
        agents_list = []
        for agent_username in qrecords:
            agents_list.append(agent_username[1])
        print(agents_list)
        print(qrecords)
        selected_agent = random.choice(agents_list)
        print(selected_agent)
        cursor.execute("SELECT * FROM agentquestions,agentdetails WHERE agentquestions.auser=agentdetails.ausername AND auser="+"\'"+selected_agent+"\';")
        final_agent = cursor.fetchall()
        print(final_agent[0][6])
        print(user_record[0][2])
        print(min_count[0][0])
        print(final_agent)
        print(str(final_agent[0][6]) + "Agent Mail")
        agent_message = Mail(
            from_email='appmanaging84@gmail.com',
            to_emails=final_agent[0][6],
            subject='Customer Tocken',
            html_content='<h4>You Have Revieved A Question From a Customer </h4><br/><br/>' + question
        )
        agentsg = SendGridAPIClient(api_sendgrid)
        response = agentsg.send(agent_message)
        print(response.status_code)
        cursor.execute(
            "SELECT * FROM Users,userquestions WHERE Users.username=userquestions.quser AND username=" + "\'" + uname + "\';")
        customer_record = cursor.fetchall()
        print(customer_record[0][4])
        customer_message = Mail(
            from_email='appmanaging84@gmail.com',
            to_emails=customer_record[0][4],
            subject='Customer Care',
            html_content='<h4>Thanks For Using Customer Care Service You will get answer Soon From Our Agent </h4><br/><br/>'
        )
        costomersg = SendGridAPIClient(api_sendgrid)
        response = costomersg.send(agent_message)
        print(response.status_code)
        cursor.execute("INSERT INTO `questions` (`qid`, `cuname`, `question`, `answer`, `status`, `aemail`) VALUES (NULL,"+"\'"+uname+"\'"+","+"\'"+question+"\'"+", '', '0',"+"\'"+(final_agent[0][6])+"\'"+");")
        cursor.execute("UPDATE `userquestions` SET `nquestions` = "+"\'"+str((user_record[0][2]+1))+"\'" + " WHERE quser = "+"\'"+uname+"\';")
        cursor.execute("UPDATE `agentquestions` SET `nquestions` = "+"\'"+str((min_count[0][0]+1))+"\'" + " WHERE auser = "+"\'"+(final_agent[0][4])+"\';")
        mysql.connection.commit()
        is_question = True
        is_profile = False
        is_review = False
        return render_template('customerpannel.html', is_profile=is_profile, is_question=is_question,
                               is_review=is_review,sucessmsg="Your Question Is Sent To Our Agent You will get answer Soon")
@app.route('/reviewquestion')
def review_questions():
    uname = session.get('sessusername')
    passwo = session.get('sesspassword')
    print(uname)
    print(passwo)
    typeofuser = session.get('usertype')
    if typeofuser == 'rcustomer':
        curser = mysql.connection.cursor()
        try:
            curser.execute(
                "select * from Users where username=" + "\'" + uname + "\'" + "and passw=" + "\'" + passwo + "\';")
        except:
            return render_template('log.html')
        records = curser.fetchall()
        print(records)
        print("hell cursor")
        if len(records) == 0:
            print("Hii")
            return render_template('log.html')
        else:
            is_question = False
            is_profile = False
            is_review = True
            cursor = mysql.connection.cursor()
            cursor.execute("select * from questions where cuname=" + "\'" + uname + "\';")
            record_questions = cursor.fetchall()
            return render_template('customerpannel.html', is_profile=is_profile, is_question=is_question,
                                       is_review=is_review, record_questions=record_questions)
@app.route('/create')
def create():
    return render_template('login.html')
@app.route('/createdata',methods=['POST'])
def create_data():
    if request.method=='POST':
        try:
            fname=request.form['name']
            username=str(request.form['username'])
            password=str(request.form['password'])
            cpassword=str(request.form['conformpassword'])
            email=str(request.form['email'])
            mnumber=str(request.form['phonenumber'])
            curs=mysql.connection.cursor()
            curs.execute("select * from Users;")
            recorddetails=curs.fetchall()
            print(recorddetails)
            if password !=cpassword:
                return render_template('login.html',msg='Plesse Re enter Password Correctlr')
            for erecord in recorddetails:
                print(erecord)
                if str(erecord[2])==username:
                    return render_template('login.html',msg='User Already Exists')
                if str(erecord[4])==email:
                    return render_template('login.html',msg='Email Already Exists')
            curs.execute("INSERT INTO `userquestions` (`uqid`, `quser`, `nquestions`) VALUES (NULL,"+"\'"+username+"\'"+",'0');")
            print("INSERT INTO `Users` (`userid`,`name`, `username`, `passw`, `email`, `mobilenum`) VALUES (NULL,"+"\'"+fname+"\'"+','+"\'"+username+"\'"+','+"\'"+password+"\'"+','+"\'"+email+"\'"+','+"\'"+mnumber+"\'"+");")
            curs.execute("INSERT INTO `Users` (`userid`,`name`, `username`, `passw`, `email`, `mobilenum`) VALUES (NULL,"+"\'"+fname+"\'"+','+"\'"+username+"\'"+','+"\'"+password+"\'"+','+"\'"+email+"\'"+','+"\'"+mnumber+"\'"+");")
            mysql.connection.commit()
            print("commit")
            return render_template('login.html',sucess_msg="Sucessfully Created ")
        except:
            return render_template('login.html')
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')
