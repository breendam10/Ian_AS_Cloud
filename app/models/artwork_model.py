from datetime import date
from app import db
from . import exhibition_artwork

class Artwork(db.Model):
    __tablename__ = 'artwork'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    creation_date = db.Column(db.Date, default=date.today)
    image_url = db.Column(db.String(200), nullable=False)

    # Relação 1-N com Artist
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete='CASCADE'), nullable=False)
    artist = db.relationship('Artist', back_populates='artworks', lazy=True)

    # Relação N-N com Exhibition via tabela de associação
    exhibitions = db.relationship(
        'Exhibition', secondary=exhibition_artwork,
        back_populates='artworks', lazy='subquery'
    )

    def __repr__(self) -> str:
        return f"<Artwork {self.title!r} by {self.artist.name!r}>"
