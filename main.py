from config import get_config, write_config
from loguru import logger
import locale
from models import Downloader
from parse import parse_erai_raws_or_subsplease, parse_nyaapantsu_xml
import traceback
from const import SLEEP_TIME, NAME
import time


def parse():
    # while get_config()['USER'].getboolean('status'):
    #     try:
    downloader = Downloader()
    locale.setlocale(locale.LC_TIME, 'en_US')
    parse_erai_raws_or_subsplease('erai_raws', downloader)
            # parse_erai_raws_or_subsplease('subsplease', downloader)
            # parse_nyaapantsu_xml('nyaapantsu', downloader)
        # except Exception:
        #     logger.error(f'Ошибка: {traceback.format_exc()}')
        # finally:
        #     time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    logger.add(f'{NAME.upper()}.log', encoding='utf-8')
    parse()
