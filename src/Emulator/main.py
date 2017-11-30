import client
import json


config = json.load(open("config.json"))
print(config)
client.run(config)
