from flask import Flask, jsonify, send_from_directory, g
import os
from flask_cors import CORS

# Existing route imports
from routes.market_routes import market_bp
from routes.portfolio_routes import portfolio_bp
from routes.team_routes import team_bp
from routes.user_routes import user_bp

# <-- UPDATED LINE: import transactions blueprint from transaction_routes.py
from routes.transaction_routes import transactions_bp

# Import and trigger the market data fetch
from services.market_service import fetch_and_cache_market_data
fetch_and_cache_market_data()  # <-- run once per backend startup

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['STATIC_FOLDER'] = 'static'  # Set the static folder

# Register blueprints
app.register_blueprint(market_bp)
app.register_blueprint(portfolio_bp)
app.register_blueprint(team_bp)
app.register_blueprint(user_bp)

# <-- UPDATED LINE: register transactions blueprint
app.register_blueprint(transactions_bp)  

# Basic homepage route
@app.route('/')
def homepage():
    return jsonify({"message": "Finance Portfolio API"})

# Serve static files (e.g. images)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
