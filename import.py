from ics import Calendar
import requests

url = "https://cloud.timeedit.net/abbindustrigymnasium/web/public1/ri.ics?sid=3&p=0.w%2C12.w&objects=7612.20&e=221108&enol=t"
c = Calendar(requests.get(url).text)

c
c.events
#  ...}
e = list(c.timeline)[0]
print(c.extra)
"Event '{}' started {}".format(e.name, e.begin.humanize())