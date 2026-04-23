"""
app.py

Main entry point for the Flask web application.
"""
from flask import Flask
from routes import bp as routes_bp
from graph import init_graph

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super_secret_key_for_train_connect_booking_simulation_only'
    
    # Register routes
    app.register_blueprint(routes_bp)
    
    # Initialize the railway network graph
    init_graph()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
