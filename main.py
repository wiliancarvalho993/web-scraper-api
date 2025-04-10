from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# Adicione sua chave da OpenAI
openai.api_key = 'chabeee aqui'  # Substitua com sua chave da OpenAI

@app.route("/")
def home():
    return "🚀 API de Raspagem Web está ativa!"

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    url = data.get("url")

    try:
        # Raspando o conteúdo da URL
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remover scripts e estilos
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Pega o texto da página
        texto = soup.get_text(separator="\n")
        linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
        conteudo = "\n".join(linhas[:100])  # Limitando a 100 linhas

        # Enviar o conteúdo para a OpenAI gerar uma resposta interativa como uma vendedora
        prompt = f"""
        Você é uma vendedora muito simpática e prestativa. Responda de forma amigável e atenciosa, com base nas informações do conteúdo abaixo, como se estivesse explicando as notícias e dando informações de vendas para o cliente.

        Aqui está o conteúdo extraído do site:
        {conteudo}

        Agora, qualquer dúvida que o cliente tenha, seja sobre os produtos ou serviços, você deve responder de maneira profissional, amigável e persuasiva.
        """
        
        openai_response = openai.Completion.create(
            engine="text-davinci-003",  # Use o modelo mais adequado para o seu caso
            prompt=prompt,
            max_tokens=150,  # Ajuste conforme necessário
            temperature=0.7  # Aumente a "temperatura" para respostas mais criativas
        )

        # Obtenha a resposta da OpenAI
        resposta_openai = openai_response.choices[0].text.strip()

        return jsonify({"scraped_text": conteudo, "openai_response": resposta_openai})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
