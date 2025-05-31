from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models import Artwork, Artist

artworks_ns = Namespace('artworks', description='Operações relacionadas a obras de arte')

artwork_model = artworks_ns.model('Artwork', {
    'id': fields.Integer(readonly=True, description='ID da obra'),
    'title': fields.String(required=True, description='Título da obra'),
    'description': fields.String(description='Descrição da obra'),
    'creation_date': fields.Date(description='Data de criação (YYYY-MM-DD)'),
    'image_url': fields.String(required=True, description='URL da imagem da obra'),
    'artist_id': fields.Integer(required=True, description='ID do artista'),
})

@artworks_ns.route('/')
class ArtworkList(Resource):
    @artworks_ns.marshal_list_with(artwork_model)
    def get(self):
        """Retorna a lista de todas as obras"""
        return Artwork.query.all()

    @artworks_ns.expect(artwork_model, validate=True)
    @artworks_ns.marshal_with(artwork_model, code=201)
    def post(self):
        """Cria uma nova obra de arte"""
        data = artworks_ns.payload
        # Valida se o artista existe
        artist = Artist.query.get(data['artist_id'])
        if not artist:
            artworks_ns.abort(400, 'Artista não encontrado.')
        artwork = Artwork(
            title=data['title'],
            description=data.get('description'),
            creation_date=data.get('creation_date'),
            image_url=data['image_url'],
            artist_id=data['artist_id']
        )
        db.session.add(artwork)
        db.session.commit()
        return artwork, 201

@artworks_ns.route('/<int:id>')
@artworks_ns.param('id', 'ID da obra')
class ArtworkResource(Resource):
    @artworks_ns.response(200, 'Obra encontrada')
    @artworks_ns.response(404, 'Obra não encontrada')
    @artworks_ns.marshal_with(artwork_model)
    def get(self, id):
        """Retorna uma obra pelo ID"""
        artwork = Artwork.query.get(id)
        if not artwork:
            return {'message': f'Obra com ID {id} não encontrada.'}, 404
        return artwork, 200

    @artworks_ns.expect(artwork_model, validate=True)
    @artworks_ns.response(200, 'Obra atualizada com sucesso')
    @artworks_ns.response(400, 'Artista não encontrado')
    @artworks_ns.response(404, 'Obra não encontrada')
    @artworks_ns.marshal_with(artwork_model)
    def put(self, id):
        """Atualiza uma obra existente"""
        artwork = Artwork.query.get(id)
        if not artwork:
            return {'message': f'Obra com ID {id} não encontrada.'}, 404
        data = artworks_ns.payload
        # Valida artista
        artist = Artist.query.get(data['artist_id'])
        if not artist:
            artworks_ns.abort(400, 'Artista não encontrado.')
        artwork.title = data['title']
        artwork.description = data.get('description')
        artwork.creation_date = data.get('creation_date')
        artwork.image_url = data['image_url']
        artwork.artist_id = data['artist_id']
        db.session.commit()
        return artwork

    @artworks_ns.response(200, 'Obra removida com sucesso')
    @artworks_ns.response(404, 'Obra não encontrada')
    def delete(self, id):
        """Exclui uma obra"""
        artwork = Artwork.query.get(id)
        if not artwork:
            return {'message': f'Obra com ID {id} não encontrada.'}, 404
        title = artwork.title
        db.session.delete(artwork)
        db.session.commit()
        return {'message': f'Obra "{title}" removida com sucesso.'}, 200
