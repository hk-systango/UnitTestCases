import json
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from employee_detail import get_employee_detail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root2:root@localhost:5432/employee_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Model
class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    mobile_number = db.Column(db.String(15))
    designation = db.Column(db.String(50))
    department = db.Column(db.String(50))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, age, mobile_number, designation, department):
        self.name = name
        self.age = age
        self.mobile_number = mobile_number
        self.designation = designation
        self.department = department

    def __repr__(self):
        return f"{self.id}"


db.create_all()


class EmployeeSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Employee
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    mobile_number = fields.String(required=True)
    designation = fields.String(required=True)
    department = fields.String(required=True)


@app.route('/api/v1/employee', methods=['GET'])
def get_employee():
    get_employees = Employee.query.all()
    employee_schema = EmployeeSchema(many=True)
    employees = employee_schema.dump(get_employees)
    return make_response(jsonify({"employees": employees}))


@app.route('/api/v1/employee/<id>', methods=['GET'])
def get_employee_by_id(id):
    employee = Employee.query.get(id)
    if employee:
        employee_schema = EmployeeSchema()
        employee = employee_schema.dump(employee)
    else:
        return make_response(jsonify({'error': 'Employee not found'}), 404)
    return make_response(jsonify({"employee": employee}))


@app.route('/api/v1/employee/<id>', methods=['PUT'])
def update_employee_by_id(id):
    data = request.get_json()
    get_employee = Employee.query.get(id)
    if data.get('name'):
        get_employee.name = data['name']
    if data.get('age'):
        get_employee.age = data['age']
    if data.get('mobile_number'):
        get_employee.mobile_number = data['mobile_number']
    if data.get('designation'):
        get_employee.designation = data['designation']
    if data.get('department'):
        get_employee.department = data['department']
    db.session.add(get_employee)
    db.session.commit()
    employee_schema = EmployeeSchema(only=['id', 'name', 'age', 'mobile_number', 'designation', 'department'])
    employee = employee_schema.dump(get_employee)
    return make_response(jsonify({"employee": employee}))


@app.route('/api/v1/employee/<id>', methods=['DELETE'])
def delete_employee_by_id(id):
    get_employee = Employee.query.get(id)
    if get_employee:
        db.session.delete(get_employee)
        db.session.commit()
    else:
        return make_response(jsonify({'error': 'Employee not found'}), 404)
    return make_response("", 204)


@app.route('/api/v1/employee', methods=['POST'])
def create_employee():
    data = request.get_json()
    employee_schema = EmployeeSchema()
    try:
        employee = Employee(name=data['name'], age=data['age'], mobile_number=data['mobile_number'],
                            designation=data['designation'], department=data['department'])
        created_employee = employee.create()
        result = employee_schema.dump(created_employee)
    except KeyError as key:
        return make_response(jsonify({"error": f'Missing {key} field'}), 400)
    return make_response(jsonify({"employee": result}), 201)


@app.route('/api/v1/employee-detail/<id>', methods=['GET'])
def get_employee_personal_detail_by_id(id):
    employee_detail = get_employee_detail(id)
    return make_response(jsonify({"employee_detail": employee_detail}))


if __name__ == "__main__":
    app.run(debug=True)
