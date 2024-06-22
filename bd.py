from flask import Flask, render_template, request, redirect, session, jsonify, app# type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore


app = Flask(__name__)


app.secret_key = 'sua_chave_secreta'  # Use uma chave secreta segura para as sessões
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bd_site.sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Definição do modelo de usuário
db = SQLAlchemy(app)
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