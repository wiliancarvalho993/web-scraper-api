from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS  # Importa o CORS

app = Flask(__name__)
CORS(app)  # Ativa o CORS em toda a aplicação

@app.route("/")
def home():
    return "🚀 API de Raspagem Web está ativa!"

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    url = data.get("url")

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts e estilos
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Extrai o texto limpo
        texto = soup.get_text(separator="\n")
        linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
        conteudo = "\n".join(linhas[:100])  # Limita a 100 linhas

        return jsonify({"text": conteudo})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
