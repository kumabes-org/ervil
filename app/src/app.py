from flask import Flask, url_for
from markupsafe import escape
from flask_restful import Resource, Api, reqparse, request
from prometheus_client import Gauge, Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


app = Flask(__name__)
api = Api(app)


# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

login_com_sucesso = Counter("login_com_sucesso", "Quantidade de login com sucesso!")
login_com_falha = Counter("login_com_falha", "Quantidade de login com falha!")

@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/login', methods=["POST"])
def login():
    username = request.json['username']
    password = request.json['password']
    if username == "admin" and password == "password":
        login_com_sucesso.inc()
        return f"Usuário {username} logado com sucesso", 201
    else:
        login_com_falha.inc()
        return f"Ocorreu um problema ao fazer login!", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)