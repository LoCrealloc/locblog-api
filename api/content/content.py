from flask import Blueprint, jsonify

content = Blueprint("content", __name__, url_prefix="/content")
