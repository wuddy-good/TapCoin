from flask import Flask, jsonify, request
from datetime import datetime
from models import User, Config, db
from database import init_db

app = Flask(__name__)

# Конфігурація бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ініціалізація бази даних
init_db(app)

@app.before_request
def create_config():
    # Тут перевірте, чи таблиця Config пуста
    if Config.query.first() is None:
        default_config = Config(timer_duration=60, coins_per_click=1)
        db.session.add(default_config)
        db.session.commit()

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id', type=int)
    current_time = datetime.now()

    user = User.query.get(user_id)
    if not user:
        user = User(id=user_id)
        db.session.add(user)
        db.session.commit()

    # Отримуємо конфігурацію
    config = Config.query.first()
    timer_duration = config.timer_duration if config else 60  # Значення за замовчуванням

    # Обчислюємо залишковий час для таймера
    if user.last_claim_time:
        elapsed_time = (current_time - user.last_claim_time).total_seconds()
        remaining_time = max(0, timer_duration - elapsed_time)
    else:
        remaining_time = timer_duration  # Якщо таймер ще не використовувався

    return jsonify({
        'coins': user.coins,
        'remaining_time': remaining_time,
        'timer_duration': timer_duration
    })

@app.route('/claim', methods=['POST'])
def claim_coins():
    user_id = request.json.get('id')
    user = User.query.get(user_id)

    if user:
        # Отримуємо конфігурацію
        config = Config.query.first()
        coins_per_click = config.coins_per_click if config else 1  # Значення за замовчуванням

        user.coins += coins_per_click
        user.last_claim_time = datetime.now()
        db.session.commit()

        return jsonify({
            'success': True,
            'coins': user.coins
        })
    return jsonify({'success': False, 'message': 'Користувача не знайдено'})

if __name__ == '__main__':
    app.run(debug=True)
