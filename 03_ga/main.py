import pygamp as pg
import uuid
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

send_usd_rate = BlockingScheduler()


CLIENT_ID = str(uuid.uuid4())
PROPERTY_ID = 'UA-212228455-1'
NBU_API_URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'


def get_current_currency(currency):
    response = requests.get(url=NBU_API_URL)
    if response.status_code == 200:
        json_data = response.json()
        for currency_data in json_data:
            if currency_data['cc'] == currency:
                return int(currency_data['rate'] * 10000)
    else:
        return None


def send_currency_rate_event(currency):
    current_usd = get_current_currency(currency)

    if isinstance(current_usd, int):
        pg.event(
            cid=CLIENT_ID,
            property_id=PROPERTY_ID,
            category='Currency',
            action='Check currency ratio',
            label='USD',
            value=current_usd,
            non_interactive=1
        )
    else:
        print('Unable to get current currency ratio')


@send_usd_rate.scheduled_job('interval', minutes=1)
def send_usd_rate_func():
    send_currency_rate_event(currency='USD')


if __name__ == "__main__":
    send_usd_rate.start()
