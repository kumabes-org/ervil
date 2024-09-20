"""This is the main file that we use to start ervil app."""


from flask import Flask, jsonify
from flask_restful import Api, request
from prometheus_client import Counter, make_wsgi_app, Gauge, Histogram
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time
import requests
from datetime import datetime


app = Flask(__name__)
api = Api(app)


# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

login_com_sucesso = Counter('login_com_sucesso', 'Quantidade de login com sucesso!')
login_com_falha = Counter('login_com_falha', 'Quantidade de login com falha!')
tempo_processamento_index = Gauge('tempo_processamento_index', 'Tempo de processamento da página index.')
LATENCY = Histogram('request_latency_seconds', 'Request Latency', labelnames=['path', 'method'])
IN_PROGRESS = Gauge('inprogress_requests', 'Total number of requests in progress', labelnames=['path', 'method'])
REQUESTS = Counter('http_requests_total', 'Total number of requests', labelnames=['path', 'method'])
ERRORS = Counter('http_errors_total', 'Total number of errors', labelnames=['code'])

@app.get('/')
def index():
    """Application Route for index."""    
    start = time.time()
    REQUESTS.labels('/', 'get').inc()
    retorno = f"Hello World at {datetime.now()}"
    end = time.time()
    tempo_processamento_index.set(end - start)
    return retorno

@app.post('/login')
def login():
    """Application Route for login."""
    REQUESTS.labels('login', 'post').inc()
    username = request.json['username']
    password = request.json['password']
    retorno = None
    if username == "admin" and password == "password":
        login_com_sucesso.inc()
        retorno = f"Usuário {username} logado com sucesso", 201
    else:
        login_com_falha.inc()
        retorno = "Ocorreu um problema ao fazer login!", 401
    return retorno


@app.get('/quotes/<currency>')
def quotes(currency:str):
    """Application Route for quotes."""    
    REQUESTS.labels('quotes', 'get').inc()
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.get(f"https://economia.awesomeapi.com.br/json/last/{currency}", headers=headers)
    status_code = r.status_code
    data = r.json()
    key = currency.replace('-','')
    retorno = {
        'compra': data[key]['bid'],
        'venda': data[key]['ask'],
        'variacao': data[key]['varBid'],
        'porcentagem_de_variacao': data[key]['pctChange'],
        'maximo': data[key]['high'],
        'minimo': data[key]['low']
    }
    return jsonify(retorno), status_code

@app.errorhandler(404)
def page_not_found(e):
    """
    Page Not Found
    """
    ERRORS.labels('404').inc()
    return "page not found", 404

def before_request():
    IN_PROGRESS.labels(request.method, request_path).inc()
    request.start_time = time.time()

def after_request(response):
    request_latency = time.time() - request.start_time
    IN_PROGRESS.labels(request.method, request_path).dec()
    LATENCY.labels(request.method, request_path).observe(request_latency)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    app.before_request(before_request)
    app.after_request(after_request)
