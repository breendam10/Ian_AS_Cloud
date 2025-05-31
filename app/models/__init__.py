# C:\Users\ianes\Desktop\AS-Cloud\app\models\__init__.py

from app import db

# Associação N-N entre exposições e obras
exhibition_artwork = db.Table(
    'exhibition_artwork',
    db.Column('exhibition_id', db.Integer, db.ForeignKey('exhibition.id'), primary_key=True),
    db.Column('artwork_id',     db.Integer, db.ForeignKey('artwork.id'),     primary_key=True)
)

# Importa os modelos individuais
from .user_model       import User
from .artist_model     import Artist
from .artwork_model    import Artwork
from .exhibition_model import Exhibition

# Chaves públicas do pacote
__all__ = [
    'User',
    'Artist',
    'Artwork',
    'Exhibition',
    'exhibition_artwork'
]
