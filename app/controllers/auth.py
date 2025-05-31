# C:\Users\ianes\Desktop\AS-Cloud\app\auth\auth.py

from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

auth_ns = Namespace('auth', description='Autenticação de usuários')

# Modelos para documentação
signup_model = auth_ns.model('Signup', {
    'username': fields.String(required=True, description='Nome de usuário'),
    'password': fields.String(required=True, description='Senha')
})

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Nome de usuário'),
    'password': fields.String(required=True, description='Senha')
})

@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.expect(signup_model, validate=True)
    @auth_ns.response(201, 'Usuário criado com sucesso.')
    @auth_ns.response(400, 'Usuário já existe.')
    def post(self):
        """Registra um novo usuário"""
        data = auth_ns.payload
        if User.query.filter_by(username=data['username']).first():
            auth_ns.abort(400, 'Usuário já existe.')
        user = User(
            username=data['username'],
            password_hash=generate_password_hash(data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return {'message': 'Usuário criado'}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login bem-sucedido.')
    @auth_ns.response(401, 'Usuário ou senha inválidos.')
    def post(self):
        """Realiza login e inicia sessão"""
        data = auth_ns.payload
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password_hash, data['password']):
            auth_ns.abort(401, 'Usuário ou senha inválidos.')
        login_user(user)
        return {'message': 'Logado com sucesso'}, 200

@auth_ns.route('/logout')
class Logout(Resource):
    @login_required
    @auth_ns.response(200, 'Logout realizado.')
    def post(self):
        """Encerra a sessão do usuário"""
        logout_user()
        return {'message': 'Deslogado'}, 200
