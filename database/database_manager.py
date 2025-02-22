from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.engine = create_engine(config['DATABASE_URL'], echo=config['DEBUG_MODE']=='true')  # echo=True logs SQL for debugging
        self.base = declarative_base()
        self.define_models()
        # Create tables
        self.base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)

    def define_models(self):
        # Player specific models
        player_inventory = Table('player_inventory', self.base.metadata,
            Column('player_id', Integer, ForeignKey('players.id'), primary_key=True),
            Column('item_id', Integer, ForeignKey('items.id'), primary_key=True)
        )

        class Player(self.base):
            __tablename__ = 'players'
            id = Column(Integer, primary_key=True)
            name = Column(String(50), nullable=False)
            discord_id = Column(String(50), unique=True, nullable=False)
            current_room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
            current_room = relationship("Room")
            inventory = relationship("Item", secondary=player_inventory)

        class Room(self.base):
            __tablename__ = 'rooms'
            id = Column(Integer, primary_key=True)
            name = Column(String(50), nullable=False)
            description = Column(String(255), nullable=False)
            exits = relationship("Exit", back_populates="room")

        class Exit(self.base):
            __tablename__ = 'exits'
            id = Column(Integer, primary_key=True)
            direction = Column(String(10), nullable=False)
            room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
            target_room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
            room = relationship("Room", foreign_keys=[room_id], back_populates="exits")
            target_room = relationship("Room", foreign_keys=[target_room_id])

        class Item(self.base):
            __tablename__ = 'items'
            id = Column(Integer, primary_key=True)
            name = Column(String(50), nullable=False)
            description = Column(String(255), nullable=False)
            room_id = Column(Integer, ForeignKey('rooms.id'), nullable=True)
            room = relationship("Room")