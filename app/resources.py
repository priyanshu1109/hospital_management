from flask_restx import Resource,Namespace
from .models import Patient,Doctor,Department,MedicalHistory,Slot,Appointment
from .serializers import *
from .extensions import db
from flask import request

ns = Namespace('patients',path="/api")
nd = Namespace('departments',path="/api")
ndoc = Namespace('doctors',path="/api")

@ns.route('/patients')
class PatientAPI(Resource):

    @ns.marshal_list_with(patient_serializer)
    def get(self):
        return Patient.query.all()

    @ns.expect(patient_input_serializer)
    @ns.marshal_with(patient_serializer)
    def post(self):
        patient = Patient(name=ns.payload['name'],age=ns.payload['age'],contact=ns.payload['contact'],gender=ns.payload['gender'])
        db.session.add(patient)
        db.session.commit()
        return patient,201

@ndoc.route('/doctors')
class DoctorAPI(Resource):

    @ndoc.marshal_list_with(doctor_serializer)
    def get(self):
        return Doctor.query.all()

    @ndoc.expect(doctor_input_serializer)
    @ndoc.marshal_with(doctor_serializer)
    def post(self):
        doctor = Doctor(name=ndoc.payload['name'],specialization=ndoc.payload['specialization'],contact=ndoc.payload['contact'])
        s1 = Slot(slot_number=1,time='9:00',available='Yes')
        s2 = Slot(slot_number=2,time='10:00',available='Yes')
        s3 = Slot(slot_number=3,time='11:00',available='Yes')
        s4 = Slot(slot_number=4,time='12:00',available='Yes')
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.add(s4)
        doctor.schedule.append(s1)
        doctor.schedule.append(s2)
        doctor.schedule.append(s3)
        doctor.schedule.append(s4)
        db.session.add(doctor)
        db.session.commit()
        return doctor,201

@nd.route('/departments')
class DepartmentAPI(Resource):

    @nd.marshal_list_with(department_serializer)
    def get(self):
        return Department.query.all()

    @nd.expect(department_input_serializer)
    @nd.marshal_with(department_serializer)
    def post(self):
        department = Department(name=nd.payload['name'],services=nd.payload['services'])
        db.session.add(department)
        db.session.commit()
        return department,201

@ns.route('/patients/<int:id>/medical_history')
class MedicalHistoryAPI(Resource):

    @ns.expect(medicalhistory_input_serializer)
    @ns.marshal_with(medicalhistory_serializer)
    def post(self,id):
        history = MedicalHistory(diagnosis=ns.payload['diagnosis'],allergies=ns.payload['allergies'],medication=ns.payload['medication'])
        db.session.add(history)
        patient = Patient.query.get(id)
        print(patient)
        patient.medical.append(history)
        db.session.commit()
        return history,201
    
    @ns.marshal_with(medicalhistory_serializer)
    def get(self,id):
        patient = Patient.query.get(id)
        return patient.medical

@ns.route('/patients/<int:id>/appointments')
class PatientAppointmentAPI(Resource):

    @ns.marshal_with(patient_appointment_serializer)
    def get(self,id):
        patient = Patient.query.get(id)
        appointments = Appointment.query.filter(Appointment.patient_id==id).all()
        patients = []
        for doctor in appointments:
            d = Doctor.query.get(doctor.doctor_id)
            res = {'name':patient.name,'doctor_name':d.name,'appointment_time':doctor.appointment_time}
            patients.append(res)
        return patients
    

@nd.route('/departments/<int:id>/assign')
class AssignDoctorAPI(Resource):

    @nd.expect(assign_doctor_serializer)
    def put(self,id):
        department = Department.query.get(id)
        doctor = Doctor.query.get(nd.payload['doctor_id'])
        department.doctors.append(doctor)
        db.session.commit()
        return {'message':'Assigned'},201

@nd.route('/doctors/<int:id>/doctors')
class DepartmentDoctorAPI(Resource):

    @nd.marshal_list_with(doctor_serializer)
    def get(self,id):
        department = Department.query.get(id)
        return department.doctors

@ns.route('/patients/search')
class PatientSearchAPI(Resource):
    
    @ns.marshal_with(patient_serializer)
    @ns.expect(api.parser().add_argument('name', type=str, help='Patient name', required=True))
    def get(self):
        name = request.args.get('name')
        patients = Patient.query.filter(Patient.name.like(f'%{name}%')).all()
        return patients


@nd.route('/departments/search')
class DepartmentSearchAPI(Resource):

    @nd.marshal_with(department_serializer)
    @nd.expect(api.parser().add_argument('name', type=str, help='Department name', required=True))
    def get(self):
        name = request.args.get('name')
        departments = Department.query.filter(Department.name.like(f'%{name}%')).all()
        return departments

@ndoc.route('/doctors/search')
class DoctorSearchAPI(Resource):
    @ndoc.marshal_with(doctor_serializer)
    @ndoc.expect(api.parser().add_argument('specialization', type=str, help='Specialization', required=True))
    def get(self):
        specialization = request.args.get('specialization')
        doctors = Doctor.query.filter(Doctor.specialization.like(f'%{specialization}%')).all()
        return doctors

@ndoc.route('/doctors/<int:id>/availability')
class DoctorAvailabilityAPI(Resource):
    @ndoc.marshal_with(doctor_availability_serializer)
    def get(self,id):
        doctors = Doctor.query.get(id)
        return doctors.schedule

@ns.route('/patient/<int:id>/book/<string:time>')
class Booking(Resource):

    @ns.marshal_with(appointment_serializer)
    @ns.expect(book_doctor_serializer)
    def put(self,id,time):
        appointment = Appointment(doctor_id=ns.payload['doctor_id'],patient_id=id,appointment_time=time)
        db.session.add(appointment)
        doctor = Doctor.query.get(ns.payload['doctor_id'])
        for slots in doctor.schedule:
            if slots.time==time:
                if slots.available=='No':
                    return {"message":"Slot is already booked"}
                slots.available = 'No'
        db.session.commit()
        return appointment

@ndoc.route('/doctors/<int:id>/patients')
class DoctorPatientAPI(Resource):
    @ndoc.marshal_with(patient_serializer)
    def get(self,id):
        doctors = Doctor.query.get(id)
        appointments = Appointment.query.filter(Appointment.doctor_id==id)
        patients = []
        for patient in appointments:
            p = Patient.query.get(patient.patient_id)
            patients.append(p)
        return patients
