import requests
import csv
import io
import json
import ics
import dateutil.parser as dateParser
from ics.grammar import parse

courses = ["svenska", "gymnasiearbete", "religionskunskap", "mdh", "matematik", "teknik_terobvs", "engelska", "fysik", "idrott", "utvardering", "other"]

def get_course2(course):
    url = "https://cloud.timeedit.net/abbindustrigymnasium/web/public1/ri1Y7X6QQ7fZY6QfZ507Q565y0YQ2Zbny1X.csv"
    csv_raw = requests.get(url).text
    csv_raw = csv_raw.split("\n", 2)[2]

    info, csv_raw = csv_raw.split("\n", 1)

    csv_reader = csv.DictReader(io.StringIO(csv_raw))
    
    data = []
    
    for course_iter in csv_reader:
        if course in course_iter["Kurs"].lower().replace("ä", "a").replace(" ", "_"): #only utvärdering which contains special character, hence only ä needed.
            data.append(course_iter)
            
    return info, data
     
def lambda_handler(event, context):
    url = event["rawPath"]
    course = url[1:]
    print(course)
    if course in courses:
        info, data = get_course2(course)

        c = ics.Calendar()
        c.method = "PUBLISH"
        c.extra.append(parse.ContentLine(name="X-WR-CALNAME", value=info[:-1]))

        for row in data:
            print(row)
            e = ics.Event() 
            e.begin = dateParser.parse(row["Startdatum"] + " " + row["Starttid"] + "+0100")
            e.name = row["Kurs"]
            e.description = row["Info,Grupp"] + "\n" + row["Lärare"]
            e.location = row["Sal"] + " " + row[" "]
            e.end = dateParser.parse(row["Slutdatum"] + " " + row["Sluttid"] + "+0100")
            c.events.add(e)     

        return {
        'statusCode': 200,
        'headers': {
            'content-disposition': f'attachment; filename={course}.ics'
        },
        'body': c.serialize()
        }
    else:
        return {
            'statusCode': 400,
            'body': {
                'error': 'course not in list of known courses',
                'requested_course': course,
                'known_courses': courses 
            }
       }
