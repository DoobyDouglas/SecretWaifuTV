from typing import List, Tuple, Dict
from tkinter import filedialog
from ffmpeg._run import Error
from models import Subtitle
import tkinter.messagebox
import asstosrt
import pysubs2
import tkinter
import ffmpeg
import glob
import sys
import re
import os


def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, path)


def glob_path(folder: str, extension: str) -> List[str]:
    """Функция для получения пути к файлу"""
    return glob.glob(os.path.join(os.path.normpath(folder), extension))


def ass_sub_convert(folder: str, subs: List[str]) -> None:
    """Функция для конвертирования ass субтитров"""
    with open(subs[0], 'r', encoding='utf-8') as ass_file:
        srt_sub = asstosrt.convert(ass_file)
    with open(f'{folder}/subs.srt', 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_sub)
    os.remove(os.path.join(subs[0]))


def comparator(sub: str) -> bool:
    """Функция для проверки субтитра"""
    if (
        'text' in sub
        or 'sign' in sub
        or 'надпись' in sub
        or 'caption' in sub
        or ('title' in sub and 'subtitle' not in sub)
        or 'song' in sub
        or 'screen' in sub
        or 'typedigital' in sub
        or 'phonetics' in sub
    ):
        return True
    return False


def subs_edit(subs: List[str], flag: str) -> None:
    """Функция для удаления из субтитров надписей и песен"""
    subtitles = pysubs2.load(subs[0])
    if flag == 'srt':
        pattern_1 = r'\((.*?)\)'
        pattern_2 = r'\[.*?]$'
        pattern_3 = '♫'
        pattern_4 = '♪'
        to_delete = [
            i for i, line in enumerate(subtitles) if (
                re.match(pattern_1, line.text)
                or re.match(pattern_2, line.text)
                or pattern_3 in line.text
                or pattern_4 in line.text
            )
        ]
    elif flag == 'ass':
        to_delete = []
        for i, sub in enumerate(subtitles.events):
            if comparator(sub.name.lower()):
                to_delete.append(i)
            elif comparator(sub.name.lower()):
                to_delete.append(i)
    to_delete.sort()
    for i in reversed(to_delete):
        del subtitles[i]
    subtitles.save(subs[0])


def subs_reader(path: str) -> list[str]:
    subtitles = pysubs2.load(path)
    subs_list = []
    for i, sub in enumerate(subtitles.events):
        subs_list.append(Subtitle(i, sub.name, sub.text, sub.start, sub.end))
    return subs_list


if __name__ == '__main__':
    pass
