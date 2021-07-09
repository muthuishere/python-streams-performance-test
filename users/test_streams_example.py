from unittest import TestCase

from users.streams_example import find_users_of_salary_greater_than


class Test(TestCase):
    def test_find_users_of_salary_greater_than(self):
        results = find_users_of_salary_greater_than(100000)
        print(results)
        self.assertIn({
                "id": 1,
                "first_name": "Mandy",
                "last_name": "Gowan",
                "email": "mgowan0@aol.com",
                "gender": "Female",
                "loves": ['Soccer', 'Cricket', 'Golf'],
                "salary": 119885
            },results)
        self.assertIn({
                "id": 2,
                "first_name": "Janessa",
                "last_name": "Cotterell",
                "email": "jcotterell1@aol.com",
                "gender": "Female",
                "loves": ['Cricket'],
                "salary": 107629
            },results)


