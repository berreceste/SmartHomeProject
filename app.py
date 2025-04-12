from flask import Flask, jsonify, request
from models import db
from models import db, Temperature, Room
from models import Gas
from flask_mqtt import Mqtt
import json




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_home.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# MQTT Konfigürasyonu
app.config['MQTT_BROKER_URL'] = 'localhost'  # MQTT sunucusu
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)


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

@app.route('/gas-status', methods=['GET', 'POST'])
def gas_status():
    if request.method == 'POST':
        data = request.json
        room_name = data.get('room')  # örn: mutfak
        status = data.get('status')   # non-kritik / medium kritik / alarm

        # Oda kontrolü
        room = Room.query.filter_by(name=room_name).first()
        if not room:
            room = Room(name=room_name)
            db.session.add(room)
            db.session.commit()

        gaz = Gas(room_id=room.id, status=status)
        db.session.add(gaz)
        db.session.commit()

        return jsonify({"message": "Gaz verisi kaydedildi!"})

    elif request.method == 'GET':
        records = Gas.query.all()
        result = []
        for g in records:
            result.append({
                "oda": Room.query.get(g.room_id).name,
                "durum": g.status,
                "zaman": g.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
        return jsonify(result)

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

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("MQTT bağlantısı sağlandı.")
    mqtt.subscribe('esp32/sensors/temperature')  # sıcaklık
    mqtt.subscribe('esp32/sensors/gas')          # gaz

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print(f"MQTT mesaj alındı: {topic} => {payload}")

    try:
        data = json.loads(payload)

        if topic == 'esp32/sensors/temperature':
            room = data.get('room')
            value = data.get('value')
            target = data.get('target', None)

            room_obj = Room.query.filter_by(name=room).first()
            if not room_obj:
                room_obj = Room(name=room)
                db.session.add(room_obj)
                db.session.commit()

            new_temp = Temperature(room_id=room_obj.id, value=value, target=target)
            db.session.add(new_temp)
            db.session.commit()

        elif topic == 'esp32/sensors/gas':
            room = data.get('room')
            status = data.get('status')

            room_obj = Room.query.filter_by(name=room).first()
            if not room_obj:
                room_obj = Room(name=room)
                db.session.add(room_obj)
                db.session.commit()

            new_gas = Gas(room_id=room_obj.id, status=status)
            db.session.add(new_gas)
            db.session.commit()

    except Exception as e:
        print(f"Hata oluştu: {e}")