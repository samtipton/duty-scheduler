import calendar
import json
import sys
import pdfkit
import os

from loaders import (
    load_men_csv,
    load_service_duties,
    load_duty_index,
    load_service_duty_exclusions_csv,
)
from renderers import render_schedule


men = load_men_csv()
duty_exclusions = load_service_duty_exclusions_csv()
service_duties = load_service_duties()
duty_index = load_duty_index(men, service_duties)

MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def add_service_info(service_name, service_day_ord, schedule):
    if service_name not in schedule:
        schedule[service_name] = {}

        schedule[service_name] = {}
        schedule[service_name]["duties"] = [
            duty["key"] for duty in service_duties[service_name]["duties"]
        ]
        schedule[service_name]["days"] = [f"{service_day_ord}"]

        if "name" in service_duties[service_name]:
            schedule[service_name]["name"] = service_duties[service_name]["name"]
    else:
        schedule[service_name]["days"].append(f"{service_day_ord}")


def get_available_man_for_duty(
    duty_key, available_men, reassign_index, week_assignments
):
    """
    find an available man (has not assigned to an excluded duty in week_assignments) for
    duty_key started at reassign_index
    """
    print(f"reassigning {duty_key}")
    excluded_duties = duty_exclusions[duty_key]
    count = 0
    found = False
    while count < len(available_men) and not found:
        current_man = available_men[reassign_index % len(available_men)]
        print(f"checking if {current_man} assigned to excluded duties of {duty_key}")
        for excluded_duty in excluded_duties:
            if (
                excluded_duty in week_assignments
                and week_assignments[excluded_duty] == current_man
            ):
                print(
                    f"{current_man} already assigned to {excluded_duty} cannot be assigned with {duty_key}"
                )
                count += 1
                reassign_index += 1
                break
        else:
            found = True

    if not found:
        raise RuntimeError(f"could not assign man to {duty_key}")

    return reassign_index


def main():
    # Accept month and year from command line arguments
    if len(sys.argv) < 4:
        print("Usage: python schedule.py <month> <year> </path/to/output_file>")
        sys.exit(1)

    month = int(sys.argv[1])
    year = int(sys.argv[2])
    pdf_output_file = sys.argv[3]

    debug = "--debug" in sys.argv

    year_month = year + month  # for round robin index
    cal = calendar.monthcalendar(year, month)

    schedule = {}
    schedule["month"] = MONTH_NAMES[month - 1]
    schedule["assignments"] = []

    # need to handle constraints
    for i, week in enumerate(cal):
        schedule["assignments"].append({})

        assigned = set()  # men who have assignment already

        for j, duty in enumerate(service_duties["all"].items()):
            duty_key = duty[0]
            available_men = duty_index[duty_key]

            rr_index = (i + j * 3 + 4 * year_month) % len(available_men)
            current_man = available_men[rr_index]

            print(f"\nAssigning {duty_key}")
            if duty_key in duty_exclusions:
                for excluded_duty in duty_exclusions[duty_key]:
                    if (
                        excluded_duty in schedule["assignments"][i]
                        and schedule["assignments"][i][excluded_duty] == current_man
                    ):
                        print(f"{current_man} already assigned to {excluded_duty}")
                        reassign_index = rr_index + 1
                        rr_index = get_available_man_for_duty(
                            duty_key,
                            available_men,
                            reassign_index,
                            schedule["assignments"][i],
                        )
                        print(
                            f"Reassigned {duty_key} to {available_men[rr_index % len(available_men)]}"
                        )

            chosen_man = available_men[rr_index % len(available_men)]
            print(f"assigned {chosen_man} to {duty_key}")

            # assign a man to a duty in this service
            schedule["assignments"][i].update({duty_key: chosen_man})
            assigned.add(chosen_man)

        # Create add Sunday assignments
        if week[6]:
            add_service_info("sunday-9am", week[6], schedule)
            add_service_info("sunday-1030am", week[6], schedule)
            add_service_info("weekly", week[6], schedule)

        # Create add Wednesday assignments
        if week[2]:
            # todo handle singing service on last wednesday with its own duty
            add_service_info("wednesday", week[2], schedule)

    # Create add Monthly assignments
    add_service_info("monthly", -1, schedule)

    # TODO handle special events (e.g. Gospel Meetings)

    # if debug:
    #     os.makedirs(os.path.dirname("./build/schedule.json"), exist_ok=True)
    #     with open("./build/schedule.json", "w") as f:
    #         f.write(json.dumps(schedule))

    html = render_schedule(schedule, service_duties["all"])

    # if debug:
    #     os.makedirs(os.path.dirname("./build/schedule.html"), exist_ok=True)
    #     with open("./build/schedule.html", "w") as f:
    #         f.write(html)

    # with --page-size=Legal and --orientation=Landscape
    html_output_dir = os.path.dirname(pdf_output_file) + "/output/html"
    json_output_dir = os.path.dirname(pdf_output_file) + "/output/json"

    output_filename = os.path.basename(pdf_output_file)

    os.makedirs(html_output_dir, exist_ok=True)
    os.makedirs(json_output_dir, exist_ok=True)

    with open(f"{html_output_dir}/{output_filename}.html", "w") as f:
        f.write(html)
    with open(f"{json_output_dir}/{output_filename}.json", "w") as f:
        f.write(json.dumps(schedule))

    pdfkit.from_string(html, pdf_output_file)


if __name__ == "__main__":
    main()
