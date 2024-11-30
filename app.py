from flask import Flask,render_template,request,url_for,redirect,flash,session
from app_init import mysql,app

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/sellerItems")
def sellerItems():
    if "user_id" in session:
            user_id=session["user_id"]
            cursor=mysql.connect.cursor()
            cursor.execute('select product_name,productPrice,productSize from product where ProductId= %s ',(user_id,))
            db_out = cursor.fetchall()
            items=[]
            for i in db_out:
                item={
                    "ProductName": i[0],
                    "ProductPrice":i[1],
                    "ProductSize":i[2],
                }
                items.append(item)
            cursor.close()
            return render_template('sellerItems.html',items=items)
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
            return redirect(url_for('sellerItems'))
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
    if "user_id" in session:
        user_id=session["user_id"]
        cursor=mysql.connect.cursor()
        cursor.execute('select product_name,product_price,product_quantity,buyer_email,buyer_contact,order_date from orders where id= %s',(user_id,))
        db_out = cursor.fetchall()
        items=[]
        for i in db_out:
            item={
                "ProductName": i[0],
                "ProductPrice":i[1],
                "ProductSize":i[2],
                "BuyerEmail":i[3],
                "BuyerContact": i[4],
                "OrederDate":i[5]
            }
            items.append(item)
        cursor.close()
        return render_template("consumerReq.html",items=items)
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
        # Add a new productId
        productIds[product_id] = [{
            "productName": product_name,
            "productPrice": product_price,
            "productQuantity": 1
        }]
    # Save updated product list back to the session
    session["ProductIds"] = productIds
    return {"message": "Product quantity updated successfully"}
@app.route('/checkout', methods=['POST'])
def checkout():
    # Get buyer details from the form
   if request.method=="POST":
    contact_number = request.form.get('contact_number')
    email = request.form.get('email')
    # Validate inputs
    if not contact_number or not email:
        flash("Contact number and email are required to complete the purchase.", "danger")
        return redirect(url_for('cart'))
    # Get cart items from the session
    productIds = session.get("ProductIds", {})
    if not productIds:
        flash("Your cart is empty. Add items to checkout.", "warning")
        return redirect(url_for('shop'))
    try:
        # Insert the cart data along with buyer details into the database
        cursor = mysql.connection.cursor()
        for product_id, items in productIds.items():
            for item in items:
                cursor.execute(
                    '''
                    INSERT INTO orders (buyer_contact, buyer_email, product_name, product_price, product_quantity)
                    VALUES (%s, %s, %s, %s, %s)
                    ''',
                    (contact_number, email, item["productName"], item["productPrice"], item["productQuantity"])
                )
        mysql.connection.commit()
        cursor.close()

        # Clear the cart session data
        session.pop("ProductIds", None)
        flash("Order placed successfully!", "success")

    except Exception as e:
        flash(f"Error during checkout: {str(e)}", "danger")
    return redirect(url_for('shop'))
@app.route('/logout')
def logout():
    session.pop("user_id", None)
    return render_template("home.html")
if __name__ == "__main__":
    app.run()