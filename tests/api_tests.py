"""Super simple script that hits the api endpoints with CRUD commands."""
import requests
import datetime
import pytz
import json
import logging
import argparse

logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

TZ = pytz.timezone('US/Pacific')


def create():
    """Create a couple of entries in the db.

    Choice of state: (('TD', 'todo'), ('IP', 'in-progress'), ('DN', 'done'))

    :return: None
    :rtype: None
    """
    logger.info("Creating Todo entries")
    resp = requests.post(
        url=API_ENDPOINT,
        json={
            'text': 'minimum amount of data needed to create entry'
        }
    )
    resp.raise_for_status()

    resp = requests.post(
        url=API_ENDPOINT,
        json={
            'text': 'This will create a "todo" state',
            'due_at': str(datetime.datetime(year=2018, month=11, day=25, hour=8, minute=12))
        }
    )
    resp.raise_for_status()

    resp = requests.post(
        url=API_ENDPOINT,
        json={
            'text': 'And this is in-progress',
            'state': 'IP',
            'due_at': str(datetime.datetime(year=2018, month=11, day=30, hour=10, minute=12))
        }
    )
    resp.raise_for_status()

    failed_resp = requests.post(
        url=API_ENDPOINT,
        json={
            'text': 'Gotta have those dates right though',
            'state': 'IP',
            'due_at': '2018-11-9001 10:12:00'
        }
    )
    expected_err = {"due_at":["Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."]}
    assert json.loads(failed_resp.text) == expected_err


def retrieve():
    """Fetch the list of entries from the db.

    :return: None
    :rtype: None
    """
    logger.info("Fetching Todo entries")
    # all
    resp = requests.get(
        url="{}fetch_all".format(API_ENDPOINT)
    )
    resp.raise_for_status()
    all_items = resp.json()
    assert len(all_items) > 2

    # single
    id_to_fetch = all_items[0]['id']
    resp = requests.get(
        url="{}{}".format(API_ENDPOINT, id_to_fetch)
    )
    resp.raise_for_status()
    single_item = resp.json()
    assert isinstance(single_item, dict) and single_item['id'] == id_to_fetch

    # paginated
    resp = requests.get(
        url="{}?page=1".format(API_ENDPOINT)
    )
    resp.raise_for_status()
    paginated = resp.json()
    assert paginated['count'] == len(all_items)
    assert len(paginated['results']) <= 10  # set limit in paginator

    # filtered by state
    resp = requests.get(
        url="{}?state=IP".format(API_ENDPOINT)
    )
    resp.raise_for_status()
    state_only = resp.json()
    assert state_only['count'] > 0

    # return all that are newer/older than given due date

    resp = requests.post(
        url=API_ENDPOINT,
        json={
            'text': 'Created now, due tomorrow',
            'state': 'DN',
            'due_at': str(datetime.datetime.now(tz=TZ) + datetime.timedelta(days=1))
        }
    )
    resp.raise_for_status()

    start = datetime.datetime.now(tz=TZ).isoformat()
    end = (datetime.datetime.now(tz=TZ) + datetime.timedelta(days=2)).isoformat()
    date_url = "{}fetch_by_due_at_range/{}/{}".format(API_ENDPOINT, start, end)
    resp = requests.get(
        url=date_url
    )
    resp.raise_for_status()
    date_range = resp.json()
    assert date_range['count'] > 0


def update():
    """Update an entry in the db.

    :return: None
    :rtype: None
    """
    logger.info("Updating Todo entries")
    resp = requests.post(
        url=API_ENDPOINT,
        json={
            'text': 'Create a new todo for updating',
            'state': 'TD',  # todo
        }
    )
    resp.raise_for_status()
    before = resp.json()

    id_to_fetch = before['id']
    resp = requests.patch(
        url="{}{}/".format(API_ENDPOINT, id_to_fetch),
        json={
            'state': 'DN'  # done
        }
    )
    resp.raise_for_status()
    updated = resp.json()
    assert before['state'] == 'TD'
    assert updated['state'] == 'DN'


def delete():
    """Delete an entry in the db.

    :return: None
    :rtype: None
    """
    logger.info("Deleting Todo entries")
    resp = requests.post(
        url=API_ENDPOINT,
        json={
            'text': 'Todo that will be deleted',
            'state': 'TD',  # todo
        }
    )
    resp.raise_for_status()
    new = resp.json()

    id_to_destroy = new['id']
    resp = requests.delete(
        url="{}{}/".format(API_ENDPOINT, id_to_destroy)
    )
    resp.raise_for_status()
    assert resp.status_code == 204


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-p', '--port', default=8000, type=int,
        help='The port on which the local server is running'
    )
    args = parser.parse_args()

    API_ENDPOINT = "http://localhost:{}/api/v1/todo/".format(args.port)

    create()
    retrieve()
    update()
    delete()

    logger.info("All tests ran successfully.")  # If not, will throw exception before this.
