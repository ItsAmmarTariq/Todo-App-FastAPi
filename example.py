class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age}, email={self.email})"

# Creating an instance of Person
person = Person(name="Alice", age=25, email="alice@example.com")

# Data to update the person object
update_data = {
    "name": "Updated Alice",
    "age": 26,
    "email": "updated_alice@example.com",
}

# Updating the person object using setattr
for key, value in update_data.items():
    setattr(person, key, value)

# Displaying the updated person object
print(person)
