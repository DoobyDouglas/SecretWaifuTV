from models import GoogleVoice
from const import MEDIA_ROOT
from utils import subs_reader
import reapy
from reapy import reascript_api as RPR
import time

path = 'D:/TEST/NINJA/04/1.ass'

text_list = subs_reader(path)
project = reapy.Project()
for i, sub in enumerate(text_list):
    voice = GoogleVoice('ru', sub.text.replace("\n", " "))
    voice.save_voice('D:/TEST/NINJA/04', sub.id)
    start = sub.start / 1000
    end = sub.end / 1000 - sub.start / 1000
    # if i > 0:
    #     if text_list[i].start == text_list[i - 1].end:
    #         end = end - 0.1
    project.cursor_position = start
    RPR.MoveEditCursor(end, True)
    time.sleep(1)
    RPR.InsertMedia(voice.file, 0 | 4)
    RPR.MoveEditCursor(- project.cursor_position, False)
