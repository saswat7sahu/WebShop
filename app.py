from flask import Flask,render_template,request,url_for,redirect,flash,session
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
    cursor.execute("""select product_name,productPrice,productSize,ProductId from product""")
    db_out = cursor.fetchall()
    items=[]
    for i in db_out:
        item={
            "ProductName": i[0],
            "ProductPrice":i[1],
            "ProductSize":i[2],
            "ProductId":i[3]
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
        if "user_id" in session:
            user_id=session["user_id"]
        # adding record to database
            cursor =mysql.connection.cursor()
            cursor.execute('''INSERT INTO product(product_name,productPrice,productSize,ProductId) VALUES(%s,%s,%s,%s)''',(productName,productPrice,productSize,user_id))
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
        cursor.execute('SELECT id,username, password FROM signup WHERE username = %s and password= %s', (email,password))
        user = cursor.fetchone() 
        # If user exists and passwords 
        if user:
            #session data which user logged in
            user_id=user[0]
            print(user_id)
            session["user_id"]=user_id
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
@app.route('/consumerReq')
def consumerReq():
    return render_template("consumerReq.html")
@app.route('/cart')
def cart():
    productIds = session.get("ProductIds", {})
    return render_template("cart.html", productIds=productIds)
@app.route("/update_quantity", methods=["POST"])
def update_quantity():
    data = request.get_json()  # Receive JSON data from the client
    product_name = data.get('productName')
    product_price = data.get('productPrice')
    product_id = data.get('productId')

    # Get existing product data from the session
    productIds = session.get("ProductIds", {})

    # Check if the productId is already in the session
    if product_id in productIds:
        # Update quantity if the product exists
        for item in productIds[product_id]:
            if item["productName"] == product_name:
                item["productQuantity"] += 1
                break
        else:
            # Add as a new item for the productId if not already in the list
            productIds[product_id].append({
                "productName": product_name,
                "productPrice": product_price,
                "productQuantity": 1
            })
    else:
        # Add a new productId entry if it doesn't exist
        productIds[product_id] = [{
            "productName": product_name,
            "productPrice": product_price,
            "productQuantity": 1
        }]

    # Save updated product list back to the session
    session["ProductIds"] = productIds

    print(session["ProductIds"])  # Debugging output

    return {"message": "Product quantity updated successfully"}
if __name__ == "__main__":
    app.run()