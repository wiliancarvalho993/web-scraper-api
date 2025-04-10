from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 API de Raspagem Web está ativa!"

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    urls = data.get("urls")

    # Raspagem das URLs fornecidas
    content = ""
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove tags de script e style
            for tag in soup(["script", "style"]):
                tag.decompose()

            # Extrair e limpar o texto
            texto = soup.get_text(separator="\n")
            linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
            content += "\n".join(linhas[:100]) + "\n\n"
        except Exception as e:
            content += f"Erro ao processar a URL {url}: {str(e)}\n"

    return jsonify({"text": content})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")

    # Enviar a mensagem para o OpenAI
