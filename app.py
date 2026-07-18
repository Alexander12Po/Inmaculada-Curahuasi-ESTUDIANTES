from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Configuración de tu API externa y Token Privado
API_BASE_URL = "https://api-codart.cgrt.org/api/v1/consultas/fd"
TOKEN = "jmdCRmBLZ13ITSmUGCWcBnDcTuOddttU7d0UbL8S7HJNelk8loSpnVkUyFJO"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/consulta/dni/<dni>', methods=['GET'])
def consulta_dni(dni):
    url = f"{API_BASE_URL}/dni/{dni}"
    try:
        response = requests.get(url, headers=HEADERS)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/consulta/nombre', methods=['GET'])
def consulta_nombre():
    n1 = request.args.get('n1', '')
    ap1 = request.args.get('ap1', '')
    ap2 = request.args.get('ap2', '')
    
    url = f"{API_BASE_URL}/nm?n1={n1}&ap1={ap1}&ap2={ap2}"
    try:
        response = requests.get(url, headers=HEADERS)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
      
