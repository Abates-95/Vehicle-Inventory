from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api= Blueprint("api", __name__, url_prefix='/api')


@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_car_token):
    classification = request.json['classification']
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    doors = request.json['doors']
    color = request.json['color']
    car_token = current_car_token.token

    print(f'You are here things are working: {current_car_token.token}')

    car = Car(classification, make, model, year, doors, color, car_token = car_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_car(current_car_token):
    a_car = current_car_token.token
    cars = Car.query.filter_by(car_token = a_car).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_car_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_car_token, id):
    # Query database for a book with specific ID
    car = Car.query.get(id)
    # Update book data with retrieved data from request object
    fields_to_update = request.json.keys()

    for field in fields_to_update:
        if hasattr(car, field):
            setattr(car, field, request.json[field])
            car.car_token = current_car_token.token

    # Commit changes to database
    db.session.commit()
    
    # Serialize updated book object and return as JSON response
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_car_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)