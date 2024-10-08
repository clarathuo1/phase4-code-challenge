from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Define naming convention for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy with metadata
db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'  # Corrected to __tablename__

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  # Optional: Set nullable as per requirements
    super_name = db.Column(db.String, nullable=False)  # Optional: Set nullable as per requirements

    # Relationship to HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    # Association proxy to access powers directly
    powers = association_proxy("hero_powers", "power")

    # Serialization rules
    serialize_rules = ("-hero_powers.hero", "-hero_powers")

    def __repr__(self):  # Corrected to __repr__
        return f'<Hero {self.id}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'  # Corrected to __tablename__

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  # Optional: Set nullable as per requirements
    description = db.Column(db.String, nullable=False)  # Optional: Set nullable as per requirements

    # Relationship to HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    # Association proxy to access heroes directly
    heroes = association_proxy("hero_powers", "hero")

    # Serialization rules
    serialize_rules = ("-hero_powers.power", "-hero_powers")
    
    # Validation for description
    @validates('description')  # Removed db. prefix
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be present and at least 20 characters long")
        return description

    def __repr__(self):  # Corrected to __repr__
        return f'<Power {self.id}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'  # Corrected to __tablename__

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # Relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    # Serialization rules
    serialize_rules = ("-hero.hero_powers", "-power.hero_powers")
    
    # Validation for strength
    @validates('strength')  # Removed db. prefix
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Invalid strength value.")
        return strength

    def __repr__(self):  # Corrected to __repr__
        return f'<HeroPower {self.id}>'
