from flask import Blueprint, request


app = Blueprint("user", __name__, url_prefix="/users")


@app.route('/', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'POST':
        pass
    else:
        pass
