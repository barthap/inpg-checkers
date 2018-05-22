import configparser as cp
from typing import Any

from utils.constants import *
import utils.config as cfg
from pathlib import Path


__raw: cp.ConfigParser = None
__current = None


def locale_exists() -> bool:
	file = Path(LOCALE_FILE)
	return file.is_file()


def init():
	global __raw
	global __current
	if __raw is None:
		if locale_exists():
			__raw = __create_from_file()
		else:
			raise FileNotFoundError("Locale file " + LOCALE_FILE + " not found!")

	__current = str.upper(cfg.get('GENERAL', 'locale'))


def get(name: str) -> str:
	if not __loaded():
		init()

	return __raw[__current][name]


def __create_from_file() -> cp.ConfigParser:
	print("Loading locale from ", LOCALE_FILE)
	cfg = cp.ConfigParser()
	cfg.read(LOCALE_FILE)
	return cfg


def __loaded() -> bool:
	return __raw is not None
