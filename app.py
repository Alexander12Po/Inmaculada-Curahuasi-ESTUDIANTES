from flask import Flask, request, jsonify, render_template
import requests
import re

app = Flask(__name__)

# Configuración de tu API externa y Token Privado
API_BASE_URL = "https://api-codart.cgrt.org/api/v1/consultas/fd"
TOKEN = "jmdCRmBLZ13ITSmUGCWcBnDcTuOddttU7d0UbL8S7HJNelk8loSpnVkUyFJO"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

# NOTA: la consulta por nombre usa los mismos headers que la de DNI.
# Se probó agregar "Content-Type: application/json" (como sugería la
# documentación) pero en una petición GET sin cuerpo esto provocó que
# la API externa respondiera 404 en vez de procesar la consulta, así
# que se quitó.
HEADERS_NOMBRE = HEADERS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/consulta/dni/<dni>', methods=['GET'])
def consulta_dni(dni):
    if not dni.isdigit() or len(dni) != 8:
        return jsonify({"success": False, "error": "El DNI debe tener 8 dígitos numéricos."}), 400

    url = f"{API_BASE_URL}/dni/{dni}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        try:
            body = response.json()
        except ValueError:
            return jsonify({"success": False, "error": "La API externa no devolvió JSON válido."}), 502
        return jsonify(body), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"No se pudo contactar la API externa: {e}"}), 502

@app.route('/api/consulta/nombre', methods=['GET'])
def consulta_nombre():
    n1 = request.args.get('n1', '').strip()
    ap1 = request.args.get('ap1', '').strip()
    ap2 = request.args.get('ap2', '').strip()

    segmentos_validos = [s for s in (n1, ap1, ap2) if s and re.search(r'[A-Za-zÁÉÍÓÚÑáéíóúñ]', s)]
    if len(segmentos_validos) < 2:
        return jsonify({"success": False, "error": "Escribe al menos nombre y apellido (2 palabras)."}), 400

    url = f"{API_BASE_URL}/nm"
    params = {"n1": n1, "ap1": ap1, "ap2": ap2}
    try:
        response = requests.get(url, headers=HEADERS_NOMBRE, params=params, timeout=10)
        try:
            body = response.json()
        except ValueError:
            return jsonify({"success": False, "error": "La API externa no devolvió JSON válido."}), 502
        return jsonify(body), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"No se pudo contactar la API externa: {e}"}), 502
      
