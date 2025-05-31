from datetime import date
from app import db
from . import exhibition_artwork

class Exhibition(db.Model):
    __tablename__ = 'exhibition'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text)
    date = db.Column(db.Date, default=date.today)

    # Relação N-N com Artwork
    artworks = db.relationship(
        'Artwork', secondary=exhibition_artwork,
        back_populates='exhibitions', lazy='subquery'
    )

    def __repr__(self) -> str:
        return f"<Exhibition {self.name!r} on {self.date}>"
