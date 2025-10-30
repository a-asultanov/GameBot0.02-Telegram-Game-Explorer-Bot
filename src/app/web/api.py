from flask import Flask, request, jsonify
import threading
import asyncio
from src.app.services.game_service import get_games_by_genre_and_year
import html
from src.app.web.models import db, RequestLog, User, Game
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from dotenv import load_dotenv
import os
from src.config import Config

load_dotenv()  

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

def create_admin_app():
    
    with app.app_context():
        db.create_all()

    admin = Admin(app, name='GameOracle Admin')
    admin.add_view(ModelView(Game, db.session))
    admin.add_view(ModelView(RequestLog, db.session))
    return app

# Простой health-check эндпоинт
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Flask API is running..."
    })



@app.route("/api/games/top", methods=["GET"])
def get_top_games():
     # Получаем и очищаем параметры
    genre = request.args.get("genre", "").strip().lower()
    year = request.args.get("year", "").strip()
    platform = request.args.get("platform", "").strip()

    if not genre or not year.isdigit() or not platform.isdigit():
        return jsonify({"error": "Некорректные параметры. Требуются genre, year и platform."}), 400

    try:
        games = asyncio.run(get_games_by_genre_and_year(genre, year, platform))
    except Exception as e:
        app.logger.error(f"[API ERROR] Ошибка при получении игр: {e}")
        return jsonify({"error": "Ошибка сервера. Попробуйте позже."}), 500

    if not games:
        return jsonify({"count": 0, "games": []}), 200

    safe_games = []
    for g in games:
        safe_games.append({
            "name": html.escape(g.get("name", "")),
            "slug": html.escape(g.get("slug", "")),
            "rating": g.get("rating", 0),
            "released": html.escape(str(g.get("released", ""))),
            "background_image": g.get("background_image"),
        })

    

    # --- ЛОГИРОВАНИЕ ЗАПРОСА ---
    try:
        user_id = request.args.get("user_id")
        username = request.args.get("username", "unknown")

        try:
            user_id = int(user_id) if user_id else 0
        except ValueError:
            user_id = 0


        user = db.session.get(User, user_id)
        if not user:
            user = User(id=user_id, username=username)
            db.session.add(user)
            db.session.commit()

        log = RequestLog(
            user_id=user_id,
            username=username,
            genre=genre,
            platform=platform,
            year=year
        )

        db.session.add(log)
        db.session.commit()

    except Exception as e:
        app.logger.error(f"Ошибка при логировании запроса: {e}")


    return jsonify({
        "count": len(safe_games),
        "games": safe_games
    })


def run_flask():
    app.run(host='127.0.0.1', port=5000)

