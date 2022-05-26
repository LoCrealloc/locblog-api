from flask import Blueprint, jsonify

admin = Blueprint("admin", __name__, url_prefix="/admin")
