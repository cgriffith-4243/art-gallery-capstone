from flask import Flask, request, jsonify, redirect, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import setup_db, Artwork, Medium
from auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
  
    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.route('/')
    def index():
        return "Healthy."

    '''
    GET /mediums
    '''
    @app.route('/mediums', methods=['GET'])
    def mediums():
        try:
            all_mediums = [medium.format() for medium in Medium.query.all()]

            return jsonify({
                'success': True,
                'mediums': all_mediums
            }), 200
        except:
            abort(404)

    '''
    POST /mediums
    '''
    @app.route('/mediums', methods=['POST'])
    @requires_auth('post:medium')
    def create_mediums(payload):
        error = False
        form = request.get_json()
        # verify payload contains essential data
        title = form.get('title', None)

        if not title:
            abort(422)
        # attempt insertion of new entry
        try: 
            medium = Medium(
                title=title
            )
            medium.insert()
        except:
            error = True
        finally:
            if not error:
                return jsonify({
                    'success': True,
                    'created': medium.id,
                }), 201
            else:
                abort(422)
    
    '''
    GET /mediums/<int:medium_id>
    '''
    @app.route('/mediums/<int:medium_id>', methods=['GET'])
    def read_medium(medium_id):
        medium = Medium.query.get(medium_id)
        if medium:
            try:
                medium_artworks = [artwork.thumbnail() for artwork in Artwork.query.filter(Artwork.medium_id == medium_id).all()]

                return jsonify({
                    'success': True,
                    'medium_id': medium.id,
                    'title': medium.title,
                    'artworks': medium_artworks
                }), 200
            except:
                abort(404)
        abort(404)

    '''
    PATCH /medium/<int:medium_id>
    '''
    @app.route('/mediums/<int:medium_id>', methods=['PATCH'])
    @requires_auth('patch:medium')
    def update_medium(payload, medium_id):
        error = False
        form = request.get_json()
        # verify payload contains essential data
        title = form.get('title', False)
        # if entry with matching id is found, attempt updating attribute values
        medium = Medium.query.get(medium_id)
        if medium:
            try:
                # only update if payload value exists
                medium.title = title if title else medium.title
                medium.update()
            except:
                error = True
            finally:
                if not error:
                    return jsonify({
                        'success': True,
                        'updated': medium_id,
                    }), 200
                else:
                    abort(422)
        abort(404)

    '''
    DELETE /mediums/<int:medium_id>
    '''
    @app.route('/mediums/<int:medium_id>', methods=['DELETE'])
    @requires_auth('delete:medium')
    def delete_medium(payload, medium_id):
        error = False
        medium = Medium.query.get(medium_id)
        # if entry with matching id is found, attempt deletion
        if medium:
            try:
                medium.delete()
            except:
                error = True
            finally:
                if not error:
                    return jsonify({
                        'success': True,
                        'deleted': medium_id
                    }), 200
                else:
                    abort(422)
        else:
            abort(404)

    '''
    GET /artworks
    '''
    @app.route('/artworks', methods=['GET'])
    def artworks():
        try:
            all_artworks = [artwork.thumbnail() for artwork in Artwork.query.all()]

            return jsonify({
                'success': True,
                'artworks': all_artworks
            }), 200
        except:
            abort(404)
    
    '''
    POST /artworks
    '''
    @app.route('/artworks', methods=['POST'])
    @requires_auth('post:artwork')
    def create_artwork(payload):
        error = False
        form = request.get_json()
        # verify payload contains essential data
        title = form.get('title', None)
        medium = form.get('medium', None)
        year = form.get('year', None)
        image_link = form.get('image_link', None)
        medium_id = form.get('medium_id', None)

        if not (title and medium and year and image_link and medium_id):
            abort(422)
        # attempt insertion of new entry
        try: 
            artwork = Artwork(
                title=title,
                medium=medium,
                year=year,
                image_link=image_link,
                medium_id=medium_id
            )
            artwork.insert()
        except:
            error = True
        finally:
            if not error:
                return jsonify({
                    'success': True,
                    'created': artwork.id,
                }), 201
            else:
                abort(422)
    
    '''
    GET /artworks/<int:artwork_id>
    '''
    @app.route('/artworks/<int:artwork_id>', methods=['GET'])
    def read_artwork(artwork_id):
        artwork = Artwork.query.get(artwork_id)
        if artwork:
            return jsonify({
                'success': True,
                'artwork_id': artwork.id,
                'title': artwork.title,
                'medium': artwork.medium,
                'year': artwork.year,
                'image_link': artwork.image_link,
                'medium_id': artwork.medium_id
            }), 200
        abort(404)
    
    '''
    PATCH /artworks/<int:artwork_id>
    '''
    @app.route('/artworks/<int:artwork_id>', methods=['PATCH'])
    @requires_auth('patch:artwork')
    def update_artwork(payload, artwork_id):
        error = False
        form = request.get_json()
        # verify payload contains essential data
        title = form.get('title', False)
        medium = form.get('medium', False)
        year = form.get('year', False)
        image_link = form.get('image_link', False)
        medium_id = form.get('medium_id', False)
        # if entry with matching id is found, attempt updating attribute values
        artwork = Artwork.query.get(artwork_id)
        if artwork:
            try:
                # only update if payload value exists
                artwork.title = title if title else artwork.title
                artwork.medium = medium if medium else artwork.medium
                artwork.year = year if year else artwork.year
                artwork.image_link = image_link if image_link else artwork.image_link
                artwork.medium_id = medium_id if medium_id else artwork.medium_id

                artwork.update()
            except:
                error = True
            finally:
                if not error:
                    return jsonify({
                        'success': True,
                        'updated': artwork_id,
                    }), 200
                else:
                    abort(422)
        abort(404)

    '''
    DELETE /artworks/<int:artwork_id>
    '''
    @app.route('/artworks/<int:artwork_id>', methods=['DELETE'])
    @requires_auth('delete:artwork')
    def delete_artwork(payload, artwork_id):
        error = False
        artwork = Artwork.query.get(artwork_id)
        # if entry with matching id is found, attempt deletion
        if artwork:
            try:
                artwork.delete()
            except:
                error = True
            finally:
                if not error:
                    return jsonify({
                        'success': True,
                        'deleted': artwork_id
                    }), 200
                else:
                    abort(422)
        else:
            abort(404)

    ## Error Handling
    '''
    error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    '''
    error handling for resource not found
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''
    error handling for AuthError
    '''
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
                        "success": False, 
                        "error": error.status_code,
                        "message": error.error
                        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()