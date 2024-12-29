# Forge


## Features

- Turn firestore documents to pydantic schemas automatically.

## Installation

Forge requires python to run, developed on python v3.10.

```sh
git clone https://github.com/yash-nait/Forge.git
cd Forge
pip install pipenv
pipenv install
```


## Use

Forge automatically picks the default firestore project you have set using gcloud cli on you system.

Create model for firestore document at path 'forgeCollection/forge_path'
```sh
python forge.py -dp "forgeCollection/forge_path"
```
This will create you model at model.py, if you want to specify the file and path use `-fp`
```sh
python forge.py -dp "forgeTestCollection/forge_test_document" -fp "my/path/my_model.py"
```
To have every field as optional use `-o`
```sh
python forge.py -dp "forgeTestCollection/forge_test_document" -fp "my/path/my_model.py" -o
```

### Example model

For a firstore document at path `forgeTestCollection/forge_test_document`, like:
```py
data = firestore.client().document(document_path).get().to_dict()
pprint(data)

# Output

{
    '_createdAt': DatetimeWithNanoseconds(2024, 12, 29, 19, 25, 18, 938561, tzinfo=datetime.timezone.utc),
    '_id': '1234',
    'address': {
        'city': 'Sample City',
        'geo': {'latitude': 40.7128, 'longitude': -74.006},
        'street': '123 Main St',
        'zipcode': '12345'
    },
    'age': 30,
    'contacts': [
        {'type': 'email', 'value': 'john.doe@example.com'},
        {'type': 'phone', 'value': '+1234567890'}
    ],
    'education': [
        {
            'degree': 'BSc Computer Science',
            'gpa': 3.8,
            'graduationYear': 2016,
            'institution': 'University A'
        },
        {
            'degree': 'MSc Data Science',
            'gpa': 3.9,
            'graduationYear': 2018,
            'institution': 'University B'
        }
    ],
    'height': 5.9,
    'isActive': True,
    'name': 'John Doe',
    'orderHistory': [
        {
            'orderDate': DatetimeWithNanoseconds(2023, 11, 15, 14, 30, tzinfo=datetime.timezone.utc),
            'orderId': '12345',
            'price': 1200.99,
            'product': 'Laptop',
            'quantity': 1,
            'status': 'shipped'
        },
        {
            'orderDate': DatetimeWithNanoseconds(2023, 12, 10, 10, 0, tzinfo=datetime.timezone.utc),
            'orderId': '12346',
            'price': 799.99,
            'product': 'Smartphone',
            'quantity': 2,
            'status': 'delivered'
        },
        {
            'orderDate': DatetimeWithNanoseconds(2023, 12, 25, 17, 45, tzinfo=datetime.timezone.utc),
            'orderId': '12347',
            'price': 150.75,
            'product': 'Wireless Headphones',
            'quantity': 1,
            'status': 'pending'
        }
    ],
    'profile': {
        'isAerified': False,
        'preferences': {
            'notifications': {'email': True, 'sms': False},
            'theme': 'dark'
        },
        'socialLinks': {
            'github': 'https://github.com/johndoe',
            'linkedin': 'https://linkedin.com/in/johndoe'
        }
    },
    'tags': ['developer', 'python', 'firebase']
}

```
Command 
```sh
python forge.py -dp "forgeTestCollection/forge_test_document" -o
```
will generate
```py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderHistory(BaseModel):

    orderDate: Optional[datetime] = None
    orderId: Optional[str] = None
    price: Optional[float] = None
    product: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None


class Education(BaseModel):

    degree: Optional[str] = None
    gpa: Optional[float] = None
    graduationYear: Optional[int] = None
    institution: Optional[str] = None


class SocialLinks(BaseModel):

    github: Optional[str] = None
    linkedin: Optional[str] = None


class Notifications(BaseModel):

    email: Optional[bool] = None
    sms: Optional[bool] = None


class Preferences(BaseModel):

    notifications: Optional[Notifications] = None
    theme: Optional[str] = None


class Profile(BaseModel):

    isAerified: Optional[bool] = None
    preferences: Optional[Preferences] = None
    socialLinks: Optional[SocialLinks] = None


class Contact(BaseModel):

    type: Optional[str] = None
    value: Optional[str] = None


class Geo(BaseModel):

    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Address(BaseModel):

    city: Optional[str] = None
    geo: Optional[Geo] = None
    street: Optional[str] = None
    zipcode: Optional[str] = None


class ForgeTestCollection(BaseModel):

    createdAt: Optional[datetime] = Field(None, alias="_createdAt")
    id: Optional[str] = Field(None, alias="_id")
    address: Optional[Address] = None
    age: Optional[int] = None
    contacts: Optional[list[Contact]] = None
    education: Optional[list[Education]] = None
    height: Optional[float] = None
    isActive: Optional[bool] = None
    name: Optional[str] = None
    orderHistory: Optional[list[OrderHistory]] = None
    profile: Optional[Profile] = None
    tags: Optional[list[str]] = None

```
## License

MIT

