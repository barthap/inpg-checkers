import configparser as cp
from typing import Any

from utils.constants import *
from pathlib import Path


__cfg: cp.ConfigParser = None


def config_exists() -> bool:
	file = Path(CONFIG_FILE)
	return file.is_file()


def locale_exists() -> bool:
	file = Path(LOCALE_FILE)
	return file.is_file()


def save():
	global __cfg
	with open(CONFIG_FILE, 'w') as file:
		__cfg.write(file)


def init():
	global __cfg
	if __cfg is None:
		if config_exists():
			__cfg = __create_from_file()
		else:
			__cfg = __create_default_cfg()
			save()


def get(group: str, prop: str=None) -> Any:
	if not __loaded():
		init()

	if prop is None:
		return __cfg[group]

	return __cfg[group][prop]


def __create_default_cfg() -> cp.ConfigParser:
	print("File not found, creating new config")
	cfg = cp.ConfigParser()
	cfg['GENERAL'] = {}
	gen = cfg['GENERAL']
	gen['locale'] = 'en'
	gen['StartPieceRows'] = '3'
	return cfg


def __create_from_file() -> cp.ConfigParser:
	print("Loading config from ", CONFIG_FILE)
	cfg = cp.ConfigParser()
	cfg.read(CONFIG_FILE)
	return cfg


def __loaded() -> bool:
	return __cfg is not None
