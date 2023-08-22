import pytest
from app import app, db, Employee
import json


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_create_employee(client):
    data = {
        'name': 'John Doe',
        'age': 30,
        'mobile_number': '1234567890',
        'designation': 'Engineer',
        'department': 'IT'
    }
    response = client.post('/api/v1/employee', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'employee' in response_data
    assert response_data['employee']['name'] == 'John Doe'


def test_create_employee_missing_field(client):
    # Negative test case for missing 'name' field
    data = {
        'age': 30,
        'mobile_number': '1234567890',
        'designation': 'Engineer',
        'department': 'IT'
    }
    response = client.post('/api/v1/employee', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400  # 400 Bad Request status code for missing field
    response_data = json.loads(response.data)
    assert 'error' in response_data
    assert response_data['error'] == "Missing 'name' field"


def test_get_employee_by_id(client):
    employee = Employee(name='John Doe', age=30, mobile_number='1234567890', designation='Engineer', department='IT')
    db.session.add(employee)
    db.session.commit()
    response = client.get(f'/api/v1/employee/{employee.id}')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'employee' in response_data
    assert response_data['employee']['name'] == 'John Doe'


def test_get_nonexistent_employee_by_id(client):
    # Negative test case for nonexistent employee ID
    nonexistent_id = 999  # Assume this ID does not exist
    response = client.get(f'/api/v1/employee/{nonexistent_id}')
    assert response.status_code == 404  # 404 Not Found status code
    response_data = json.loads(response.data)
    assert 'error' in response_data
    assert response_data['error'] == "Employee not found"


def test_update_employee_by_id(client):
    employee = Employee(name='John Doe', age=30, mobile_number='1234567890', designation='Engineer', department='IT')
    db.session.add(employee)
    db.session.commit()
    data = {
        'name': 'Jane Smith',
        'age': 35,
        'mobile_number': '9876543210',
        'designation': 'Senior Engineer',
        'department': 'Software Development'
    }
    response = client.put(f'/api/v1/employee/{employee.id}', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'employee' in response_data
    assert response_data['employee']['name'] == 'Jane Smith'


def test_delete_employee_by_id(client):
    employee = Employee(name='John Doe', age=30, mobile_number='1234567890', designation='Engineer', department='IT')
    db.session.add(employee)
    db.session.commit()
    response = client.delete(f'/api/v1/employee/{employee.id}')
    assert response.status_code == 204
    assert response.data == b''


def test_get_employee_personal_detail_by_id(client):
    response = client.get(f'/api/v1/employee-detail/1')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'employee_detail' in response_data
    assert response_data['employee_detail']['account number'] == '009091234554321'
    assert response_data['employee_detail']['ifcs code'] == '000XYZ1234'


def test_get_employee_personal_detail_by_id_mp(client, monkeypatch):
    def mock_get_employee_detail(id):
        return {
            "employee id": id,
            "name": "Mock Name",
            "account number": "0000000000000000",
            "ifcs code": "000000000",
            "pan number": "00000000000"
        }
    monkeypatch.setattr('employee_detail.details', mock_get_employee_detail(1))
    response = client.get(f'/api/v1/employee-detail/1')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'employee_detail' in response_data
    assert response_data['employee_detail']['account number'] == '0000000000000000'
    assert response_data['employee_detail']['name'] != 'Rahul Singh'
    assert response_data['employee_detail']['ifcs code'] == '000000000'
