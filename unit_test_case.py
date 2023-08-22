
import unittest
import json
from app import app, db, Employee


class EmployeeAPITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_employee(self):
        data = {
            'name': 'John Doe',
            'age': 30,
            'mobile_number': '1234567890',
            'designation': 'Engineer',
            'department': 'IT'
        }
        response = self.client.post('/api/v1/employee', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('employee', response_data)
        self.assertEqual(response_data['employee']['name'], 'John Doe')

    def test_create_employee_negative(self):
        data = {
            # 'age': 30,
            'name':'xyz',
            'mobile_number': '1234567890',
            'designation': 'Engineer',
            'department': 'IT'
        }
        response = self.client.post('/api/v1/employee', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # 400 Bad Request status code for validation failure
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        # self.assertEqual(response_data['error'], "Missing 'name' field")
        self.assertEqual(response_data['error'], "Missing 'age' field")

    def test_get_employee_by_id(self):
        employee = Employee(name='John Doe', age=30, mobile_number='1234567890', designation='Engineer', department='IT')
        db.session.add(employee)
        db.session.commit()
        response = self.client.get(f'/api/v1/employee/{employee.id}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('employee', response_data)
        self.assertEqual(response_data['employee']['name'], 'John Doe')

    def test_get_nonexistent_employee_by_id(self):
        # Negative test case for nonexistent employee ID
        nonexistent_id = 999  # Assume this ID does not exist
        response = self.client.get(f'/api/v1/employee/{nonexistent_id}')
        self.assertEqual(response.status_code, 404)  # 404 Not Found status code
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "Employee not found")

    def test_update_employee_by_id(self):
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
        response = self.client.put(f'/api/v1/employee/{employee.id}', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('employee', response_data)
        self.assertEqual(response_data['employee']['name'], 'Jane Smith')

    def test_delete_employee_by_id(self):
        employee = Employee(name='John Doe', age=30, mobile_number='1234567890', designation='Engineer', department='IT')
        db.session.add(employee)
        db.session.commit()
        response = self.client.delete(f'/api/v1/employee/{employee.id}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b'')

    def test_delete_nonexistent_employee_by_id(self):
        # Negative test case for deleting a nonexistent employee
        nonexistent_id = 999  # Assume this ID does not exist
        response = self.client.delete(f'/api/v1/employee/{nonexistent_id}')
        self.assertEqual(response.status_code, 404)  # 404 Not Found status code
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "Employee not found")


# Add more test cases for other API endpoints
if __name__ == '__main__':
    unittest.main()
