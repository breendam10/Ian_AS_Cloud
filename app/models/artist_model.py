from app import db

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    biography = db.Column(db.Text)
    birth_date = db.Column(db.Date)

    # Relação 1-N com Artwork
    artworks = db.relationship('Artwork', back_populates='artist', cascade='all, delete-orphan', lazy=True)

    def __repr__(self) -> str:
        return f"<Artist {self.name!r}>"
