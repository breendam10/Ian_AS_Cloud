from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models import Exhibition, Artwork

exhibitions_ns = Namespace('exhibitions', description='Operações relacionadas a exposições')

exhibition_model = exhibitions_ns.model('Exhibition', {
    'id': fields.Integer(readonly=True, description='ID da exposição'),
    'name': fields.String(required=True, description='Nome da exposição'),
    'description': fields.String(description='Descrição da exposição'),
    'date': fields.Date(description='Data da exposição (YYYY-MM-DD)'),
    'artwork_ids': fields.List(fields.Integer, description='IDs das obras participantes')
})

@exhibitions_ns.route('/')
class ExhibitionList(Resource):
    @exhibitions_ns.marshal_list_with(exhibition_model)
    def get(self):
        """Lista todas as exposições"""
        expos = Exhibition.query.all()
        return [{
            'id': e.id,
            'name': e.name,
            'description': e.description,
            'date': e.date,
            'artwork_ids': [a.id for a in e.artworks]
        } for e in expos]

    @exhibitions_ns.expect(exhibition_model, validate=True)
    @exhibitions_ns.marshal_with(exhibition_model, code=201)
    def post(self):
        """Cria uma nova exposição"""
        data = exhibitions_ns.payload
        artworks = []
        for art_id in data.get('artwork_ids', []):
            art = Artwork.query.get(art_id)
            if not art:
                exhibitions_ns.abort(400, f'Obra com ID {art_id} não encontrada.')
            artworks.append(art)
        expo = Exhibition(
            name=data['name'],
            description=data.get('description'),
            date=data.get('date')
        )
        expo.artworks = artworks
        db.session.add(expo)
        db.session.commit()
        return {
            'id': expo.id,
            'name': expo.name,
            'description': expo.description,
            'date': expo.date,
            'artwork_ids': [a.id for a in expo.artworks]
        }, 201

@exhibitions_ns.route('/<int:id>')
@exhibitions_ns.param('id', 'ID da exposição')
@exhibitions_ns.response(404, 'Exposição não encontrada')
class ExhibitionResource(Resource):
    @exhibitions_ns.marshal_with(exhibition_model)
    def get(self, id):
        """Detalha uma exposição pelo ID"""
        expo = Exhibition.query.get_or_404(id)
        return {
            'id': expo.id,
            'name': expo.name,
            'description': expo.description,
            'date': expo.date,
            'artwork_ids': [a.id for a in expo.artworks]
        }

    @exhibitions_ns.expect(exhibition_model, validate=True)
    @exhibitions_ns.marshal_with(exhibition_model)
    def put(self, id):
        """Atualiza uma exposição"""
        expo = Exhibition.query.get_or_404(id)
        data = exhibitions_ns.payload
        expo.name = data['name']
        expo.description = data.get('description')
        expo.date = data.get('date')
        artworks = []
        for art_id in data.get('artwork_ids', []):
            art = Artwork.query.get(art_id)
            if not art:
                exhibitions_ns.abort(400, f'Obra com ID {art_id} não encontrada.')
            artworks.append(art)
        expo.artworks = artworks
        db.session.commit()
        return {
            'id': expo.id,
            'name': expo.name,
            'description': expo.description,
            'date': expo.date,
            'artwork_ids': [a.id for a in expo.artworks]
        }

    def delete(self, id):
        """Exclui uma exposição"""
        expo = Exhibition.query.get(id)
        if not expo:
            return {'message': f'Exposição com ID {id} não encontrada.'}, 404
        name = expo.name
        db.session.delete(expo)
        db.session.commit()
        return {'message': f'Exposição "{name}" removida com sucesso.'}, 200
