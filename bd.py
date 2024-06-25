from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuração da chave secreta para sessões
app.secret_key = 'sua_chave_secreta'  # Use uma chave secreta segura para as sessões

# Configuração da URI do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bd_site'  # Ajuste o nome do banco de dados conforme necessário
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização da extensão SQLAlchemy
db = SQLAlchemy(app)

# Definição do modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(200), nullable=False)

# Rota para a página de cadastro
@app.route('/cadastro')
def cadastro_page():
    return render_template('cadastrar.html')

# Rota para processar o cadastro de usuário
@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    cpf = request.form['cpf']
    nome = request.form['nome']
    senha = request.form['senha']

    # Verifica se o usuário já existe pelo email ou CPF
    existing_user = User.query.filter_by(email=email).first() or User.query.filter_by(cpf=cpf).first()

    if existing_user:
        return jsonify({'status': 'error', 'message': 'Email ou CPF já cadastrados.'}), 400

    # Cria um novo usuário
    hashed_password = generate_password_hash(senha, method='sha256')
    new_user = User(email=email, cpf=cpf, nome=nome, senha=hashed_password)

    # Adiciona o novo usuário ao banco de dados
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Usuário cadastrado com sucesso!'})

if __name__ == '__main__':
    db.create_all()  # Cria as tabelas no banco de dados, se ainda não existirem
    app.run(debug=True)
