import requests
import csv
import io
import json
import ics

courses = ["svenska", "gymnasiearbete", "religionskunskap", "mdh", "matematik", "teknik terobvs", "engelska", "fysik", "idrott", "utvärdering"]

url = "https://cloud.timeedit.net/abbindustrigymnasium/web/public1/ri1Y7X6QQ7fZY6QfZ507Q565y0YQ2Zbny1X.csv"

csv_raw = requests.get(url).text

csv_raw = csv_raw.split("\n", 3)[3]

csv_reader = csv.DictReader(io.StringIO(csv_raw))

data = {"other": []}
for course in courses:
    data[course] = []

for row in csv_reader:
    for course in courses:
        if course in row["Kurs"].lower():
            data[course].append(row)
            break
    else:
        data["other"].append(row)


#print(data)
print(json.dumps(data, indent="\t"))

c = ics.Calendar()
for row in data["svenska"]:
    print(row)
    e = ics.Event() 
    e.begin = row["Startdatum"] + " " + row["Starttid"]
    e.name = row["Kurs"]
    e.description = row["Info,Grupp"] + " " + row["Lärare"]
    e.location = row["Klass"]
    e.end = row["Slutdatum"] + " " + row["Sluttid"]
    c.events.add(e)
   
with open('my.ics', 'w') as f:
    f.writelines(c.serialize_iter())