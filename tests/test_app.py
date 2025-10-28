import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test if home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    # Check that home page shows "No posts yet" or flash area
    assert b"<title>" in response.data or b"Posts" in response.data

def test_create_post_page(client):
    """Test if new post page loads successfully"""
    response = client.get('/post/new')
    assert response.status_code == 200
    # Check if page contains form elements
    assert b"<form" in response.data

def test_create_post_submission(client):
    """Test creating a post"""
    response = client.post(
        '/post/new',
        data={'title': 'Test Post', 'content': 'This is a test.'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Test Post" in response.data
