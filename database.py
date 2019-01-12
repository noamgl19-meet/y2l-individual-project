from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('sqlite:///space.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def create_band(band_name, username, password):

    band = Bands(band_name = band_name, username = username, password = password)
    session.add(band)
    session.commit()
def query_by_username(username):
	band = session.query(Bands).filter_by(username = username).first()
	return band

def query_all_bands():
	bands = session.query(Bands).all()
	return bands
def query_all_band_members(username):
	members = session.query(Members).filter_by(band_name = username).all()
	return members
def create_member(member_name, instrument, band_name):
	member = Members(member_name = member_name, instrument = instrument, band_name = band_name)
	session.add(member)
	session.commit()
def query_all_members():
	members = session.query(Members).all()
	return members
def query_lyrics_by_username(username):
	lyrics = session.query(Lyrics).filter_by(band_name =username).all()
	return lyrics
def create_song(song_name, song_lyrics, member_name, band_name):
	time = str(datetime.datetime.now())
	song = Lyrics(song_name = song_name, song_lyrics = song_lyrics, member_name = member_name, band_name = band_name, time = time)
	session.add(song)
	session.commit()
def add_show(place, date, band_name):
	show = Shows(place = place, date = date, band_name = band_name)
	session.add(show)
	session.commit()

def query_all_band_shows(username):
	shows = session.query(Shows).filter_by(band_name = username).all()
	return shows
def adjust_instrument(member_name, instrument):

	member = session.query(Members).filter_by(member_name = member_name)
	
	member.instrument = instrument
	session.commit()

def add_song(member_name, name, link, band_name):
	song = Songs(member_name = member_name ,name = name, link = link, band_name = band_name)
	session.add(song)
	session.commit()

def query_all_band_records(username):
	songs = session.query(Songs).filter_by(band_name = username).all()
	return songs


# create_song("datura", "hello i am writing a story now so i can check line width, it should not take me so long to do, i think what i did so far is enough, by.", "noam", "datura")
