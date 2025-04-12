from flask import Flask, jsonify, request
from models import db
from models import db, Temperature, Room


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
        oda_adi = data.get('room')           # örn: "salon"
        value = data.get('value')            # derece
        target = data.get('target')          # hedef sıcaklık

        # Oda varsa al, yoksa oluştur
        room = Room.query.filter_by(name=oda_adi).first()
        if not room:
            room = Room(name=oda_adi)
            db.session.add(room)
            db.session.commit()

        temp = Temperature(room_id=room.id, value=value, target=target)
        db.session.add(temp)
        db.session.commit()

        return jsonify({"message": "Sıcaklık verisi kaydedildi!"})

    elif request.method == 'GET':
        temps = Temperature.query.all()
        result = []
        for t in temps:
            result.append({
                "oda": Room.query.get(t.room_id).name,
                "deger": t.value,
                "hedef": t.target,
                "zaman": t.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
        return jsonify(result)


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