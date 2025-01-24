from flask import Blueprint, request


app = Blueprint("post", __name__, url_prefix="/posts")


@app.route('/', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'POST':
        pass
    else:
        pass
