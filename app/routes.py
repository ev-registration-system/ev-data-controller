from flask import Blueprint, jsonify, make_response
from app.controller import charger

bp = Blueprint('routes', __name__)

@bp.route('/state', methods=['GET'])
def get_state():
    return make_response(jsonify({'state': charger.get_state()}))

@bp.route('/toggle', methods=['POST'])
def toggle_charger():
    charger.toggle()
    return make_response(jsonify({'message': 'Charger toggled', 'state': charger.get_state()}))