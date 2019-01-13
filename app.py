from flask import Flask, render_template,send_from_directory, redirect, request, url_for, session as loging_session
from database import create_band, query_by_username, query_all_bands, query_all_band_members, create_member, query_all_members, query_lyrics_by_username, create_song, query_all_band_shows, add_show, adjust_instrument, add_song, query_all_band_records
import os
from werkzeug import secure_filename
import datetime


#constants
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])




#app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf movies'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



#Uploading a file:

@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
	if 'username' in loging_session:
		if 'member_name' in loging_session:
			username = loging_session['username']
			membername = loging_session['member_name']
			if request.method == 'POST':
				file = request.files['file']
				if file and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					add_song(membername, filename, url_for('uploaded_file', filename = filename), username)
				   	return redirect(url_for('audio'))
				else:
					return redirect(url_for('audio'))
			else:
				return redirect(url_for('audio'))

		else:
			return redirect(url_for('choose'))
	else:
		return redirect(url_for('login'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):

	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)



#all songs:
@app.route('/audio')
def audio():
	if 'username' in loging_session:
		if 'member_name' in loging_session:
			username = loging_session['username']
			membername = loging_session['member_name']
			songs = query_all_band_records(username)
			return render_template('audio.html', member = membername, songs = songs)
		else:
			return redirect(url_for('choose'))
	else:
		return redirect(url_for('login'))



#login
@app.route('/', methods=['POST', 'GET'])
def login():
	if request.method == 'GET'	:
		return render_template("login.html")
	else:
		username = request.form['username']
		password = request.form['password']

		bands = query_all_bands()
		is_match = False
		for band in bands:
			if band.username == username:
				if band.password == password:
					loging_session['username'] = username
					is_match = True
					members = query_all_band_members(username)
					if len(members) < 1:
						return render_template('add_member.html')
					else:
						return render_template("choose.html")
		if is_match == False:
			return render_template('login.html', msg = "not matching")
		

#register
@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == 'GET':
		return render_template("register.html")
	else:
		band_name = request.form['band_name']
		username = request.form['username']
		password = request.form['password']
		
		is_open = True
		bands = query_all_bands()

		#checking if no other band has the same username
		for band in bands:
			if band.username == username:
				is_open = False

		if is_open:
			create_band(band_name, username, password)
			return redirect(url_for('login'))
		else:
			return render_template("register.html", msg = "username is taken")

#selecting which member you are.
@app.route('/choose', methods = ['GET', 'POST'])
def choose():
	if 'username' in loging_session:
		username = loging_session['username']
		
		
		if request.method == 'GET':
			
			return render_template("choose.html")
		else:
			member_name = request.form['member_name']
			members = query_all_band_members(username)
			names = []
			for i in range(len(members)):
				names.append(members[i].member_name)

			if member_name in names:
				loging_session['member_name'] = member_name
				return redirect(url_for("home"))
			else:
				return redirect(url_for("choose"))
	else:
		return redirect(url_for('login'))

#adding a member
@app.route('/add_member', methods=['GET','POST'])
def add_member():
	if 'username' in loging_session:
		username = loging_session['username']
		if request.method == 'GET':
			return render_template("add_member.html")
		else:
			member_name = request.form['member_name']
			instrument = request.form['instrument']

			
			
			create_member(member_name, instrument, username)
			loging_session['member_name'] = member_name
			return redirect(url_for("home"))
	else:
		return render_template("login.html")

#home
@app.route('/home')
def home():
	if 'username' in loging_session:
		if 'member_name' in loging_session:
			username = loging_session['username']
			membername = loging_session['member_name']
		#begin
			lyrics = query_lyrics_by_username(username)










			return render_template('home.html', band_name = username, member = membername,lyrics = lyrics, reset = 0)
		#end
		else:
			return redirect(url_for('choose'))
	else:
		return redirect(url_for('login'))
		


@app.route('/logout')
def logout():
	loging_session.pop('username', None)
	loging_session.pop('member_name', None)
	return redirect(url_for('login'))



#lyrics
@app.route('/upload_songs', methods = ['GET','POST'])
def upload_songs():
	return "needs to be changed!"

#profile
@app.route('/profile', methods = ['GET','POST'])
def profile():
	if 'username' in loging_session:
		if 'member_name' in loging_session:
			username = loging_session['username']
			membername = loging_session['member_name']
			return render_template('profile.html', member = membername)
		else:
			return redirect(url_for('choose'))
	else:
		return redirect(url_for('login'))

#shows
@app.route('/shows', methods=['GET','POST'])
def upload_shows():
	if 'username' in loging_session:
		if 'member_name' in loging_session:
			username = loging_session['username']
			membername = loging_session['member_name']
			#begin

			if request.method == 'GET':
				shows = query_all_band_shows(username)
				return render_template('shows.html', shows = shows, member = membername)
			
			else:
				place = request.form['place']
				date = request.form['date']
				add_show(place,date,username)
				shows = query_all_band_shows(username)
				return render_template('shows.html', shows = shows, member = membername)






			#end
		else:
			return redirect(url_for('choose'))
	else:
		return redirect(url_for('login'))


#upload a song
@app.route('/upload_song', methods=['GET','POST'])
def upload_song():
	if 'username' in loging_session:
		if 'member_name' in loging_session:
			username = loging_session['username']
			membername = loging_session['member_name']
			#begin

			if request.method == 'GET':
				
				return render_template('lyrics.html', member = membername)
			
			else:
				song_name = request.form['song_name']
				song_lyrics = request.form['song_lyrics']
				create_song(song_name, song_lyrics, membername, username)
				return redirect(url_for('home'))






			#end
		else:
			return redirect(url_for('choose'))
	else:
		return redirect(url_for('login'))


@app.route('/control_panel', methods=['GET', 'POST'])
def control_panel():
	if "username" in loging_session:
		if "member_name" in loging_session:
			username = loging_session['username']
			membername = loging_session['member_name']
			#begin

			if request.method == "GET":

				return render_template("cp.html", member = membername)


			else:
				members = query_all_band_members(username)
				member_name = request.form['member_name']
				instrument = request.form['instrument']
				if len(member_name) < 4 or len(instrument) < 3:
					return render_template("cp.html", member = membername, msg = "invalid ditails: \nno way that a full name would contain less than 4 characters, or an instrument below 3 characters. \nplease re-enter.")

				for member in members:
					if member.member_name == member_name and member.instrument == instrument:
						return render_template("cp.html", member = membername, msg = "this member is already in the band")

					else:
						create_member(member_name, instrument, username)
				return render_template("cp.html", member = membername)
































			#end
		else:
			return render_template('choose.html')
	else:
		return render_template('login.html')


@app.route('/adjust', methods=['POST'])
def adjust():
	if "username" in loging_session:
		if "member_name" in loging_session:
			username = loging_session['username']
			membername = loging_session['member_name']

			if request.method == 'GET':

				render_template('cp.html', member = membername)


			else:

				member_name = request.form['member_name']
				instrument = request.form['instrument']
				if len(member_name) < 4 or len(instrument) < 3:
					return render_template("cp.html", member = membername, adjust_msg = "invalid ditails: \nno way that a full name would contain less than 4 characters, or an instrument below 3 characters. \nplease re-enter.")
				members = query_all_band_members(username)
				for member in members:
					if member.member_name == membername:
						adjust_instrument(member_name, instrument)
						return render_template('cp.html', member = membername, adjust_msg = membername + "'s instrument has been successfully changed to " + instrument)

				return render_template('cp.html', adjust_msg = "an unknown error has accured.", member = membername)

					











		else:
			return redirect(url_for('choose'))
	else:
		return redirect(url_for('login'))


#records
@app.route('/upload_record')
def upload_record():

	# file = request.files['input_file']


	# newFile = record(file.filename, file.read())
	
	return ' is saved to the database.'


if __name__ == '__main__':
	app.run(debug=True)

