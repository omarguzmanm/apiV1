# routes/routes.py
from flask import Flask
from routes.recommendation_logic import get_recommendations_logic

app = Flask(__name__)

@app.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    return get_recommendations_logic(user_id)
