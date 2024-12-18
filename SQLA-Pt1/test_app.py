import pytest
from app import app, db, User

# Setup the test client
@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

# Test home page redirect
def test_home_page_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.location == '/users'

# Test the /users page (show all users)
def test_show_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert b'Users' in response.data

# Test the /users/new page and form submission
def test_new_user(client):
    # Test the GET request
    response = client.get('/users/new')
    assert response.status_code == 200
    assert b'Add New User' in response.data
    
    # Test the POST request (creating a new user)
    response = client.post('/users/new', data={
        'first_name': 'Test',
        'last_name': 'User',
        'image_url': 'http://example.com'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Test User' in response.data

# Test the /users/<user_id> page (show single user)
def test_show_single_user(client):
    new_user = User(first_name="John", last_name="Doe", image_url="http://example.com")
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        user_in_db = db.session.get(User, new_user.id)
    
    response = client.get(f'/users/{user_in_db.id}')
    assert response.status_code == 200
    assert b'John' in response.data
    assert b'Doe' in response.data
