from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from auth.models import User
from auth.models import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter(User.username == username).first()
    if user and user.password == password:
        return jsonify({
            "success": True,
            "user": user.to_dict()
        })
    else:
        return jsonify({
            "success": False,
            "message": "用户名或密码错误",
        }), 401

@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))

@auth.post('/register')
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'success': False,
            'message': 'Missing required fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'User registered successfully'
    }), 201