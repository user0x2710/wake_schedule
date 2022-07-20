
from datetime import datetime

import orjson
import requests
from app.celery import celery_app as app
from bs4 import BeautifulSoup
from celery import group
from core.config import config
from user_agent import generate_user_agent


@app.task()
def fetch_page(wp_id, item_index, date=None):
    settings = config.SHEDULE_ITEMS[wp_id]
    payload = settings.default_payload.copy()
    payload.update(settings.items[item_index]['extra_payload'])

    payload[settings.date_field_name] = (
        date or datetime.today().strftime(settings.date_field_format)
    )

    headers = settings.headers.copy()
    headers['user-agent'] = generate_user_agent()

    response = requests.post(
        settings.data_url,
        data=payload,
        headers=headers,
    )

    if response.status_code != requests.codes.ok:
        return None

    try:
        data = orjson.loads(response.content.decode('utf-8-sig'))
        return data[settings.data_field_key]
    except (KeyError, ValueError):
        return None


@app.task()
def parse_page(data):
    bs = BeautifulSoup(data, 'html.parser')

    timetable = []
    for item in bs.find_all('input'):
        time = item.attrs['data-time'].split(' - ')
        timetable.append({
            'timeStart': time[0],
            'timeEnd': time[1],
            'price': item.attrs['data-price'],
            'avaliable': 'disabled' not in item.attrs,
        })

    return timetable


@app.task()
def format_response(data, config):
    return {
        'name': config['name'],
        'description': config['description'],
        'timetable': data,
    }


def request_shedule(wp_id):
    tasks_groups = []
    for i_index, i_config in enumerate(config.SHEDULE_ITEMS[wp_id].items):
        chain = (
            fetch_page.s(wp_id, i_index) |
            parse_page.s() |
            format_response.s(i_config)
        )
        tasks_groups.append(chain)

    if tasks_groups:
        return group(*tasks_groups)
