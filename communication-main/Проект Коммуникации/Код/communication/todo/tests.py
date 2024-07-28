from django.test import TestCase

# Create your tests here.

class TestToDo(TestCase):
    
    def test_layout(self):
        response = self.client.get('/todo/')
        self.assertEqual(response.status_code, 200)

    def test_new_note(self):
        response = self.client.get('/todo/').content.decode()
        print(response)
