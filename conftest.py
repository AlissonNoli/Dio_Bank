import sys
import os
import pytest
from src.app import create_app, db

@pytest.fixture()
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
        yield app
        
        # db.drop_all()
        
# @pytest.fixture(scope='module')
# def test_client():
#     flask_app = create_app({
#         'TESTING': True,
#         'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
#     })

#     with flask_app.test_client() as testing_client:
#         with flask_app.app_context():
#             db.create_all()
            
#             yield testing_client  
#             db.drop_all()
            
@pytest.fixture()
def client(app):
    return app.test_client()


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))