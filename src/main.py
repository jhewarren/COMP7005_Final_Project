from Emulator import emulator
from Server import server
from Client import client
import json


config = json.load(open("config.json"))
print(config)
client.run(config)
