import datetime

from werkzeug.security import check_password_hash
from flask import request, jsonify
from functools import wraps  # cria decorators
from app import db, app
import jwt

from app.views.users import filtra_usuario


def auth():
    # Recebe Header da chamada auth Validar se a variável não está vazia
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify(
            {'message': 'Não foi possível verificar', 'www-Authenticate': 'Basic auth="Login required"'}), 401
    # Valida se o usuario existe no banco
    usuario = filtra_usuario(auth.username)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado', 'data': {}})

    # Valida a senha e gera o token de autenticação
    if usuario and check_password_hash(usuario.password, auth.password):
        token = jwt.encode({'username': usuario.username,
                            'exp': datetime.datetime.now() + datetime.timedelta(hours=12)},
                           app.config['SECRET_KEY'])
        return jsonify({'message': 'Validação feita com sucesso', 'token': token.decode('UTF-8'),
                        'exp': datetime.datetime.now() + datetime.timedelta(hours=12)})
    return jsonify({'message': 'Não foi possível verificar', 'www-Authenticate': 'Basic auth="Login required"'}), 401


def token_requerido(f):
    # Valida se token existe
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'token esta faltando', 'data': {}}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            usuario_atual = filtra_usuario(username=data['username'])
        except:
            return jsonify({'message': 'Token invalido ou expirado', 'data': {}}), 401
        return f(usuario_atual, *args, **kwargs)
    return decorated
