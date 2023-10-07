from flask import Flask, render_template,request,redirect
import pymysql
app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def signin():
    if(request.method == 'POST'):
      name=request.form['name']
      password=request.form['pass']
      cpass=request.form['cpass']
      if(password==cpass):
        conn= pymysql.connect(host='localhost',user='root',password='',db='todo')
        with conn.cursor() as c:
         c.execute("INSERT INTO `users` (`name`,`pass`) VALUES ('"+name+"','"+password+"');")
         conn.commit()
         conn.close()
        return redirect(f'/welcome/{name}')
      else:
        return render_template('signin.html') 
    else:
      return render_template('signin.html')  


@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        name=request.form['name']
        password=request.form['pass']

        conn= pymysql.connect(host='localhost',user='root',password='',db='todo')
        with conn.cursor() as c:
         c.execute("SELECT * FROM `users` WHERE `name`='"+name+"' AND `pass`='"+str(password)+"';")
         result = c.fetchall()
        #  print(result)
        conn.close()
        if len(result) == 0:
            return render_template('login.html',error=True)
        else: 
            return redirect(f'/welcome/{name}')
    else:
        return render_template('login.html')
        


@app.route('/welcome/<string:name>',methods=['GET','POST'])
def hello_world(name):
    # print(name)
    if(request.method == 'POST'):
        t=request.form['title']
        d=request.form['dic']
        conn= pymysql.connect(host='localhost',user='root',password='',db='todo')
        with conn.cursor() as c:
         c.execute("INSERT INTO `mytodos` (`title`,`dic`,`name`) VALUES ('"+t+"','"+d+"','"+name+"');")
         conn.commit()
         c.execute("SELECT * FROM `mytodos`  WHERE `name`='"+name+"';")
         result = c.fetchall()
         print(result)
         alltodos=result
        #  print(alltodos)
        conn.close()
        return render_template('index.html',alltodo=alltodos,name=name)
    else:
        conn= pymysql.connect(host='localhost',user='root',password='',db='todo')
        with conn.cursor() as c:
         c.execute("SELECT * FROM `mytodos` WHERE `name`='"+name+"';")
         result = c.fetchall()
         print(result)
         alltodos=result
         return render_template('index.html',alltodo=alltodos,name=name)    


@app.route('/delete/<string:name>/<int:sno>')
def delete(name,sno):
      conn= pymysql.connect(host='localhost',user='root',password='',db='todo')
      with conn.cursor() as c:  
        c.execute("DELETE FROM `mytodos` WHERE `name`='"+name+"' AND `sno`="+str(sno)+";")
        conn.commit()
        # alltodos=todo.query.all()
        return redirect(f'/welcome/{name}')


@app.route('/update/<string:name>/<int:sno>',methods=['GET','POST'])
def update(name,sno):

    if(request.method == 'POST'):
        t=request.form['title']
        d=request.form['dic']
        conn= pymysql.connect(host='localhost',user='root',password='',db='todo')
        with conn.cursor() as c:  
         c.execute("UPDATE `mytodos` SET `title`='"+t+"',`dic`='"+d+"' WHERE name='"+name+"' AND `sno`="+str(sno)+";")
        conn.commit()
        return redirect(f'/welcome/{name}')
    else:
         conn= pymysql.connect(host='localhost',user='root',password='',db='todo')
         with conn.cursor() as c:  
          c.execute("SELECT * FROM `mytodos` WHERE name='"+name+"' AND `sno`="+str(sno)+";")
          res=c.fetchall()
         return render_template('update.html',title=res[0][1],dec=res[0][2],sno=sno,name=name) 
    
if __name__ =="__main__":
    app.run(debug=True)
