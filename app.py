from flask import Flask,render_template,request,url_for,redirect,flash
from app_init import mysql,app

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/shop")
def shop():
    cursor=mysql.connect.cursor()
    cursor.execute("""select product_name,productPrice,productSize from product""")
    db_out = cursor.fetchall()
    items=[]
    for i in db_out:
        item={
            "ProductName": i[0],
            "ProductPrice":i[1],
            "ProductSize":i[2]
        }
        items.append(item)
    cursor.close()
    return render_template('shop.html',items=items)
@app.route("/additems",methods=["GET", "POST"])
def additems():
    if request.method=="POST":
        productName=request.form.get('productName')
        productPrice=request.form.get('productPrice')
        productSize=request.form.get('productSize')
        # adding record to database
        cursor =mysql.connection.cursor()
        cursor.execute('''INSERT INTO product(product_name,productPrice,productSize) VALUES(%s,%s,%s)''',(productName,productPrice,productSize))
        mysql.connection.commit()
        cursor.close()
        flash(f"Item {productName} has been added!",'success')
        return redirect(url_for('shop'))
    return render_template('additems.html')
@app.route('/login',methods=['GET','POST'])
def login():
     if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user exists in the database
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username, password FROM signup WHERE username = %s and password= %s', (email,password))
        user = cursor.fetchone() 
        # If user exists and passwords 
        if user:
            return redirect(url_for('sellerpage'))
        else:
            flash('Incorrect username or password', 'danger')
            return redirect(url_for('login'))
        cursor.close()

     return render_template("login.html")
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        print(username)
        cursor =mysql.connection.cursor()
        cursor.execute(''' INSERT INTO signup(username,password) VALUES(%s,%s)''',(username,password))
        mysql.connection.commit()
        cursor.close()
        return render_template("login.html")
    return render_template("signup.html")
@app.route('/sellerpage')
def sellerpage():
    return render_template("sellerpage.html")
if __name__ == "__main__":
    app.run()