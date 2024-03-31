from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vinayak@786@localhost:5432/variantcontrol'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))


class Attribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Variant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    attributes = db.relationship('Attribute', secondary='variant_attributes',
                                 backref=db.backref('variants', lazy='dynamic'))


variant_attributes = db.Table('variant_attributes',
                              db.Column('variant_id', db.Integer, db.ForeignKey('variant.id'), primary_key=True),
                              db.Column('attribute_id', db.Integer, db.ForeignKey('attribute.id'), primary_key=True)
                              )


# Routes
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    product = Product(name=data['name'], description=data.get('description'))
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'}), 201


@app.route('/api/attributes', methods=['POST'])
def add_attribute():
    data = request.json
    attribute = Attribute(name=data['name'])
    db.session.add(attribute)
    db.session.commit()
    return jsonify({'message': 'Attribute added successfully'}), 201


@app.route('/api/products/<int:product_id>/variants', methods=['POST'])
def add_variant(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    variant = Variant(product_id=product.id)
    for attribute_id in data['attributes']:
        attribute = Attribute.query.get_or_404(attribute_id)
        variant.attributes.append(attribute)
    db.session.add(variant)
    db.session.commit()
    return jsonify({'message': 'Variant added successfully'}), 201


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    variants = Variant.query.filter_by(product_id=product.id).all()
    product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'variants': [{'id': variant.id, 'attributes': [attr.id for attr in variant.attributes]} for variant in variants]
    }
    return jsonify(product_data)


if __name__ == '__main__':
    app.run(debug=True)
