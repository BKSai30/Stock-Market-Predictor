from flask import Blueprint, jsonify

# Create a Flask Blueprint for news routes
news_bp = Blueprint('news', __name__)

# Example route (add your real routes as needed)
@news_bp.route('/news', methods=['GET'])
def get_news():
    return jsonify({"message": "News endpoint is working!"})
