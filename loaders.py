import json
import os
import csv


def load_service_duties():
    service_duties = {}
    all_duties = {}
    for filename in os.listdir("./duties"):
        if filename.endswith(".json"):
            with open(f"./duties/{filename}", "r") as f:
                data = json.load(f)
                all_duties.update(
                    {duty["key"]: duty["name"] for duty in data["duties"]}
                )
                service_duties[filename[:-5]] = data
    return service_duties, all_duties


def load_service_duty_exclusions_csv():
    exclusions = {}
    with open("./duties/exclusions.csv", newline="") as csvfile:
        dict_reader = csv.DictReader(csvfile)
        headers = dict_reader.fieldnames[1:]
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            excluded = set(
                [
                    h
                    for i, h in enumerate(headers)
                    if row[i + 1] == "1" and headers[i] != row[0]
                ]
            )

            if excluded:
                exclusions[row[0]] = excluded

    return exclusions


def load_men_csv():
    # map each man to the duties they have signed up for
    men = {}

    # reverse index of men: map each duty to the men who signed up for it
    duty_index = {}

    with open("./men/men.csv", newline="") as csvfile:
        dict_reader = csv.DictReader(csvfile)
        headers = dict_reader.fieldnames[1:]

        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            elected_duties = [h for i, h in enumerate(headers) if row[i + 1] == "1"]
            name = row[0]

            [
                duty_index[duty].append(name)
                if duty in duty_index
                else duty_index.update({duty: [name]})
                for duty in elected_duties
            ]

            if elected_duties:
                last_name, first_name = name.split(", ")
                men[name] = {
                    "duties": elected_duties,
                    "formatted_name": name,
                    "last_name": last_name,
                    "first_name": first_name,
                }

    [available_men.sort() for available_men in duty_index.values()]

    return men, duty_index
