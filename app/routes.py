from app import app
from flask import jsonify, request
import json

# Carregar os dados de um arquivo JSON
def carregar_dados():
    with open('app/clientes.json', 'r') as f:
        return json.load(f)

# Salvar os dados de volta para o arquivo JSON
def salvar_dados(dados):
    with open('app/clientes.json', 'w') as f:
        json.dump(dados, f, indent=4)

# Rota GET para listar todos os clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    dados = carregar_dados()
    return jsonify(dados)

# Rota GET para obter um cliente específico por ID
@app.route('/clientes/<string:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    dados = carregar_dados()
    # Comparar o cliente_id da URL com o cliente_id no arquivo JSON
    cliente = next((c for c in dados if str(c['cliente_id']) == cliente_id), None)
    if cliente:
        return jsonify(cliente)
    return jsonify({"message": "Cliente não encontrado"}), 404


# Rota POST para adicionar um novo cliente
@app.route('/clientes', methods=['POST'])
def add_cliente():
    dados = carregar_dados()
    novo_cliente = request.get_json()
    dados.append(novo_cliente)
    salvar_dados(dados)
    return jsonify(novo_cliente), 201

# Rota PUT para atualizar um cliente existente
@app.route('/clientes/<string:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    dados = carregar_dados()
    cliente = next((c for c in dados if c['cliente_id'] == cliente_id), None)
    if cliente:
        dados.remove(cliente)
        cliente_atualizado = request.get_json()
        cliente_atualizado['cliente_id'] = cliente_id  # Manter o mesmo cliente_id
        dados.append(cliente_atualizado)
        salvar_dados(dados)
        return jsonify(cliente_atualizado)
    return jsonify({"message": "Cliente não encontrado"}), 404

# Rota DELETE para remover um cliente
@app.route('/clientes/<string:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    dados = carregar_dados()
    cliente = next((c for c in dados if c['cliente_id'] == cliente_id), None)
    if cliente:
        dados.remove(cliente)
        salvar_dados(dados)
        return jsonify({"message": "Cliente removido com sucesso"}), 200
    return jsonify({"message": "Cliente não encontrado"}), 404
