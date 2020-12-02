import datetime
from app import db, ma_convertsqljson

"""
 Definição da classe / tabela dos usuários e seus campos
"""


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ## Produção - o correto é ser unico
    # username = db.Column(db.String(20), unique=True, nullable=False)
    ## Teste - Para inserir o mesmo para testar
    username = db.Column(db.String(20), unique=False, nullable=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    ## Produção - o correto é ser unico
    # email = db.Column(db.String(50), unique=False, nullable=False)
    ## Teste - Para inserir o mesmo para testar
    email = db.Column(db.String(50), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email


"""
  Definindo o schema do Marshmallow para facilitar a utilização do JSON
"""


class UserSchema(ma_convertsqljson.Schema):
    class Meta:
        fields = ('id', 'username', 'name', 'email', 'password', 'created_on')


user_schema = UserSchema()
users_schema = UserSchema(many=True)  # O parametro many indica que será retornado um array
