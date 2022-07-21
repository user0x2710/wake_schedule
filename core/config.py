# flake8: noqa E501
import os
from typing import Dict, List

from pydantic import BaseModel, BaseSettings, RedisDsn


class WakeParkConfigModel(BaseModel):
    name: str
    reservation_url: str
    data_url: str
    date_field_name: str
    date_field_format: str
    data_field_key: str
    default_payload: Dict[str, str]
    headers: Dict[str, str]
    items: List[dict]


class Config(BaseSettings):
    NAME: str = "WakeSchedule"
    ENV: str = "development"
    DEBUG: bool = True
    REDIS_DSN: RedisDsn = 'redis://default:@localhost:6379/1'
    SHEDULE_ITEMS: Dict[str, WakeParkConfigModel] = {
        'wakeinn': {
            'name': 'WakeInn',
            'reservation_url': 'https://wakeinn.lt/rezervacija/',
            'data_url': 'https://wakeinn.lt/wp-admin/admin-ajax.php',
            'default_payload': {
                'action': 'get_timetable',
            },
            'date_field_name': 'data[date]',
            'data_field_key': 'body',
            'date_field_format': '%Y-%m-%d',
            'headers': {
                'authority': 'wakeinn.lt',
                'Accept': '*/*',
                'origin': 'https://wakeinn.lt',
                'referer': 'https://wakeinn.lt/rezervacija/',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
            'items': [
                {
                    'name': 'Wakeinn line 1',
                    'description': 'Two L-sized trampolines, Pipe-to-Pipe Bowl Stage, Rooftop 20m',
                    'extra_payload': {'data[id]': '24'}
                },
                {
                    'name': 'Wakeinn lane 2',
                    'description': 'Two M size trampolines, Flat Box 20m, Double Wave 20m',
                    'extra_payload': {'data[id]': '25'}
                },
                {
                    'name': 'Wakeinn lane 3',
                    'description': 'Beginner track without figures.',
                    'extra_payload': {'data[id]': '26'}
                }
            ]
        },
        'splash': {
            'name': 'Splash Cable Park',
            'reservation_url': 'https://wake.splash.lt/e-bilietas/',
            'data_url': 'https://wake.splash.lt/wp-admin/admin-ajax.php',
            'default_payload': {
                'action': 'get_timetable',
            },
            'date_field_name': 'data[date]',
            'date_field_format': '%Y-%m-%d',
            'data_field_key': 'body',
            'headers': {
                'authority': 'wake.splash.lt',
                'Accept': '*/*',
                'origin': 'https://wake.splash.lt',
                'referer': 'https://wake.splash.lt/e-bilietas/',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
            'items': [
                {
                    'name': 'Splash line 1',
                    'description': 'Two L size trampolines, Rail 2 Rail Transition',
                    'extra_payload': {'data[id]': '61'}
                },
                {
                    'name': 'Splash line 2',
                    'description': 'S size trampoline, M size trampoline, Fat Pipe 20m, Incline 8m, Nico 4',
                    'extra_payload': {'data[id]': '62'}
                },
            ]
        },
    }


class DevelopmentConfig(Config):
    DEBUG: str = True


class ProductionConfig(Config):
    DEBUG: str = False


def get_config():
    env = os.getenv("ENV", "development")
    config_type = {
        "development": DevelopmentConfig(),
        "production": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
