from tkinter import Tk
from unittest import TestCase

from src.data_adapters.mongo_interface import get_default_mongo_client

from src.tests.testsetup import Controller, Player, View

def create_app(data: str):
    app = Tk()

    v = View(app)
    v.pack()
    c = Controller(APPS[data]())
    c.set_view(v)

    app.mainloop()


class ViewTest(TestCase):

    def test_fake_data(self):
        create_app('TEST')

    def test_live_data(self):
        create_app('LIVE')


def live_frame_data():
    client = get_default_mongo_client()
    return [Player(db, 20) for db in client.list_database_names()]

def test_frame_data():
    return [Player('Billy', 69), Player('Bobby', 420)]

APPS = {
    'LIVE': live_frame_data,
    'TEST': test_frame_data
}
