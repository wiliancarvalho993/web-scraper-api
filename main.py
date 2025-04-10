from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Inicializando o OpenAI com a chave da API armazenada em variáveis de ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 API de Raspagem Web está ativa!"

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    urls = data.get("urls")  # Obtém a lista de URLs

    if not urls:
        return jsonify({"error": "No URLs provided"}), 400

    scraped_data = []
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style"]):
                tag.decompose()

            texto = soup.get_text(separator="\n")
            linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
            conteudo = "\n".join(linhas[:100])  # Limitando as primeiras 100 linhas do texto

            # Armazenando o conteúdo raspado para cada URL
            scraped_data.append({"url": url, "content": conteudo})
        except Exception as e:
            scraped_data.append({"url": url, "error": str(e)})

    return jsonify({"data": scraped_data})


if __name__ == "__main__":
    app.run(debug=True)
