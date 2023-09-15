# Spotify Song Title Reader
## Description
tested only on obs 29 and python 3.7+

On start up the code reads the information about the application loaded and produces information about: 
- the current song: song name and artist
- the next song: song name and artist
- song progress
	- Max and Current Time Format
	- Max and Current Number

| Show/Hide	Events  | Description										|
| :---				| :---												|
| Pause				| show sources only when spotify is Paused			|
| Play				| show sources only when spotify is Playing			|
| Spotify Opened	| show sources only when the spotify app is Opened	|
| Spotify Unopened	| show sources only when spotify is not Opened		|

## Installation
just drop the [Stable Version](https://github.com/) into your OBS scripts (assuming you have connected your spotify)

if you havent done so prior download the follow from the requirements.txt with the command under the dependency section.

## Dependencies
If get this script run a cmd with the following code:

	pip install -r requirements.txt

or just download the components individually if you need to be extra

if you get an error with win32api, follow the guide here for your python and OS: https://github.com/mhammond/pywin32/releases



