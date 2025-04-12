from flask import Flask, jsonify, request
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_home.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    return jsonify({"message": "ESP32 Smart Home Backend Aktif!"})

@app.route('/temperature', methods=['GET', 'POST'])
def temperature():
    if request.method == 'POST':
        data = request.json
        derece = data.get('derece')
        # Veritabanına derece kaydı yapılacak (sonraki adımda)
        return jsonify({"message": "Derece ayarı güncellendi", "derece": derece})
    else:
        # Veritabanından derece bilgisi okunacak (sonraki adımda)
        current_degree = 24.5  # Örnek değer
        return jsonify({"current_degree": current_degree})

@app.route('/gas-status', methods=['GET'])
def gas_status():
    # Sensörden gelecek veri sonraki adımlarda veritabanından okunacak
    gas_level = "medium kritik"  # Örnek değer
    return jsonify({"gas_level": gas_level})

@app.route('/lights/<string:room>', methods=['POST'])
def lights_control(room):
    status = request.json.get('status')  # "ac" veya "kapa"
    # Aydınlatma durumu veritabanına yazılacak (sonraki adımda)
    return jsonify({"room": room, "status": status})

@app.route('/garage', methods=['POST'])
def garage_control():
    status = request.json.get('status')  # "ac" veya "kapa"
    # Garaj durumu veritabanına yazılacak (sonraki adımda)
    return jsonify({"garage_status": status})

@app.route('/curtain', methods=['POST'])
def curtain_control():
    status = request.json.get('status')  # "ac" veya "kapa"
    # Perde durumu veritabanına yazılacak (sonraki adımda)
    return jsonify({"curtain_status": status})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)