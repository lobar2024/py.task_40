import json
import logging

class LogMixin:
    def log(self, msg):
        logging.info(f"[{self.__class__.__name__}] {msg}")

class SerializeMixin:
    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, data):
        obj = cls.__new__(cls)
        obj.__dict__.update(json.loads(data))
        return obj

class ValidateMixin:
    def validate(self):
        for field, expected_type in getattr(self, '_types', {}).items():
            val = getattr(self, field, None)
            if not isinstance(val, expected_type):
                raise TypeError(f"{field} {expected_type.__name__} bo'lishi kerak")
        return True

class User(LogMixin, SerializeMixin, ValidateMixin):
    _types = {'name': str, 'age': int}

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.validate()
        self.log(f"Foydalanuvchi yaratildi: {name}")

class Product(LogMixin, SerializeMixin, ValidateMixin):
    _types = {'title': str, 'price': float}

    def __init__(self, title, price):
        self.title = title
        self.price = price
        self.validate()
        self.log(f"Mahsulot yaratildi: {title}")

u = User("Ali", 25)
print(u.to_json())

p = Product("Laptop", 999.99)
print(p.to_json())

u2 = User.from_json('{"name": "Vali", "age": 30}')
print(u2.name, u2.age)
