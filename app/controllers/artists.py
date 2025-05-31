from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models import Artist

artists_ns = Namespace('artists', description='Operações relacionadas a artistas')

artist_model = artists_ns.model('Artist', {
    'id': fields.Integer(readonly=True, description='ID do artista'),
    'name': fields.String(required=True, description='Nome do artista'),
    'biography': fields.String(description='Biografia do artista'),
    'birth_date': fields.Date(description='Data de nascimento (YYYY-MM-DD)'),
})

@artists_ns.route('/')
class ArtistList(Resource):
    @artists_ns.marshal_list_with(artist_model)
    def get(self):
        """Retorna a lista de todos os artistas"""
        return Artist.query.all()

    @artists_ns.expect(artist_model, validate=True)
    @artists_ns.marshal_with(artist_model, code=201)
    def post(self):
        """Cria um novo artista"""
        data = artists_ns.payload
        artist = Artist(
            name=data['name'],
            biography=data.get('biography'),
            birth_date=data.get('birth_date')
        )
        db.session.add(artist)
        db.session.commit()
        return artist, 201

@artists_ns.route('/<int:id>')
@artists_ns.param('id', 'ID do artista')
class ArtistResource(Resource):
    @artists_ns.response(200, 'Artista encontrado')
    @artists_ns.response(404, 'Artista não encontrado')
    @artists_ns.marshal_with(artist_model)
    def get(self, id):
        """Retorna um artista pelo ID"""
        artist = Artist.query.get(id)
        if not artist:
            artists_ns.abort(404, message=f'Artista com ID {id} não encontrado.')
        return artist, 200

    @artists_ns.expect(artist_model, validate=True)
    @artists_ns.response(200, 'Artista atualizado com sucesso')
    @artists_ns.response(404, 'Artista não encontrado')
    @artists_ns.marshal_with(artist_model)
    def put(self, id):
        """Atualiza um artista existente"""
        artist = Artist.query.get(id)
        if not artist:
            artists_ns.abort(404, message=f'Artista com ID {id} não encontrado.')
        data = artists_ns.payload
        artist.name = data['name']
        artist.biography = data.get('biography')
        artist.birth_date = data.get('birth_date')
        db.session.commit()
        return artist

    def delete(self, id):
        """Exclui um artista"""
        artist = Artist.query.get(id)
        if not artist:
            artists_ns.abort(404, message=f'Artista com ID {id} não encontrado.')
        name = artist.name
        db.session.delete(artist)
        db.session.commit()
        return {'message': f'Artista "{name}" removido com sucesso.'}, 200
