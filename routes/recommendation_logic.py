from flask import jsonify
from db.db import conn
from model.recommendation_model import df, model

def get_recommendations_logic(user_id):
 # Filtrar las preferencias del usuario
    user_preferences = df[df['user_id'] == user_id]
    user_tags = user_preferences['tag_id'].tolist()

    # Consultar la base de datos para obtener los posts asociados a los tags recomendados
    cursor = conn.cursor()
    if user_tags:
        cursor.execute("SELECT post_id FROM post_tag WHERE tag_id IN (%s)" % (','.join(['%s'] * len(user_tags))), user_tags)
        post_ids = cursor.fetchall()
    else:
        post_ids = []

    cursor.close()

    post_ids = [post_id[0] for post_id in post_ids]

    # Hacer predicciones para el usuario
    user_predictions = [model.predict(user_id, post_id) for post_id in post_ids]

    # Obtener las predicciones del modelo SVD para los posts asociados a los tags recomendados
    predicted_posts_dict = {}  # Diccionario para almacenar las predicciones únicas

    for prediction in user_predictions:
        post_id = prediction.iid
        if post_id not in predicted_posts_dict or prediction.est > predicted_posts_dict[post_id]['predicted_rating']:
            # Si no hemos registrado esta predicción para este post o la nueva predicción es mejor
            predicted_posts_dict[post_id] = {
                'post_id': post_id,
                'predicted_rating': prediction.est
            }

    # Obtener la lista final de predicciones únicas
    unique_posts = list(predicted_posts_dict.values())

    # Ordenar los posts según la puntuación predicha en orden descendente
    unique_posts = sorted(
        unique_posts,
        key=lambda x: x['predicted_rating'],
        reverse=True
    )

    # Devolver la lista de posts recomendados con IDs únicos
    return jsonify({'user_id': user_id, 'recommended_posts': unique_posts})
    