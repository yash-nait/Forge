from datetime import datetime
import firebase_admin
from firebase_admin import firestore
from google.auth import default

from utils import get_user_confirmation, prompt_user

example_document_path: str = "forgeTestCollection/forge_test_document"

# Initialize Firestore client
cred, project = default()
firebase_admin.initialize_app(cred, {'projectId': project})

prompt_user(f"\n⚠️ Current selected project is `{project}`.", "RED")

prompt_user(f"\n⚠️ For this example a test document will be created at path `{example_document_path}`.", "RED")

get_user_confirmation("GRAY")

db = firestore.client()

# Create a sample document structure with various types of data
document_data = {
    '_createdAt': datetime.now(),  # Datetime object
    '_id': '1234',
    'name': 'John Doe',  # String
    'age': 30,  # Integer
    'height': 5.9,  # Float
    'isActive': True,  # Boolean
    'address': {  # Nested dictionary
        'street': '123 Main St',
        'city': 'Sample City',
        'zipcode': '12345',
        'geo': {  # Nested further
            'latitude': 40.7128,
            'longitude': -74.0060
        }
    },
    'contacts': [  # List of dictionaries (Array)
        {'type': 'email', 'value': 'john.doe@example.com'},
        {'type': 'phone', 'value': '+1234567890'}
    ],
    'tags': ['developer', 'python', 'firebase'],  # Array of strings
    'profile': {  # Nested dictionary with mixed data types
        'isAerified': False,
        'socialLinks': {
            'github': 'https://github.com/johndoe',
            'linkedin': 'https://linkedin.com/in/johndoe'
        },
        'preferences': {  # Nested further dictionary
            'theme': 'dark',
            'notifications': {'email': True, 'sms': False}
        }
    },
    'orderHistory': [  # List of dictionaries (Array of orders)
        {
            'orderId': '12345',
            'product': 'Laptop',
            'quantity': 1,
            'price': 1200.99,
            'orderDate': datetime(2023, 11, 15, 14, 30),
            'status': 'shipped'
        },
        {
            'orderId': '12346',
            'product': 'Smartphone',
            'quantity': 2,
            'price': 799.99,
            'orderDate': datetime(2023, 12, 10, 10, 0),
            'status': 'delivered'
        },
        {
            'orderId': '12347',
            'product': 'Wireless Headphones',
            'quantity': 1,
            'price': 150.75,
            'orderDate': datetime(2023, 12, 25, 17, 45),
            'status': 'pending'
        }
    ],
    'education': [  # List of dictionaries (Array of educational records)
        {
            'institution': 'University A',
            'degree': 'BSc Computer Science',
            'graduationYear': 2016,
            'gpa': 3.8
        },
        {
            'institution': 'University B',
            'degree': 'MSc Data Science',
            'graduationYear': 2018,
            'gpa': 3.9
        }
    ]
}

doc_ref = db.collection('forgeTestCollection').document('forge_test_document')
doc_ref.set(document_data)

prompt_user("""
-> Test Document created at path 'forgeTestCollection/forge_test_document' successfully!
""")
