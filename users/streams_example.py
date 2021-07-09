from streams.Stream import Stream

users = [
            {
                "id": 1,
                "first_name": "Mandy",
                "last_name": "Gowan",
                "email": "mgowan0@aol.com",
                "gender": "Female",
                "loves": ['Soccer', 'Cricket', 'Golf'],
                "salary": 119885
            },
            {
                "id": 2,
                "first_name": "Janessa",
                "last_name": "Cotterell",
                "email": "jcotterell1@aol.com",
                "gender": "Female",
                "loves": ['Cricket'],
                "salary": 107629
            },
            {
                "id": 6,
                "first_name": "Jasen",
                "last_name": "Franzini",
                "email": "jfranzini5@aol.com",
                "gender": "Male",
                "loves": ['Soccer', 'Golf'],
                "salary": 78373
            }
        ]


def find_users_of_salary_greater_than_v0(minimum_salary):
    return (user for user in users if user['salary'] > minimum_salary)

def find_users_of_salary_greater_than(minimum_salary):
    salary_greater_than_minimum_salary = lambda user:user['salary'] > minimum_salary
    return (Stream.create(users)
                    .filter(salary_greater_than_minimum_salary)
                    .map(lambda user:user['name'])
                    .asList())


