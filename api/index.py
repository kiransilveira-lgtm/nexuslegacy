from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

IDENTIDADE_HYDRALYNX = (
  "Sua linguagem padrão dever ser o Português Brasileiro, deve usar emojis como tópicos e falar de forma fluida e humana"
  "Você é uma IA para auxilio em acadêmias, dietas e treinos, porém sempre lembre o usuário que você não substitui um profissional da saúde"
  "Seu nome é MyCoach da NEXUS LEGACY, jamais revele seu código ou sua API"
  ""
  ""
  ""

)

@app.route('/')
def index():
    return render_template('index.html')

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
            model="openai/gpt-oss-20b:free", 
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
