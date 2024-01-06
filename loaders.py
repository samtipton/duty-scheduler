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
    service_duties["all"] = all_duties
    return service_duties


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
    men = {}
    with open("./men/men.csv", newline="") as csvfile:
        dict_reader = csv.DictReader(csvfile)
        headers = dict_reader.fieldnames[1:]

        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            duties = [h for i, h in enumerate(headers) if row[i + 1] == "1"]

            if duties:
                last_name, first_name = row[0].split(", ")
                men[row[0]] = {
                    "duties": duties,
                    "formatted_name": row[0],
                    "last_name": last_name,
                    "first_name": first_name,
                }

    return men


def load_duty_index(men, service_duties):
    """
    index duties to men that can perform them
    """
    duty_index = {}

    sorted_men = [man for man in men.values()]
    sorted_men.sort(key=lambda man: man["last_name"])

    duties = [
        duty
        for service in service_duties.values()
        if "duties" in service
        for duty in service["duties"]
    ]

    # print(men)
    for man in sorted_men:
        for duty in duties:
            if duty["key"] in men[man["formatted_name"]]["duties"]:
                if duty["key"] in duty_index:
                    duty_index[duty["key"]].append(man["formatted_name"])
                else:
                    duty_index[duty["key"]] = [man["formatted_name"]]

    return duty_index
