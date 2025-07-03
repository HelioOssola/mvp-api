from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consumos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SQLAlchemy
db = SQLAlchemy(app)

# Habilitar CORS
CORS(app)

# Configuração do Swagger
swagger = Swagger(app)

# Modelo de tabela
class Consumo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'data': self.data,
            'quantidade': self.quantidade
        }

# Criação do banco
with app.app_context():
    db.create_all()

# Adicionar consumo
@app.route('/consumos', methods=['POST'])
def adicionar_consumo():
    """
    Adicionar um novo registro de consumo
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Consumo
          required:
            - data
            - quantidade
          properties:
            data:
              type: string
              example: "2025-06-30"
            quantidade:
              type: integer
              example: 2000
    responses:
      201:
        description: Registro criado com sucesso
      400:
        description: Dados inválidos
    """
    dados = request.get_json()
    data = dados.get('data')
    quantidade = dados.get('quantidade')

    if not data or not quantidade:
        return jsonify({'erro': 'Dados incompletos.'}), 400

    novo_consumo = Consumo(data=data, quantidade=quantidade)
    db.session.add(novo_consumo)
    db.session.commit()

    return jsonify({'mensagem': 'Registro criado com sucesso!'}), 201

# Listar consumos
@app.route('/consumos', methods=['GET'])
def listar_consumos():
    """
    Listar todos os registros de consumo
    ---
    responses:
      200:
        description: Lista de consumos
    """
    consumos = Consumo.query.all()
    return jsonify([c.to_dict() for c in consumos]), 200

# Buscar consumo por ID
@app.route('/consumos/<int:id>', methods=['GET'])
def buscar_consumo(id):
    """
    Buscar um registro específico
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do consumo
    responses:
      200:
        description: Registro encontrado
      404:
        description: Registro não encontrado
    """
    consumo = Consumo.query.get(id)
    if consumo:
        return jsonify(consumo.to_dict()), 200
    else:
        return jsonify({'erro': 'Registro não encontrado.'}), 404

# Deletar consumo
@app.route('/consumos/<int:id>', methods=['DELETE'])
def deletar_consumo(id):
    """
    Deletar um registro pelo ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do consumo
    responses:
      200:
        description: Registro deletado com sucesso
      404:
        description: Registro não encontrado
    """
    consumo = Consumo.query.get(id)
    if consumo:
        db.session.delete(consumo)
        db.session.commit()
        return jsonify({'mensagem': 'Registro deletado com sucesso!'}), 200
    else:
        return jsonify({'erro': 'Registro não encontrado.'}), 404

# Atualizar consumo
@app.route('/consumos/<int:id>', methods=['PUT'])
def atualizar_consumo(id):
    """
    Atualizar um registro pelo ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do consumo
      - in: body
        name: body
        required: true
        schema:
          id: ConsumoAtualizado
          required:
            - data
            - quantidade
          properties:
            data:
              type: string
              example: "2025-06-30"
            quantidade:
              type: integer
              example: 2500
    responses:
      200:
        description: Registro atualizado com sucesso
      404:
        description: Registro não encontrado
    """
    consumo = Consumo.query.get(id)
    if not consumo:
        return jsonify({'erro': 'Registro não encontrado.'}), 404

    dados = request.get_json()
    consumo.data = dados.get('data', consumo.data)
    consumo.quantidade = dados.get('quantidade', consumo.quantidade)

    db.session.commit()
    return jsonify({'mensagem': 'Registro atualizado com sucesso!'}), 200

# Executar app
if __name__ == '__main__':
    app.run(debug=True)
