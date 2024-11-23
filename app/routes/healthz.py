from flask import Blueprint

healthz_blueprint = Blueprint('healthz', __name__)

@healthz_blueprint.route('/', methods=['GET'])
def healthz():
    return "The server is running"