from flask import Blueprint, jsonify

volatility_bp = Blueprint('volatility', __name__)

@volatility_bp.route('/volatility', methods=['GET'])
def get_volatility():
    return jsonify({"message": "Volatility endpoint is working!"})
