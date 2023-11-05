from qbittorrent import Client
import os
from data import update_or_get_parser_data
from const import NAME, LOCALHOST
import time
from gtts import gTTS
from const import MEDIA_ROOT
import os
import pysubs2
import ffmpeg
from ffmpeg._run import Error
from loguru import logger
import traceback
import re
from dataclasses import dataclass
import glob


def glob_path(folder: str, extension: str) -> list[str]:
    """Функция для получения пути к файлу"""
    return glob.glob(os.path.join(os.path.normpath(folder), extension))


class SubsEditor():

    def __init__(self, video_path: str) -> None:
        self.video_path = video_path
        self.__status = False
        self.__dot_ext = None

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def dot_ext(self):
        return self.__dot_ext

    @dot_ext.setter
    def dot_ext(self, dot_ext):
        self.__dot_ext = dot_ext

    @property
    def dialogs(self):
        return self.__sings_subs

    @dialogs.setter
    def dialogs(self, sings_subs):
        self.__sings_subs = sings_subs

    @staticmethod
    def comparator_signs(sub: str) -> bool:
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

    def subs_extract(self, dot_ext: str, mapping: str) -> str:
        """Функция для извлечения субтитров из видео"""
        try:
            input_file = ffmpeg.input(os.path.normpath(self.video_path))
            self.subs_path = f'{os.path.splitext(self.video_path)[0]}{dot_ext}'
            ffmpeg.run(ffmpeg.output(input_file, self.subs_path, map=mapping))
            self.status = True
            self.dot_ext = dot_ext
            self.subtitles = pysubs2.load(self.subs_path)
        except Error:
            logger.error(f'Ошибка: {traceback.format_exc()}')

    def delete_sings(self) -> None:
        """Функция для удаления из субтитров надписей"""
        to_delete = []
        for i, sub in enumerate(self.subtitles.events):
            if self.comparator_signs(sub.name.lower()):
                to_delete.append(i)
            elif self.comparator_signs(sub.name.lower()):
                to_delete.append(i)
        to_delete.sort()
        for i in reversed(to_delete):
            del self.subtitles[i]
        self.dialogs = (
            f'{os.path.splitext(self.subs_path)[0]}_dialogs{self.dot_ext}'
        )
        self.subtitles.save(self.dialogs)
        # self.subtitles = pysubs2.load(self.subs_path)
        # пока так
        os.remove(self.subs_path)


class Torrent:

    __slots__ = ('name', 'link', 'number', 'title')

    def __init__(self, name: str, link: str) -> None:
        self.name = name
        self.link = link
        self.number = None
        self.title = None

    def set_number_and_title(self, title: str) -> None:
        self.number = self.name.replace(title, '').split()[1]
        self.title = title

    def update_db(self, author: str) -> None:
        update_or_get_parser_data(author, self.name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


class Downloader:

    subs_editor = SubsEditor

    def __init__(self) -> None:
        self.client = Client(LOCALHOST)
        self.client.login('admin', '')

    def download(self, torrent: Torrent) -> str:
        data = update_or_get_parser_data(get=True)
        kwargs = {'link': torrent.link}
        if torrent.title in data['downloads']:
            path = f'{data["downloads"][torrent.title]}'f'/{torrent.number}'
            os.makedirs(path, exist_ok=True)
            kwargs['savepath'] = path
            self.client.download_from_link(**kwargs)
            return path
        # Обработать

    def remove_torrent(self, torrent: Torrent, path: str):
        time.sleep(1)
        flag = False
        while not flag:
            for i in self.client.torrents():
                if torrent.title.strip('?') in i['name']:
                    if i['progress'] != 1:
                        break
                    else:
                        self.client.delete(i['hash'])
                        flag = True
            time.sleep(3)
        self.__extract_subs(path)

    def __extract_subs(self, path):
        raws = glob_path((path), '*.mkv') + glob_path((path), '*.mp4')
        if len(raws) > 1:
            print('Много видео')
            return
        # Вынести язык в настройку
        lang = "rus"
        subs_editor = self.subs_editor(raws[0])
        # Вынести формат сабов в настройку
        subs_editor.subs_extract('.ass',  f'0:s:m:language:{lang}')
        if subs_editor.status:
            subs_editor.delete_sings()


class GoogleVoice:

    def __init__(self, lang: str, text: str) -> None:
        self.__lang = lang
        self.tts = gTTS(text, lang=self.lang)

    @property
    def lang(self) -> str:
        return self.__lang

    @lang.setter
    def lang(self, lang):
        self.__lang = lang

    def save_voice(self, path, number):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        self.file = f'{path}/voice_{number}.mp3'
        self.tts.save(self.file)


@dataclass
class Subtitle:
    id: int
    name: str
    text: str
    start: float
    end: float
