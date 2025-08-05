from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime
import os
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # troque por uma chave segura em produção

DB_PATH = 'database.json'

ASKMUSIC = ["A música despertou alguma emoção em você?", "A voz do cantor/cantora te agradou?", "Você escutaria essa música de novo?", "A letra tem alguma mensagem relevante ou interessante?", "A produção musical pareceu bem feita?", "Você indicaria essa música para alguém?", "O refrão ficou na sua cabeça?", "A música te lembrou de algum momento da sua vida?", "O estilo da música combina com seu gosto pessoal?", "O artista parece ter identidade própria?", "Você sentiu autenticidade na performance?", "A música é diferente do que você costuma ouvir?", "O ritmo te fez querer dançar ou se mexer?", "A música tem potencial para se tornar um hit?", "A capa ou imagem do artista te chamou atenção positivamente?", "A letra é fácil de entender e acompanhar?", "Você escutaria essa música em diferentes momentos do dia?", "A música te deixou com vontade de conhecer mais do artista?", "A música passa algum sentimento verdadeiro?", "A melodia é agradável aos ouvidos?", "A música tem alguma parte que te marcou especialmente?", "O clipe (se houver) contribui positivamente para a experiência?", "Você acha que o artista é consistente com outras músicas dele(a)?", "A música é original em comparação com outras do mesmo gênero?", "A batida ou instrumental chamou sua atenção de forma positiva?", "Você se vê colocando essa música em uma playlist sua?", "Você acha que o artista tem talento?", "A música te surpreendeu de alguma forma?", "Você acha que o artista tem futuro na indústria?", "Você recomendaria essa música/artista para alguém com gosto musical diferente do seu?"]
IMGSRANDOM = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

def resetar_se_novo_dia(user):
    hoje = datetime.now().date().isoformat()
    if user.get('last_evaluation_date') != hoje:
        user['evaluations_today'] = 0
        user['earned_today'] = 0.0
        user['last_evaluation_date'] = hoje

# Função para carregar o banco de dados
def load_db():
    if not os.path.exists(DB_PATH):
        return {"users": {}}
    with open(DB_PATH, 'r') as file:
        return json.load(file)

# Função para salvar no banco de dados
def save_db(data):
    with open(DB_PATH, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def home():
    return redirect(url_for('login'))

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = load_db()
        user = db['users'].get(username)

        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

# Rota de cadastro
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if password != confirm_password:
        return render_template('login.html', error="Passwords do not match.")

    db = load_db()

    if username in db['users']:
        return render_template('login.html', error="Username already exists.")

    db['users'][username] = {
        "password": password,
        "paypal": "",
        "balance": 180.0,
        "withdrawn": 0.0,
        "created_at": datetime.now().isoformat(),
        "last_withdraw_date": None,
        "evaluations_today": 0
    }

    save_db(db)
    session['username'] = username
    return render_template('login.html', success="Username created.")

# Rota do dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = load_db()
    username = session['username']
    user = db['users'].get(username)

    if not user:
        return "User not found.", 404

    # Verifica se já é outro dia e zera a contagem
    today = datetime.now().date().isoformat()
    if user.get("last_evaluation_date") != today:
        user["evaluations_today"] = 0
        user["earned_today"] = 0.0
        user["last_evaluation_date"] = today
        save_db(db)

    return render_template('dashboard.html', user=user, username=username)

@app.route('/rating')
def rating():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = load_db()
    username = session['username']
    user = db['users'][username]

    # Resetar contadores se for novo dia
    resetar_se_novo_dia(user)

    # Verificação de limite
    if user['evaluations_today'] >= 16 or user['earned_today'] >= 120.0:
        save_db(db)  # salvar reset, se tiver sido feito
        return redirect(url_for('dashboard'))

    save_db(db)  # mesmo que não redirecione, salvar possíveis resets

    # Sorteia 16 perguntas aleatórias
    perguntas = random.sample(ASKMUSIC, 16)
    images = random.sample(IMGSRANDOM, 16)

    return render_template('rating.html', user=user, perguntas=perguntas, images=images)

@app.route('/salvar-avaliacoes', methods=['POST'])
def salvar_avaliacoes():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = load_db()
    username = session['username']
    user = db['users'][username]

    today = datetime.now().date().isoformat()

    user['evaluations_today'] = 16
    user['earned_today'] = 120.0
    user['balance'] += 120.0
    user['last_evaluation_date'] = today

    save_db(db)

    return redirect(url_for('dashboard'))


# Rota de logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Execução local
if __name__ == '__main__':
    app.run(debug=True, host='192.168.15.117', port=8080)
