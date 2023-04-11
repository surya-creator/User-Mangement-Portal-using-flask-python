from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#mysql connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "mysqleight"
app.config["MYSQL_DB"] = "crud"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)




#Loading Home Page
@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM users"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)

#add new user details
@app.route("/addusers",methods = ["GET","POST"])
def addusers():
    if request.method =="POST":
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        con=mysql.connection.cursor()
        sql = "insert into users (NAME,AGE,CITY)values(%s,%s,%s);"
        con.execute(sql,[name,age,city])
        mysql.connection.commit()
        con.close()
        flash('new user details added')
        return redirect(url_for("home"))
    return render_template("addusers.html")
#update user details
@app.route("/edituser/<string:id>",methods=["GET","POST"])
def edituser(id):
    con = mysql.connection.cursor()
    if request.method =="POST":
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        sql = "update users set NAME =%s, AGE =%s,CITY =%s where ID =%s;"
        con.execute(sql,[name,age,city,id])
        mysql.connection.commit()
        con.close()
        flash('user detail updated')
        return redirect(url_for("home"))
    sql="select * from users where id = %s;"
    con.execute(sql,[id])
    res = con.fetchone()
    return render_template("edituser.html",datas =res)
#DElete user

@app.route("/deleteuser/<string:id>",methods=["GET","POST"])
def deleteuser(id):
    con=mysql.connection.cursor()
    sql = "delete from users where id = %s;"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    flash('user detail detailed')
    return redirect(url_for("home"))



if (__name__ == '__main__'):
    app.secret_key ="abc123"
    app.run(debug=True)



