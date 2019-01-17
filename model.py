from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.types import BINARY


Base = declarative_base()

#bands
class Bands(Base):
    __tablename__ = "bands"
    id = Column(Integer, primary_key = True)
    band_name = Column(String)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
    	message = "Band name: " + self.band_name + "\nUsername: " + self.username + "\nPassword: " + self.password
    	return message

#members
class Members(Base):
	__tablename__ = "members"
	id = Column(Integer, primary_key = True)
	member_name = Column(String)
	instrument = Column(String)
	band_name = Column(String)

	def __repr__(self):
		message = "Member name: " + self.member_name + "\nInstrument: " + self.instrument + "\nBand: " + self.band_name
		return message

#lyrics
class Lyrics(Base):
	__tablename__ = "lyrics"
	id = Column(Integer, primary_key = True)
	song_name = Column(String)
	song_lyrics = Column(String)
	member_name = Column(String)
	band_name = Column(String)
	time = Column(String)
	def __repr__(self):
		message = "\nSong name: " + self.song_name + "\nLyrics: " + self.song_lyrics + "\nWriter: " + self.member_name + "\nBand: " + self.band_name + "shared at: " + self.time
		return message

#preformances
class Shows(Base):
	__tablename__ = "shows"
	id = Column(Integer, primary_key = True)
	place = Column(String)
	date = Column(String)
	band_name = Column(String)

	def __repr__(self):
		message = "\nplace: " + self.place + "\ndate: " + self.date

#songs
class Songs(Base):
	__tablename__ = "songs"
	id = Column(Integer, primary_key = True)
	member_name = Column(String)
	name = Column(String)
	link = Column(String)
	band_name = Column(String)

class Tasks(Base):
	__tablename__ = "tasks"
	id = Column(Integer, primary_key = True)
	member_name = Column(String)
	name = Column(String)
	link = Column(String)
	band_name = Column(String)
	notes = Column(String)
	send_to = Column(String)

class Reply(Base):
	__tablename__ = "reply"
	id = Column(Integer, primary_key = True)
	member_name = Column(String)
	message = Column(String)
	time = Column(String)
	send_to = Column(String)
	band_name = Column(String)
	filename = Column(String)
