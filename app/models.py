from .extensions import db

class Patient(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.String(50),nullable=False)
    contact = db.Column(db.String(10),nullable=False)
    medical = db.relationship('MedicalHistory', backref='patient')

class MedicalHistory(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    diagnosis = db.Column(db.String(100),nullable=False)
    allergies = db.Column(db.String(100),nullable=False)
    medication = db.Column(db.String(100),nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    #patient = db.relationship('Patient', backref='medical_history', lazy=True)

class Doctor(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    specialization = db.Column(db.String(50),nullable=False)
    contact = db.Column(db.String(10),nullable=False)
    department_id = db.Column(db.ForeignKey("department.id"))
    schedule = db.relationship("Slot",backref="doctor",lazy=True)


class Department(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=True)
    services = db.Column(db.String(50),nullable=True)
    doctors = db.relationship("Doctor",backref="department",lazy=True)
    #doctor_id = db.Column(db.ForeignKey("doctor.id"))

class Appointment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    patient_id = db.Column(db.String(50),nullable=False)
    doctor_id = db.Column(db.String(50),nullable=False)
    appointment_time = db.Column(db.String(20),nullable=False)

class Slot(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    slot_number = db.Column(db.Integer,nullable=False)
    time = db.Column(db.String(20),nullable=False)
    available = db.Column(db.String(10),nullable=False,default='Yes')
    doctor_id = db.Column(db.ForeignKey("doctor.id"))