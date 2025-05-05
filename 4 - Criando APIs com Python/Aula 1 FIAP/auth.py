from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

app.config['SWAGGER'] = {
    "title":"My Flask API",
    "uiversion":3
}

swagger = Swagger(app)

auth = HTTPBasicAuth()

users = {
    "user1":"password1",
    "user2":"password2"
}


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username]==password:
        return username
    

@app.route('/')
def home():
    return "Hello, Flask. O didi é um babaca. Haha"


@app.route('/items', methods=['GET'])
@auth.login_required
def get_items():
    return jsonify({"message":"Vai Corinthians"})


def get_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip()
        print(title)
        return jsonify({"A porra do titulo": title})
    except Exception as e:
        print(f"Error: {str(e)}"), 500


@app.route('/scrape/title')
@auth.login_required
def scrape_title():
    """
    Function to scrape the title from a URL
    ___
    Secutiry:
     - BasicAuth = []
    
    Parameters:
        - name: url
        - 
    Return:
        - title (str)
    """
    # url = 'https://cidadeverde.com/noticias/433920/corinthians-sofre-com-o-var-mas-vence-o-inter-de-virada-com-hat-trick-de-yuri-alberto'
    url = request.args.get('url')
    if not url:
        return jsonify({"Error":"URL not found"}), 404
    return get_title(url) 


if __name__=='__main__':
    app.run(debug=True)
    
    


