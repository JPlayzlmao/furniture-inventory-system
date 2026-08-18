from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/products")
def products():

    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    connection.close()

    return render_template("products.html", products=products)

@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form["name"]
    selling_price = float(request.form["selling_price"])
    description = request.form["description"]

    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products (name,selling_price,description) VALUES(?, ?, ?)
    """,(name, selling_price, description))

    connection.commit()
    connection.close()

    return redirect(url_for("products"))

@app.route("/edit_product/<int:id>")
def edit_product(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM products WHERE id = ?""",(id,))

    product = cursor.fetchone()
    connection.close()

    return render_template("edit_product.html",product=product)

@app.route("/update_product/<int:id>", methods=["POST"])
def update_product(id):
    name = request.form["name"]
    selling_price = float(request.form["selling_price"])
    description = request.form["description"]

    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE products
        SET name = ?, selling_price = ?, description = ?
        WHERE id = ?
    """,(name, selling_price, description, id))

    connection.commit()
    connection.close()

    return redirect(url_for("products"))

@app.route("/delete_product/<int:id>")
def delete_product(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM products WHERE id = ?""",(id,))

    product = cursor.fetchone()

    connection.close()

    return render_template("delete_product.html",product=product)

@app.route("/confirm_delete_product/<int:id>", methods=["POST"])
def confirm_delete_product(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""DELETE FROM products WHERE id = ?""", (id,))

    connection.commit()
    connection.close()

    return redirect(url_for("products"))

@app.route("/materials")
def materials():
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM materials""")

    materials = cursor.fetchall()

    connection.close

    return render_template("materials.html",materials=materials)

@app.route("/edit_material/<int:id>")
def edit_material(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM materials WHERE id = ?""", (id,))

    material = cursor.fetchone()
    connection.close()

    return render_template("edit_material.html",material=material)

@app.route("/delete_material/<int:id>")
def delete_material(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM materials WHERE id = ?""",(id,))

    material = cursor.fetchone()
    connection.close()

    return render_template("delete_material.html",material=material)

@app.route("/add_material", methods=["POST"])
def add_material():

    name = request.form["name"]
    unit = request.form["unit"]
    quantity = float(request.form["quantity"])
    price = float(request.form["price"])

    # Connect to the database
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    # Insert the new material
    cursor.execute("""
        INSERT INTO materials (name, unit, quantity, price) VALUES (?, ?, ?, ?)
    """, (name, unit, quantity, price))

    connection.commit()
    connection.close()

    return redirect(url_for("materials"))

@app.route("/update_material/<int:id>",methods=["POST"])
def update_material(id):

    name = request.form["name"]
    unit = request.form["unit"]
    quantity = float(request.form["quantity"])
    price = float(request.form["price"])

    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE materials
        SET name = ?, unit = ?, quantity = ?, price = ?
        WHERE id = ?
    """,(name,unit,quantity,price,id))

    connection.commit()
    connection.close()

    return redirect(url_for("materials"))

@app.route("/confirm_delete_material/<int:id>",methods=["POST"])
def confirm_delete_material(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""DELETE FROM materials WHERE id = ?""",(id,))

    connection.commit()
    connection.close()

    return redirect(url_for("materials"))

@app.route("/bill_of_materials")
def bill_of_materials():
    selected_product = request.args.get("product_id", type=int)
    print("Selected product:", selected_product)

    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM products""")
    products = cursor.fetchall()

    cursor.execute("""SELECT * FROM materials""")
    materials = cursor.fetchall()

    cursor.execute("""
        SELECT bill_of_materials.id, products.name, materials.name, bill_of_materials.amount_needed
        FROM bill_of_materials
        JOIN products
            ON bill_of_materials.product_id = products.id
        JOIN materials
            ON bill_of_materials.material_id = materials.id;
    """)
    bom = cursor.fetchall()

    connection.close()

    return render_template("bill_of_materials.html",products=products,materials=materials,bom=bom,selected_product=selected_product)

@app.route("/add_bom",methods=["POST"])
def add_bom():
    product_id = request.form["product_id"]
    material_id = request.form["material_id"]
    amount_needed = float(request.form["amount_needed"])

    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO bill_of_materials (product_id, material_id, amount_needed) VALUES (?, ?, ?)
    """, (product_id, material_id, amount_needed))

    connection.commit()
    connection.close()

    return redirect(url_for("bill_of_materials",product_id=product_id))

@app.route("/edit_bom/<int:id>")
def edit_bom(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM bill_of_materials WHERE id = ?""",(id,))
    bom = cursor.fetchone()

    cursor.execute("""SELECT * FROM products""")
    products = cursor.fetchall()

    cursor.execute("""SELECT * FROM materials""")
    materials = cursor.fetchall()

    connection.close()

    return render_template("edit_bom.html",bom=bom,products=products,materials=materials)

@app.route("/update_bom/<int:id>", methods=["POST"])
def update_bom(id):
    product = request.form["product_id"]
    material = request.form["material_id"]
    amount_needed = float(request.form["amount_needed"])

    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE bill_of_materials
        SET product_id = ?, material_id = ?, amount_needed = ?
        WHERE id = ?
    """,(product,material,amount_needed,id))

    connection.commit()
    connection.close()

    return redirect(url_for("bill_of_materials"))

@app.route("/delete_bom/<int:id>")
def delete_bom(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            bill_of_materials.id,
            products.name,
            materials.name,
            materials.unit,
            bill_of_materials.amount_needed
        FROM bill_of_materials
        JOIN products
            ON bill_of_materials.product_id = products.id
        JOIN materials
            ON bill_of_materials.material_id = materials.id
        WHERE bill_of_materials.id = ?
    """,(id,))
    bom = cursor.fetchone()

    connection.close()

    return render_template("delete_bom.html",bom=bom)

@app.route("/confirm_delete_bom/<int:id>", methods=["POST"])
def confirm_delete_bom(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""DELETE FROM bill_of_materials WHERE id = ?""",(id,))

    connection.commit()
    connection.close()

    return redirect(url_for("bill_of_materials"))

@app.route("/orders")
def orders():
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM orders""")
    orders = cursor.fetchall()

    connection.close()

    return render_template("orders.html",orders=orders)

@app.route("/create_order", methods=["POST"])
def create_order():
    code = request.form["receipt_code"]
    customer = request.form["customer_name"]
    date = request.form["order_date"]
    total = 0

    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO orders (receipt_code, customer_name, order_date, total) VALUES (?, ?, ?, ?)
    """, (code,customer,date,total))

    connection.commit()
    connection.close()

    return redirect(url_for("orders"))

@app.route("/manage_order/<int:id>")
def manage_order(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM orders WHERE id = ?""",(id,))
    order = cursor.fetchone()

    cursor.execute("""SELECT * FROM products""")
    products = cursor.fetchall()

    cursor.execute("""
        SELECT order_items.id, products.name ,order_items.quantity, order_items.selling_price
        FROM order_items
        JOIN products
            ON order_items.product_id = products.id
        WHERE order_items.order_id = ?
    """,(id,))
    order_items = cursor.fetchall()

    connection.close()

    return render_template("manage_order.html",order=order,products=products,order_items=order_items)

@app.route("/delete_order/<int:id>")
def delete_order(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM orders WHERE id = ?""",(id,))
    order = cursor.fetchone()

    connection.close()

    return render_template("delete_order.html", order=order)

@app.route("/confirm_delete_order/<int:id>", methods=["POST"])
def confirm_delete_order(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""DELETE FROM order_items WHERE order_id = ?""",(id,))
    cursor.execute("""DELETE FROM orders WHERE id = ?""",(id,))

    connection.commit()
    connection.close()

    return redirect(url_for("orders"))

@app.route("/add_order_item/<int:id>",methods=["POST"])
def add_order_item(id):
    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])

    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    
    cursor.execute("""SELECT selling_price FROM products WHERE id = ?""",(product_id,))
    product = cursor.fetchone()
    selling_price = product[0]

    cursor.execute("""
        INSERT INTO order_items (order_id,product_id,quantity,selling_price) VALUES (?,?,?,?)
    """,(id,product_id,quantity,selling_price))

    connection.commit()

    update_order_total(id)

    connection.close()

    return redirect(url_for("manage_order", id=id))

@app.route("/delete_order_item/<int:id>")
def delete_order_item(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
            SELECT order_items.id, order_items.order_id, products.name ,order_items.quantity, order_items.selling_price
            FROM order_items
            JOIN products
                ON order_items.product_id = products.id
            WHERE order_items.id = ?
        """,(id,))
    item = cursor.fetchone()

    connection.close()

    return render_template("delete_order_item.html",item=item)

@app.route("/confirm_delete_order_item/<int:id>", methods=["POST"])
def confirm_delete_order_item(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT order_id FROM order_items WHERE id = ?""",(id,))
    result = cursor.fetchone()
    order_id = result[0]

    cursor.execute("""DELETE FROM order_items WHERE id = ?""",(id,))

    connection.commit()

    update_order_total(order_id)

    connection.close()

    return redirect(url_for("manage_order",id=order_id))

@app.route("/edit_order_item/<int:id>")
def edit_order_item(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_items.id, products.name ,order_items.quantity, order_items.selling_price
        FROM order_items
        JOIN products
            ON order_items.product_id = products.id
        WHERE order_items.id = ?
    """,(id,))
    item = cursor.fetchone()

    connection.close()
    
    return render_template("edit_order_item.html",item=item)

@app.route("/update_order_item/<int:id>", methods=["POST"])
def update_order_item(id):
    quantity = int(request.form["quantity"])

    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id FROM order_items WHERE id = ?
    """,(id,))
    result = cursor.fetchone()
    order_id = result[0]

    cursor.execute("""
        UPDATE order_items SET quantity = ? WHERE id = ?    
    """,(quantity,id))

    connection.commit()

    update_order_total(order_id)

    connection.close()

    return redirect(url_for("manage_order"))

def update_order_total(id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(quantity * selling_price) FROM order_items WHERE order_id = ?
    """,(id,))
    total = cursor.fetchone()[0] or 0

    cursor.execute("""
        UPDATE orders SET total = ? WHERE id = ?
    """,(total,id))

    connection.commit()
    connection.close()

if __name__ == "__main__":
    app.run(debug=True)