import unittest
from app import app
import os
import json
import sqlite3

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_run_task_success(self):
        response = self.app.post('/run?task=count the number of Wednesdays in /data/dates.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task A3 executed successfully', response.get_data(as_text=True))

    def test_run_task_no_description(self):
        response = self.app.post('/run')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Task description is required', response.get_data(as_text=True))

    def test_read_file_success(self):
        # Create a temporary file for testing
        with open('test_file.txt', 'w') as f:
            f.write('Test content')

        response = self.app.get('/read?path=test_file.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'Test content')

        # Clean up the temporary file
        os.remove('test_file.txt')

    def test_read_file_not_found(self):
        response = self.app.get('/read?path=non_existent_file.txt')
        self.assertEqual(response.status_code, 404)
        self.assertIn('File not found', response.get_data(as_text=True))

    def test_task_a1(self):
        response = self.app.post('/run?task=install uv and run datagen')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task A1 executed successfully', response.get_data(as_text=True))

    def test_task_a2(self):
        response = self.app.post('/run?task=format /data/format.md using prettier')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task A2 executed successfully', response.get_data(as_text=True))

    def test_task_a3(self):
        with open('/data/dates.txt', 'w') as f:
            f.write('2023-10-11\n2023-10-18\n2023-10-25\n')
        response = self.app.post('/run?task=count the number of Wednesdays in /data/dates.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task A3 executed successfully', response.get_data(as_text=True))
        with open('/data/dates-wednesdays.txt', 'r') as f:
            self.assertEqual(f.read(), '3')

    def test_task_a4(self):
        contacts = [
            {"first_name": "John", "last_name": "Doe"},
            {"first_name": "Jane", "last_name": "Smith"},
            {"first_name": "Alice", "last_name": "Johnson"}
        ]
        with open('/data/contacts.json', 'w') as f:
            json.dump(contacts, f)
        response = self.app.post('/run?task=sort the array of contacts in /data/contacts.json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task A4 executed successfully', response.get_data(as_text=True))
        with open('/data/contacts-sorted.json', 'r') as f:
            sorted_contacts = json.load(f)
            self.assertEqual(sorted_contacts[0]['last_name'], 'Doe')
            self.assertEqual(sorted_contacts[1]['last_name'], 'Johnson')
            self.assertEqual(sorted_contacts[2]['last_name'], 'Smith')

    def test_task_a5(self):
        os.makedirs('/data/logs', exist_ok=True)
        for i in range(10):
            with open(f'/data/logs/log{i}.log', 'w') as f:
                f.write(f'Log entry {i}\n')
        response = self.app.post('/run?task=write the first line of the 10 most recent .log files')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task A5 executed successfully', response.get_data(as_text=True))
        with open('/data/logs-recent.txt', 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 10)
            self.assertEqual(lines[0], 'Log entry 9\n')

    def test_task_a6(self):
        os.makedirs('/data/docs', exist_ok=True)
        with open('/data/docs/doc1.md', 'w') as f:
            f.write('# Title 1\nContent 1\n')
        with open('/data/docs/doc2.md', 'w') as f:
            f.write('# Title 2\nContent 2\n')
        response = self.app.post('/run?task=extract the first occurrence of each H1 in /data/docs/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task A6 executed successfully', response.get_data(as_text=True))
        with open('/data/docs/index.json', 'r') as f:
            index = json.load(f)
            self.assertEqual(index['doc1.md'], 'Title 1')
            self.assertEqual(index['doc2.md'], 'Title 2')

    def test_task_a10(self):
        conn = sqlite3.connect('/data/ticket-sales.db')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS tickets")
        cursor.execute("CREATE TABLE tickets (type TEXT, units INTEGER, price REAL)")
        cursor.execute("INSERT INTO tickets (type, units, price) VALUES ('Gold', 10, 100.0)")
        cursor.execute("INSERT INTO tickets (type, units, price) VALUES ('Gold', 5, 150.0)")
        conn.commit()
        conn.close()
        response = self.app.post('/run?task=total sales of all the items in the “Gold” ticket type')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task A10 executed successfully', response.get_data(as_text=True))
        with open('/data/ticket-sales-gold.txt', 'r') as f:
            self.assertEqual(f.read(), '1750.0')

if __name__ == '__main__':
    unittest.main()
