from __future__ import print_function

import csv
from collections import namedtuple
import random

import requests
import tweepy

from secrets import *


Item = namedtuple('Volume', ['name', 'plural', 'value'])


def read_collection(filename):
    with open(filename) as file:
        reader = csv.reader(file)
        return [
            Item(row[0].strip(), row[1].strip(), float(row[2]))
            for row in reader
        ]


def pick_a_and_b(choices):
    a = b = random.choice(choices)
    while b.value * 2 > a.value:
        a = random.choice(choices)
        b = random.choice(choices)
    return a, b


def generate_message(choice, a, b):
    number = round(a.value / b.value)

    if b.plural:
        return 'Approximately {number} {b.plural} fit into {a.name}.' \
            .format(number=number, b=b, a=a)
    else:
        return '{b_name} fits into {a.name} approximately {number} times.' \
            .format(a=a, b_name=b.name.capitalize(), number=number)


collections = {
    'volume': read_collection('volumes.csv'),
    'duration': read_collection('durations.csv'),
    'area': read_collection('areas.csv'),
}

choice = random.choice(list(collections.keys()))
#choice = "volume"

collection = collections[choice]

a, b = pick_a_and_b(collection)
message = generate_message(choice, a, b)

print(message)

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.valueet_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)
api.update_status(message)
