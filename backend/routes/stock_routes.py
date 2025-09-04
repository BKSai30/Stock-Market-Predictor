from flask import Blueprint, jsonify

# Create a Flask Blueprint for stock routes
stock_bp = Blueprint('stock', __name__)

# Example route (you can add your real routes here)
@stock_bp.route('/stocks', methods=['GET'])
def get_stocks():
    # Just returns a sample response for now
    return jsonify({"message": "Stocks endpoint is working!"})
