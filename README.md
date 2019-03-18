# Audcon
A simple audio file converter

Audcon scans your media library and identifies files that can be converted to another format to save space. A 
typical use case would be to convert flac files to mp3.

Audcon has scanner and converter services that run on a scheduled basis. Scanner service scans all the audio files 
and stores metadata in the database while queuing files with unsupported format for conversion. Converter service 
scans the queue and converts audio files.

### Requirements ###
1. MySQL Server v8.x
2. `ffmpeg` and `ffprobe` installed locally with commands available in the `PATH` variable

### Installation ###
1. Clone the git repository to local machine
2. Create MySQL Database and tables using `database.sql` file prior to running. Edit the user/pass in the script as 
needed
3. Execute `run.sh` to start the internal server
4. Access the web ui at `http://server:5000`. First time you run it will ask for changing settings

Alternatively, a [Docker image](https://cloud.docker.com/repository/docker/vikramchauhan/audcon) is available with 
Audcon and ffmpeg/ffprobe pre-installed. You will still need MySQL 
container.

#### ---- Experimental Only ---- ####
Understand this is a very raw product. Therefore, use at own risk