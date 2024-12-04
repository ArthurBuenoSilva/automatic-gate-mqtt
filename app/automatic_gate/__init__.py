from flask import Blueprint

bp = Blueprint("automatic_gate", __name__)

from app.automatic_gate import routes
