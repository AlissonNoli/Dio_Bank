import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import JWTManager, create_access_token
from src.controllers.post import app as post_bp
from src.app import db, User, Post

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key

    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(post_bp)

    with app.app_context():
        db.create_all()
        user = User(username='testuser', password='testpassword', role_id=1)
        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def access_token(app):
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        return create_access_token(identity=str(user.id))

def test_list_posts(client: FlaskClient, access_token: str):
    response = client.get('/posts/', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert 'posts' in response.json
    assert isinstance(response.json['posts'], list)

def test_create_post(client: FlaskClient, access_token: str):
    response = client.post('/posts/', json={
        'title': 'Test Post',
        'body': 'This is a test post.'
    }, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 201
    assert response.json['title'] == 'Test Post'
    assert response.json['body'] == 'This is a test post.'
    assert 'author_id' in response.json