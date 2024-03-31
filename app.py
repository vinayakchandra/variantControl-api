from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
client = MongoClient(r'mongodb://localhost:27017/')
db = client['demo']  # demo database

# MongoDB collections
products = db['products']
attributes = db['attributes']  # size, color, material
variants = db['variants']


# CRUD operations
# Add new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    product_id = products.insert_one(data).inserted_id
    return jsonify({'message': 'Product added successfully', 'product_id': str(product_id)}), 201


# Add new attribute
@app.route('/attributes', methods=['POST'])
def add_attribute():
    data = request.json
    attribute_id = attributes.insert_one(data).inserted_id
    return jsonify({'message': 'Attribute added successfully', 'attribute_id': str(attribute_id)}), 201


# Add new variant
@app.route('/variants', methods=['POST'])
def add_variant():
    data = request.json
    variant_id = products.insert_one(data).inserted_id
    return jsonify({'message': 'Variant added successfully', 'variant_id': str(variant_id)}), 201


# Update product details
@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    products.update_one({'_id': ObjectId(product_id)}, {'$set': data})
    return jsonify({'message': 'Product updated successfully'}), 200


# Retrieve all products with variants
@app.route('/products', methods=['GET'])
def get_products():
    product_list = []
    for product in products.find():
        product_data = {
            'name': product['name'],
            'description': product['description'],
            'variants': product['variants'],
        }
        # variant
        for variant_id in product['variants']:
            variant = variants.find_one({'_id': variant_id})
            if variant:
                product_data['variants'].append({
                    'size': variant['size'],
                    'color': variant['color'],
                    'material': variant['material']
                })
        product_list.append(product_data)
    return jsonify({'products': product_list}), 200


if __name__ == '__main__':
    app.run(debug=True)
