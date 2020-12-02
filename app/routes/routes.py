from app import app
from flask import jsonify
from app.views import users, helper


@app.route('/', methods=['GET'])
@helper.token_requerido
def root(usuario_atual):
    return jsonify({'message': 'SAP - Sistema de achados e perdidos'})


@app.route('/usuarios', methods=['POST'])
def post_usuario():
    return users.post_usuario()


@app.route('/usuarios/<id>', methods=['PUT'])
def put_usuario(id):
    return users.update_usuario(id)


@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    return users.get_usuarios()


@app.route('/usuarios/<id>', methods=['GET'])
def get_usuario(id):
    return users.get_usuarioid(id)


@app.route('/usuarios/<id>', methods=['DELETE'])
def delete_usuario(id):
    return users.delete_usuario(id)


@app.route('/autentica', methods=['POST'])
def autentica():
    return helper.auth()
