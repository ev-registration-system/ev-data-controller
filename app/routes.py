from flask import Blueprint, jsonify
from app.controller import charger

bp = Blueprint('routes', __name__)

@bp.route('/state', methods=['GET'])
def get_state():
    return jsonify({'state': charger.get_state()})

@bp.route('/toggle', methods=['POST'])
def toggle_charger():
    charger.toggle()
    return jsonify({'message': 'Charger toggled', 'state': charger.get_state()})