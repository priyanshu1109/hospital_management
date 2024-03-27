from flask_restx import fields
from .extensions import api

patient_serializer = api.model("Patient",{
    "id":fields.Integer,
    "name":fields.String,
    "age": fields.Integer,
    "gender": fields.String,
    "contact": fields.String
})

patient_input_serializer = api.model("PatientInput",{
    "name":fields.String,
    "age":fields.Integer,
    "gender":fields.String,
    "contact":fields.String
})

medicalhistory_serializer = api.model("MedicalHistory",{
    "diagnosis":fields.String,
    "allergies":fields.String,
    "medication":fields.String
})


medicalhistory_input_serializer = api.model("MedicalHistoryInput",{
    "diagnosis":fields.String,
    "allergies":fields.String,
    "medication":fields.String
})

doctor_serializer = api.model("Doctor",{
    "id":fields.Integer,
    "name":fields.String,
    "specialization": fields.String,
    "contact": fields.String
})

doctor_availability_serializer = api.model("Slots",{
    "id":fields.Integer,
    "slot_number":fields.Integer,
    "time": fields.String,
    "available": fields.String
})


doctor_input_serializer = api.model("DoctorInput",{
    "name":fields.String,
    "specialization":fields.String,
    "contact":fields.String
})

department_serializer = api.model("Department",{
    "id":fields.Integer,
    "name":fields.String,
    "services": fields.String,
    #"doctors": fields.Nested(doctor_serializer)
})

department_input_serializer = api.model("DepartmentInput",{
    "name":fields.String,
    "services":fields.String
})

assign_doctor_serializer = api.model("DepartmentAssign",{
    "doctor_id":fields.Integer
})

book_doctor_serializer = api.model("BookDoctor",{
    "doctor_id":fields.Integer
})

appointment_serializer = api.model("Appointment",{
    "doctor_id":fields.Integer,
    "patient_id":fields.Integer,
    "appointment_time":fields.String
})

patient_appointment_serializer = api.model("PatientAppointment",{
    "appointment_id":fields.Integer,
    "name":fields.String,
    "doctor_name":fields.String,
    "appointment_time":fields.String
})