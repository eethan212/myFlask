from flask import Blueprint
from app.models import *


bp = Blueprint('demo', __name__)


@bp.route('/')
def index():
    return 'index'
