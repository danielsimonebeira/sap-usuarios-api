from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify

from ..models.users import Usuarios, user_schema, users_schema


def post_usuario():
    # json_data = request.get_json(force=True)
    conteudo = request.json
    username = conteudo['username']
    password = conteudo['password']
    name = conteudo['name']
    email = conteudo['email']

    pass_hash = generate_password_hash(password)
    usuario = Usuarios(username=username.upper(),
                    password=pass_hash,
                    name=name,
                    email=email)
    try:
        db.session.add(usuario)
        db.session.commit()
        result = user_schema.dump(usuario)
        return jsonify({'message': 'Registrado com sucesso', 'data': result}), 201
    except:
        return jsonify({'message': 'Não foi possivel registrar', 'data': {}}), 500


def update_usuario(id):
    conteudo = request.json
    username = conteudo['username']
    password = conteudo['password']
    name = conteudo['name']
    email = conteudo['email']

    usuario = Usuarios.query.get(id)

    if not usuario:
        return jsonify({'message': 'usuário não existe no sistema', 'data': {}})

    pass_hash = generate_password_hash(password)

    try:
        usuario.username = username.upper()
        usuario.password = pass_hash
        usuario.name = name
        usuario.email = email
        db.session.commit()
        resultado = user_schema.dump(usuario)
        return jsonify({'message': 'Alterado com sucesso', 'data': resultado}), 201
    except:
        return jsonify({'message': 'Não foi possivel registrar', 'data': {}}), 500


def get_usuarios():
    usuarios = Usuarios.query.all()
    if usuarios:
        resultado = users_schema.dump(usuarios)
        return jsonify({'message': 'Busca de usuarios efetuada com sucesso', 'data': resultado}), 201
    return jsonify({'message': 'Usuários não existe no sistema.', 'data': {}}), 500


def get_usuarioid(id):
    usuario = Usuarios.query.get(id)
    if usuario:
        resultado = user_schema.dump(usuario)
        return jsonify({'message': 'Busca do usuário efetuada com sucesso.', 'data': resultado})
    return jsonify({'message': 'Usuário não existe no sistema.', 'data': {}})


def delete_usuario(id):
    usuario = Usuarios.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuário não existe no sistema', 'data': {}}), 404

    if usuario:
        try:
            db.session.delete(usuario)
            db.session.commit()
            resultado = user_schema.dump(usuario)
            return jsonify({'message': 'Usuario deletado com sucesso', 'data': resultado})
        except:
            return jsonify({'message': 'Não foi possivel deletar usuário'}), 500


def filtra_usuario(username):
    try:
        return Usuarios.query.filter(Usuarios.username == username.upper()).one()
    except:
        return None
