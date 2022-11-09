import requests
import csv
import io
import json
import ics
import dateutil.parser as dateParser
from ics.grammar import parse
from flask import Flask, Response

app = Flask(__name__)

courses = ["svenska", "gymnasiearbete", "religionskunskap", "mdh", "matematik", "teknik terobvs", "engelska", "fysik", "idrott", "utvärdering"]

url = "https://cloud.timeedit.net/abbindustrigymnasium/web/public1/ri1Y7X6QQ7fZY6QfZ507Q565y0YQ2Zbny1X.csv"

csv_raw = requests.get(url).text

csv_raw = csv_raw.split("\n", 2)[2]

info, csv_raw = csv_raw.split("\n", 1)

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

     
@app.route("/get_<course>")
def get_course(course):
    print(info)
    if course not in data: 
        return "Course not found"
    c = ics.Calendar()
    c.method = "PUBLISH"
    c.extra.append(parse.ContentLine(name="X-WR-CALNAME", value=info[:-1]))
    for row in data[course]:
        print(row)
        e = ics.Event() 
        e.begin = dateParser.parse(row["Startdatum"] + " " + row["Starttid"] + "+0100")
        e.name = row["Kurs"]
        e.description = row["Info,Grupp"] + " " + row["Lärare"]
        e.location = row["Sal"] + " " + row[" "]
        e.end = dateParser.parse(row["Slutdatum"] + " " + row["Sluttid"] + "+0100")
        c.events.add(e)
       
    return Response(
            c.serialize(),
            mimetype='text/plain',
            headers={"Content-disposition": f"attachment; filename={course}.ics"})
