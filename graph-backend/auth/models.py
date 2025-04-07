from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    truename = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')  # 用户角色：user/admin
    avatarUrl = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    tags = db.Column(db.String(225))
    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'truename': self.truename,
            'password': self.password,
            'email': self.email,
            'role': self.role,
            'avatar_url': self.avatarUrl,
            'phone': self.phone,
            'tags': self.tags
        }