import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func

from app import create_app
from models import setup_db, Artwork, Medium

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + os.environ['CURATOR_TOKEN']
}

class AppTestCases(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_URI']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    POST /mediums
    '''
    def test_create_medium_valid_data(self):
        test_medium = {
            'title': 'Drawings',
        }
        total_before = len(Medium.query.all())
        response = self.client().post('/mediums', json=test_medium, headers=HEADERS)
        data = json.loads(response.data)
        total_after = len(Medium.query.all())
        # check response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        # check response body
        self.assertEqual(type(data['created']), int)
        # check database changes
        self.assertEqual(total_before + 1, total_after)

    def test_create_medium_invalid_data(self):
        test_medium = {}
        total_before = len(Medium.query.all())
        response = self.client().post('/mediums', json=test_medium, headers=HEADERS)
        data = json.loads(response.data)
        total_after = len(Medium.query.all())
        # check response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        # check response body
        self.assertEqual(type(data['message']), str)
        # check database changes
        self.assertEqual(total_before, total_after)

    def test_create_medium_unauth(self):
        test_medium = {}
        response = self.client().post('/mediums', json=test_medium)
        data = json.loads(response.data)
        # check response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    '''
    POST /artworks
    '''
    def test_create_artwork_valid_data(self):
        test_artwork = {
            'title': 'Lorem Ipsum',
            'medium': 'oil painting',
            'year': 2016,
            'image_link': 'https://i.picsum.photos/id/1056/3988/2720.jpg?hmac=qX6hO_75zxeYI7C-1TOspJ0_bRDbYInBwYeoy_z_h08',
            'medium_id': 2
        }
        total_before = len(Artwork.query.all())
        response = self.client().post('/artworks', json=test_artwork, headers=HEADERS)
        data = json.loads(response.data)
        total_after = len(Artwork.query.all())
        # check response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        # check response body
        self.assertEqual(type(data['created']), int)
        # check database changes
        self.assertEqual(total_before + 1, total_after)

    def test_create_artwork_invalid_data(self):
        test_artwork = {
            'title': 'Lorem Ipsum',
            'medium': 'oil painting',
            'year': '100'
        }
        total_before = len(Artwork.query.all())
        response = self.client().post('/artworks', json=test_artwork, headers=HEADERS)
        data = json.loads(response.data)
        total_after = len(Artwork.query.all())
        # check response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        # check response body
        self.assertEqual(type(data['message']), str)
        # check database changes
        self.assertEqual(total_before, total_after)

    def test_create_artwork_unauth(self):
        test_artwork = {
            'title': 'Lorem Ipsum',
            'medium': 'oil painting',
            'year': '100'
        }
        response = self.client().post('/artworks', json=test_artwork)
        data = json.loads(response.data)
        # check response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    '''
    GET /mediums
    '''
    def test_mediums(self):
        response = self.client().get('/mediums')
        data = json.loads(response.data)
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check response body
        self.assertEqual(type(data['mediums']), list)
    
    '''
    GET /artworks
    '''
    def test_artworks(self):
        response = self.client().get('/artworks')
        data = json.loads(response.data)
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check response body
        self.assertEqual(type(data['artworks']), list)

    '''
    PATCH /mediums/<int:medium_id>
    '''
    def test_update_medium_valid_id(self):
        test_id = 2
        medium = {
            'title': 'Mixed Media'
        }
        response = self.client().patch('/mediums/{}'.format(test_id), json=medium, headers=HEADERS)
        data = json.loads(response.data)        
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check response body
        self.assertEqual(type(data['updated']), int)
        # check response values
        self.assertEqual(data['updated'], test_id)

    def test_update_medium_invalid_id(self):
        test_id = 10000000
        medium = {}
        response = self.client().patch('/mediums/{}'.format(test_id), json=medium, headers=HEADERS)
        data = json.loads(response.data)        
        # check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        # check response body
        self.assertEqual(type(data['message']), str)

    def test_update_medium_unauth(self):
        test_id = 2
        medium = {
            'title': 'Mixed Media'
        }
        response = self.client().patch('/mediums/{}'.format(test_id), json=medium)
        data = json.loads(response.data)        
        # check response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    '''
    PATCH /artworks/<int:artwork_id>
    '''
    def test_update_artwork_valid_id(self):
        test_id = 1
        artwork = {
            "title": "Lorem Ipsum",
            "medium": "graphite drawing",
            "year": 2012,
            "image_link": "https://i.picsum.photos/id/103/2592/1936.jpg?hmac=aC1FT3vX9bCVMIT-KXjHLhP6vImAcsyGCH49vVkAjPQ",
            "medium_id": 2
        }
        response = self.client().patch('/artworks/{}'.format(test_id), json=artwork, headers=HEADERS)
        data = json.loads(response.data)        
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check response body
        self.assertEqual(type(data['updated']), int)
        # check response values
        self.assertEqual(data['updated'], test_id)

    def test_update_artwork_invalid_id(self):
        test_id = 10000000
        artwork = {
            "title": "Lorem Ipsum",
            "medium": "graphite drawing",
            "image_link": "https://i.picsum.photos/id/103/2592/1936.jpg?hmac=aC1FT3vX9bCVMIT-KXjHLhP6vImAcsyGCH49vVkAjPQ",
        }
        response = self.client().patch('/artworks/{}'.format(test_id), json=artwork, headers=HEADERS)
        data = json.loads(response.data)        
        # check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        # check response body
        self.assertEqual(type(data['message']), str)

    def test_update_artwork_unauth(self):
        test_id = 1
        artwork = {
            "title": "Lorem Ipsum",
            "medium": "graphite drawing",
            "image_link": "https://i.picsum.photos/id/103/2592/1936.jpg?hmac=aC1FT3vX9bCVMIT-KXjHLhP6vImAcsyGCH49vVkAjPQ",
        }
        response = self.client().patch('/artworks/{}'.format(test_id), json=artwork)
        data = json.loads(response.data)        
        # check response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
    
    '''
    GET /mediums/<int:medium_id>
    '''
    def test_read_medium_artworks_valid(self):
        test_id = 3
        response = self.client().get('/mediums/{}'.format(test_id))
        data = json.loads(response.data)
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check response body
        self.assertEqual(type(data['medium_id']), int)
        self.assertEqual(type(data['title']), str)
        self.assertEqual(type(data['artworks']), list)

    def test_read_medium_artworks_invalid(self):
        test_id = 1000000
        response = self.client().get('/mediums/{}'.format(test_id))
        data = json.loads(response.data)
        # check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        # check response body
        self.assertEqual(type(data['message']), str)

    '''
    GET /artworks/<int:artwork_id>
    '''
    def test_read_artwork_valid_id(self):
        test_id = 3
        response = self.client().get('/artworks/{}'.format(test_id))
        data = json.loads(response.data)        
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check response body
        self.assertEqual(type(data['artwork_id']), int)
        self.assertEqual(type(data['title']), str)
        self.assertEqual(type(data['medium']), str)
        self.assertEqual(type(data['year']), int)    
        self.assertEqual(type(data['image_link']), str)
        self.assertEqual(type(data['medium_id']), int)

    def test_read_artwork_invalid_id(self):
        test_id = 1000000
        response = self.client().get('/artworks/{}'.format(test_id))
        data = json.loads(response.data)        
        # check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        # check response body
        self.assertEqual(type(data['message']), str)

    '''
    DELETE /mediums/<int:medium_id>
    '''
    def test_delete_medium_valid_id(self):
        test_id = 5
        total_before = len(Medium.query.all())
        response = self.client().delete('/mediums/{}'.format(test_id), headers=HEADERS)
        data = json.loads(response.data)
        total_after = len(Medium.query.all())
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check response body
        self.assertEqual(data['deleted'], test_id)
        # check database changes
        self.assertEqual(total_before - 1, total_after)   

    def test_delete_medium_invalid_id(self):
        test_id = 1000000
        total_before = len(Medium.query.all())
        response = self.client().delete('/mediums/{}'.format(test_id), headers=HEADERS)
        data = json.loads(response.data)
        total_after = len(Medium.query.all())
        # check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        # check response body
        self.assertEqual(type(data['message']), str)
        # check database changes
        self.assertEqual(total_before, total_after)

    def test_delete_medium_unauth(self):
        test_id = 4
        response = self.client().delete('/mediums/{}'.format(test_id))
        data = json.loads(response.data)
        # check response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    '''
    DELETE /artworks/<int:artwork_id>
    '''
    def test_delete_artwork_valid_id(self):
        test_id = 2
        total_before = len(Artwork.query.all())
        response = self.client().delete('/artworks/{}'.format(test_id), headers=HEADERS)
        data = json.loads(response.data)
        total_after = len(Artwork.query.all())
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check response body
        self.assertEqual(data['deleted'], test_id)
        # check database changes
        self.assertEqual(total_before - 1, total_after)   

    def test_delete_artwork_invalid_id(self):
        test_id = 1000000
        total_before = len(Artwork.query.all())
        response = self.client().delete('/artworks/{}'.format(test_id), headers=HEADERS)
        data = json.loads(response.data)
        total_after = len(Artwork.query.all())
        # check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        # check response body
        self.assertEqual(type(data['message']), str)
        # check database changes
        self.assertEqual(total_before, total_after)

    def test_delete_artwork_unauth(self):
        test_id = 2
        response = self.client().delete('/artworks/{}'.format(test_id))
        data = json.loads(response.data)
        # check response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()