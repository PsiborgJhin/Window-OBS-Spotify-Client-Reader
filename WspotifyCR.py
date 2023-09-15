import re
import psutil
import obspython as obs
import pywinauto
from pywinauto import Application

from time import sleep as s

NO_SOURCE_SELECTED = "--No Source Selected--"

#the sources managed by these individual events
sources_spotify_opened              = [NO_SOURCE_SELECTED]
sources_spotify_unopened            = [NO_SOURCE_SELECTED]
sources_pause                       = [NO_SOURCE_SELECTED]
sources_play                        = [NO_SOURCE_SELECTED]
#the value shown for the sources shown if only a text source
text_source_value_spotify_opened    = ""
text_source_value_spotify_unopened  = ""
text_source_value_pause             = ""
text_source_value_play              = ""
#variables that are displayable to text source values
curr_song_name                      = ""
curr_song_artist                    = ""
next_song_name                      = ""
next_song_artist                    = ""
curr_progress_time                  = ""
curr_progress_number                = ""
max_progress_time                   = ""
max_progress_number                 = ""
playlist_name                       = ""



class SpotifyNonExistent(Exception):
  pass

class WindowsSpotifyClientReader:
    def __init__(self):
        self.curr_song_name_element = None
        self.curr_song_artist_element = None
        self.next_song_name_element = None
        self.next_song_artist_element = None
        self.spotify = Application(None)
        self.spotifyProcess = psutil.Process(None)
        self.progress_slider = None
        self.song_info_parent = None
        self.paused = False
        self.play = False

    def set_current_song_info_element(self, element):
        try:
            self.curr_song_name_element     = element.descendants()[6]     #playing current song index
            self.curr_song_artist_element   = element.descendants()[7]     #playing current artist index
        except:
            obs.timer_add() # adds this method to the timer if spotify is launched in order to load the variable
            return

    def set_next_song_info_element(self, element):
        try:
            self.curr_song_name_element   = element.descendants()[-2]     #playing Now song
            self.curr_song_artist_element = element.descendants()[-1]     #playing now artist
        except:
            obs.timer_add() # adds this method to the timer if spotify is launched in order to load the variable
            return

    def get_spotify(self):
        try:
            maxThread = 0
            for proc in psutil.process_iter():
                if proc.name() == 'Spotify.exe' and proc.num_threads() > self.spotifyProcess.num_threads():
                    self.spotifyProcess = proc
                    maxThread=proc.num_threads()
                    print("new method: pid: {pid} | num_thread: {num_thread}".format( pid=self.spotifyProcess.pid, num_thread=self.spotifyProcess.num_threads()))
            if self.spotifyProcess == psutil.Process(None):
                raise SpotifyNonExistent("Launch Spotify")
            return self.spotifyProcess
        except SpotifyNonExistent as exp:
            print("Start Spotify To Continue")

    def update_playback_events(self):
        self.paused  = True if "Spotify" in self.spotify.window_text() else "" 
        self.play    = True if "Spotify" not in self.spotify.window_text() else ""
    
    def spotify_element_setup(self):
        try:
            self.spotifyProcess = self.get_spotify()
        except:
            obs.timer_add() # Spotify isnt lauched and will be searched for
            return
        
        self.spotify=Application(backend='uia').connect(process=self.spotifyProcess.pid)

        #if opened
        self.paused  = True if "Spotify" in spotify.window_text() else "" 
        self.play    = True if "Spotify" not in spotify.window_text() else ""

        self.song_info_parent = self.spotify.top_window().descendants(title="Now Playing View", control_type="Group")
        self.set_current_song_info_element(self.song_info_parent)
        self.set_next_song_info_element(self.song_info_parent)

        self.progress_slider=self.spotify.top_window().descendants(title="Change progress", control_type="Slider")
        self.max_slider_val = self.progress_slider.max_value()
        self.curr_slider_val = self.progress_slider.value()
        sliderTimes= []
        for element in self.progress_slider.parent().descendants(control_type="Text").filter():
            if re.match(r"([0-9]+\:)+[0-9]{2}", element.window_text()) and element.parent().friendly_class_name() == "GroupBox":
                sliderTimes.append(element)
        

wscr = WindowsSpotifyClientReader()

def script_description():
        return 'Variables:\n{curr_song_name}\n{curr_song_artist}\n{next_song_name}\n{next_song_artist}\n'

def script_load(settings): #adds the 
    obs.timer_add(wscr.spotify_variable_setup,5000)

def script_update(settings):
    global source_to_toggle, invert_bool
    source_display = obs.obs_data_get_string(settings, "source_select_list")
    if source_display == "":
        source_display = None
    hide_on_error = obs.obs_data_get_bool(settings, "hide_on_error")

def script_properties():
    props = obs.obs_properties_create()
    drop_list = obs.obs_properties_add_list(props, "source_select_list", "Song Source", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_add_string(drop_list, "", "")
    sources = obs.obs_enum_sources()
    for src in sources:
        obs.obs_property_list_add_string(drop_list, obs.obs_source_get_name(src), obs.obs_source_get_name(src))
    obs.source_list_release(sources)
    song_template = obs.obs_properties_add_text(props, "song_format", "Song Text Display", obs.OBS_TEXT_DEFAULT)
    hide_error_check = obs.obs_properties_add_bool(props, "hide_on_error", "Hide Source On Error")
    return props