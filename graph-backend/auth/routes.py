import os

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from auth.models import User
from auth.models import db
import uuid

auth = Blueprint('auth', __name__)
# 配置文件上传
AVATARS_FOLDER = os.path.join('static', 'avatars')  # 保存到 static/avatars 目录
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 允许的文件类型
MAX_FILE_SIZE = 2 * 1024 * 1024  # 最大文件大小（2MB）

# 确保 avatars 目录存在
if not os.path.exists(AVATARS_FOLDER):
    os.makedirs(AVATARS_FOLDER)

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

#修改用户信息
@auth.route('/infoChange', methods=['POST'])
def infoChange():
    data = request.get_json()
    print("data" + str(data))
    id = data.get('user_id')
    user = User.query.get(id)
    print("user", user)
    user.username = data.get('username')
    # avatar_url  = user.avatarUrl
    # 删除对应的头像，删不了一点
    # static_index = avatar_url.find('/static/')
    # relative_path = avatar_url[static_index:]
    # print("delete", relative_path)
    # if avatar_url and os.path.exists(relative_path):
    #     print("delete!!!")
    #     os.remove(avatar_url)
    user.avatarUrl = data.get('avatar_url')
    user.phone = data.get('phone')
    user.email = data.get('email')
    user.gender = data.get('gender')
    user.age = data.get('age')
    user.password = data.get('password')
    user.tags = data.get('tags')
    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'User info changed successfully'
    }), 201


# 检查文件类型是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@auth.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# 上传文件接口
@auth.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '未上传文件'}), 400

    file = request.files['file']

    # 检查文件是否存在
    if file.filename == '':
        return jsonify({'success': False, 'message': '未选择文件'}), 400

    # 检查文件类型和大小
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': '文件类型不支持'}), 400

    file.seek(0, os.SEEK_END)  # 移动到文件末尾
    file_size = file.tell()  # 获取文件大小
    file.seek(0)  # 重置文件指针

    if file_size > MAX_FILE_SIZE:
        return jsonify({'success': False, 'message': '文件大小不能超过 2MB'}), 400

    # 生成唯一文件名
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f'{uuid.uuid4().hex}.{file_ext}'
    file_path = os.path.join(AVATARS_FOLDER, unique_filename)
    file.save(file_path)

    # userid = request.form.get('userId')
    # 返回文件访问 URL
    file_url = f'http://localhost:5000/static/avatars/{unique_filename}'
    return jsonify({'success': True, 'url': file_url})

@auth.route('/adduser', methods=['POST'])
def add_user():
    data = request.get_json()
    print(data)
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'success': False,'message': 'Username already exists'}), 400
    user = User()
    user.username = data.get('username')
    user.password = data.get('password')
    user.email = data.get('email')
    user.gender = data.get('gender')
    user.age = data.get('age')
    user.phone = data.get('phone')
    user.avatarUrl = data.get('avatar_url')
    user.tags = data.get('tags')
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@auth.route('/user/<int:userId>', methods=['DELETE'])
def delete_user(userId):
    user = User.query.get(userId)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User deleted successfully'}), 200