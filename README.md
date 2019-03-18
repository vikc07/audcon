# Audcon
A simple audio file converter

Audcon scans your media library and identify files that can be converted to another format to save space. A 
typical use case would be to convert flac files to mp3.

Audcon has scanner and converter services that run on a scheduled basis. Scanner service scans all the audio files 
and stores metadata in the database while queuing files with unsupported format for conversion. Converter service 
scans the queue and converts audio files.

### Requirements ###
* MySQL database is required to be pre-created. Use utf8mb4 charset
* ffprobe and ffmpeg are used for scanning and converting respectively. Ensure these programs are available locally 
and in the PATH variable

A Docker image is available with Audcon and ffmpeg/ffprobe pre-installed. You will still need mysql container

#### ---- Experimental Only ---- ####
Understand this is a very raw product. Therefore, use at own risk