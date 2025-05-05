from flasgger import Swagger
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
    )

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
jwt = JWTManager(app)
swagger = Swagger(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    time_minutes = db.Column(db.Integer, nullable=False)


@app.route('/')
def welcome():
    return("Welcome to this API")
    
@app.route('/register', methods=['GET','POST'])
def register_user():
    """
    Função para conferir se usuário já está registrado; 
    Caso não seja, o usuário é registrado

    Params:
        - nada
    Return:
        - return   
    """
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"Error":"User already registered"}), 400
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User created with success."}), 201

@app.route('/login', methods=['POST'])
def login():
    """
    text text text
    """
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        token = create_access_token(identity=str(user.id))
        return jsonify({'access_token':token}), 200
    return jsonify({"error":"invalid credentials"}), 400    

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"message":f"User ID {current_user_id} accesssed the protected route"}), 200


@app.route('/recipes', methods=['POST'])
@jwt_required()
def create_recipe():
    """
    text text text
    """
    data = request.get_json()
    new_recipe = Recipe(
        title=data['title'],
        ingredients=data['ingredients'],
        time_minutes=data['time_minutes']
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"message":"recipe created successfully"}), 200

@app.route('/recipes', methods=['GET'])
def get_recipe():
    """
    Lista as receitas com filtros adicionais
    ___
    parameters:
        - in: query
          name: ingredient
          type: string
          required: false
          description: filtra por ingredient
        - in:query
          name: max_time
          type: integer,
          required: false
          description: tempo máximo de preparo (minutos)
    response:
        200:
            description: Lista de receitas filtradas
            schema:
              type: array
              item:
                type: object
                properties:
                  id:
                    type: integer
                title:
                    type: string
                time_minutes:
                    type: integer
    """
    ingredient = request.args.get('ingredients')
    max_time = request.args.get('max_time')

    query = Recipe.query
    if ingredient:
        query = query.filter(Recipe.ingredients.ilike(f'%{ingredients}$'))
    if max_time is not None:
        query = query.filter(Recipe.time_minutes <=max_time)
    recipes = query.all()
    return jsonify([
        {
            "id":r.id,
            "title": r.title,
            "ingredient": r.ingredients,
            "time_minutes": r.time_minutes
        }
        for r in recipes
    ])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Banco de dados criado com sucesso! \n')
    app.run(debug=True)







# print('SECRET_KEY: ', app.config['SECRET_KEY'])
 

