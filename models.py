from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Oda bilgileri
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)  # antre, salon, mutfak, yatak odası

# Sıcaklık bilgisi
class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    value = db.Column(db.Float)  # derece
    target = db.Column(db.Float)  # hedef sıcaklık
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Gaz bilgisi
class Gas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    status = db.Column(db.String(20))  # non-kritik, medium kritik, alarm
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Işık kontrolü
class Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    status = db.Column(db.String(10))  # acik, kapali
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Garaj kapısı
class Garage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10))  # acik, kapali
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Perde sistemi
class Curtain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    status = db.Column(db.String(10))  # acik, kapali
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Kamera (plaka tanıma)
class PlateRecognition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20))
    status = db.Column(db.String(20))  # tanındı, tanınamadı
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)