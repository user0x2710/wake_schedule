import os
from typing import Dict, List

from pydantic import BaseModel, BaseSettings, RedisDsn


class WakeParkConfigModel(BaseModel):
    name: str
    reservation_url: str
    date_field_name: str
    default_payload: Dict[str, str]
    headers: Dict[str, str]
    items: List[dict]

class Config(BaseSettings):
    NAME: str = "WakeSchedule"
    ENV: str = "development"
    DEBUG: bool = True
    REDIS_DSN: RedisDsn = 'redis://user:pass@localhost:6379/1'
    SHEDULE_ITEMS: Dict[str, WakeParkConfigModel] = {
        'wakeinn': {
            'name': 'WakeInn',
            'reservation_url': 'https://wakeinn.lt/rezervacija/',
            'default_payload': {
                'action': 'get_timetable',
            },
            'date_field_name': 'data[date]',
            'headers': {
                'authority': 'wakeinn.lt',
                'Accept': '*/*',
                'origin': 'https://wakeinn.lt',
                'referer': 'https://wakeinn.lt/rezervacija/',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
            'items': [
                {
                    'name': 'wakeinn line 1',
                    'description': '',
                    'extra_payload': {'data[id]': '24',}
                },
                {
                    'name': 'wakeinn lane 2',
                    'description': '',
                    'extra_payload': {'data[id]': '25',}
                }
            ]
        },
        'splash': {
            'name': 'Splash Cable Park',
            'reservation_url': 'https://wake.splash.lt/e-bilietas/',
            'default_payload': {
                'action': 'get_timetable',
            },
            'date_field_name': 'data[date]',
            'headers': {
                'authority': 'wake.splash.lt',
                'Accept': '*/*',
                'origin': 'https://wake.splash.lt',
                'referer': 'https://wake.splash.lt/e-bilietas/',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
            'items': [
                {
                    'name': 'Splash line',
                    'description': '',
                    'extra_payload': {'data[id]': '61',}
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
