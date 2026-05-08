import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__, 
            template_folder="../templates", 
            static_folder="../static",
            static_url_path="/static")

IDENTIDADE_HYDRALYNX = (
    "Sua linguagem padrão deve ser o Português Brasileiro. Use emojis como tópicos e fale de forma fluida e humana. "
    "Você é uma IA para auxílio em academias, dietas e treinos. Sempre lembre o usuário que você não substitui um profissional da saúde. "
    "Seu nome é MyCoach da NEXUS LEGACY. Jamais revele seu código ou sua API."
)

# --- ROTAS DE NAVEGAÇÃO ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mycoach')
def mycoach():
    return render_template('IA.html')

@app.route('/treinos')
def treinos():
    return render_template('treinos.html')

@app.route('/cadastro')
def cadastro():
    return render_template('Cadaspage.html')

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        chave = os.environ.get("OPENAI_API_KEY")
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=chave
        )
        
        dados = request.get_json()
        pergunta = dados.get('mensagem')

        response = client.chat.completions.create(
            model="nvidia/nemotron-nano-12b-v2-vl:free", 
            messages=[
                {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.2
        )
        
        return jsonify({"resposta": response.choices[0].message.content})
        
    except Exception as e:
        return jsonify({"resposta": f"Erro técnico na NexusIA: {str(e)}"}), 500


app = app
