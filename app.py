from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import mysql.connector
import os
import db_config
from ocr_utils import extract_text_from_image

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Image Upload Config
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Helper: Get DB Connection
def get_db_connection():
    return mysql.connector.connect(
        host=db_config.MYSQL_HOST,
        user=db_config.MYSQL_USER,
        password=db_config.MYSQL_PASSWORD,
        database=db_config.MYSQL_DB
    )


# ✅ Route: Add or Update Product
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data['name']
    quantity = data['quantity']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, quantity FROM products WHERE name = %s", (name,))
    result = cur.fetchone()

    if result:
        existing_id, existing_quantity = result
        new_quantity = existing_quantity + quantity
        cur.execute("UPDATE products SET quantity = %s WHERE id = %s", (new_quantity, existing_id))
        message = f"Product '{name}' already exists. Quantity updated to {new_quantity}."
    else:
        cur.execute("INSERT INTO products (name, quantity) VALUES (%s, %s)", (name, quantity))
        message = f"New product '{name}' added with quantity {quantity}."

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": message})


# 🔍 Route: Get All Products
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    products = [{"id": r[0], "name": r[1], "quantity": r[2]} for r in rows]
    return jsonify(products)


# 🖼️ Route: Upload Sell Image (Web: HTML)
@app.route('/upload_sell_image', methods=['POST'])
def upload_sell_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    extracted_text = extract_text_from_image(filepath)
    return render_template('correction.html', ocr_text=extracted_text)


# 📝 Route: Show Correction Form (Web)
@app.route('/ocr_preview', methods=['POST'])
def ocr_preview():
    ocr_text = request.form['ocr_text']
    return render_template('correction.html', ocr_text=ocr_text)


# ✅ Route: Correct Entries (Web)
@app.route('/correct_entry', methods=['POST'])
def correct_entry():
    corrected_text = request.form['corrected_text']

    conn = get_db_connection()
    cur = conn.cursor()
    lines = corrected_text.splitlines()

    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            product_name = parts[0].lower()
            try:
                quantity = int(parts[1])
                cur.execute("SELECT quantity FROM products WHERE name = %s", (product_name,))
                result = cur.fetchone()
                if result:
                    new_quantity = result[0] - quantity
                    new_quantity = max(0, new_quantity)
                    cur.execute("UPDATE products SET quantity = %s WHERE name = %s", (new_quantity, product_name))
            except ValueError:
                continue

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Inventory updated successfully'})


# 📱 Flutter Route: Upload Image and Get OCR Text
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'})

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected image'})

    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    extracted_text = extract_text_from_image(filepath)
    return jsonify({'ocr_text': extracted_text})


# 📱 Flutter Route: Submit Corrected Text
@app.route('/upload_corrected_text', methods=['POST'])
def upload_corrected_text():
    data = request.get_json()
    corrected_text = data.get('corrected_text', '')

    conn = get_db_connection()
    cur = conn.cursor()
    lines = corrected_text.splitlines()

    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            product_name = parts[0].lower()
            try:
                quantity = int(parts[1])
                cur.execute("SELECT quantity FROM products WHERE name = %s", (product_name,))
                result = cur.fetchone()
                if result:
                    new_quantity = result[0] - quantity
                    new_quantity = max(0, new_quantity)
                    cur.execute("UPDATE products SET quantity = %s WHERE name = %s", (new_quantity, product_name))
            except ValueError:
                continue

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Inventory updated from Flutter successfully'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
