import calendar

calendar.setfirstweekday(calendar.SUNDAY)
import sys
import pdfkit
import os

from loaders import (
    load_men_csv,
    load_service_duties,
    load_service_duty_exclusions_csv,
)
from renderers import render_schedule
from schedule import Schedule


men, duty_index = load_men_csv()
duty_exclusions = load_service_duty_exclusions_csv()
service_duties, all_duties = load_service_duties()


def get_available_man_for_duty(
    duty_key, available_men, reassign_index, week_assignments
):
    """
    find an available man (has not assigned to an excluded duty in week_assignments) for
    duty_key started at reassign_index
    """
    # print(f"reassigning {duty_key}")
    excluded_duties = duty_exclusions[duty_key]
    count = 0
    found = False
    while count < len(available_men) and not found:
        current_man = available_men[reassign_index % len(available_men)]
        # print(f"checking if {current_man} assigned to excluded duties of {duty_key}")
        for excluded_duty in excluded_duties:
            if (
                excluded_duty in week_assignments
                and week_assignments[excluded_duty] == current_man
            ):
                # print(
                #     f"{current_man} already assigned to {excluded_duty} cannot be assigned with {duty_key}"
                # )
                count += 1
                reassign_index += 1
                break
        else:
            found = True

    if not found:
        raise RuntimeError(f"could not assign man to {duty_key}")

    return reassign_index


def duty_this_week(week: list[int], duty_key: str, schedule: Schedule) -> bool:
    for service in schedule.services().values():
        for duty in service["duties"]:
            if duty["key"] == duty_key:
                for day in service["daysOfWeek"]:
                    if week[day]:
                        return True
                else:
                    return False
    return False


def make_schedule(year, month):
    schedule = Schedule(year, month, service_duties)

    cal = calendar.monthcalendar(year, month)
    year_month = year + month

    for i, duty in enumerate(all_duties.items()):
        duty_key = duty[0]
        available_men = duty_index[duty_key]

        rr_index = (i * 3 + 4 * year_month) % len(available_men)
        for week_index, week in enumerate(cal):
            if not duty_this_week(week, duty_key, schedule):
                continue

            # print(f"week_index {week_index}")
            # print(f"week {week}")
            # print(f"\nAssigning {duty_key}")

            current_man = available_men[rr_index % len(available_men)]

            if duty_key in duty_exclusions:
                for excluded_duty in duty_exclusions[duty_key]:
                    if (
                        excluded_duty in schedule.assignments(week_index)
                        and schedule.assignment(week_index, excluded_duty)
                        == current_man
                    ):
                        # print(f"{current_man} already assigned to {excluded_duty}")
                        reassign_index = rr_index + 1
                        rr_index = get_available_man_for_duty(
                            duty_key,
                            available_men,
                            reassign_index,
                            schedule.assignments(week_index),
                        )
                        # print(
                        #     f"Reassigned {duty_key} to {available_men[rr_index % len(available_men)]}"
                        # )

            current_man = available_men[rr_index % len(available_men)]

            # assign a man to a duty in this service
            schedule.assign(week_index, duty_key, current_man)
            # print(f"Assigned {current_man} to {duty_key}")

            rr_index += 1

    return schedule


def main():
    # Accept month and year from command line arguments
    if len(sys.argv) < 4:
        print("Usage: python schedule.py <month> <year> </path/to/output_file>")
        sys.exit(1)

    month = int(sys.argv[1])
    year = int(sys.argv[2])
    pdf_output_file = sys.argv[3]

    debug = "--debug" in sys.argv

    schedule = make_schedule(year, month)

    # TODO handle special events (e.g. Gospel Meetings)

    # with --page-size=Legal and --orientation=Landscape
    output_filename = os.path.basename(pdf_output_file)

    json_output_dir = os.path.dirname(pdf_output_file) + "/output/json"
    os.makedirs(json_output_dir, exist_ok=True)
    with open(f"{json_output_dir}/{output_filename}.json", "w") as f:
        f.write(schedule.__str__())

    html = render_schedule(schedule)
    html_output_dir = os.path.dirname(pdf_output_file) + "/output/html"
    os.makedirs(html_output_dir, exist_ok=True)

    with open(f"{html_output_dir}/{output_filename}.html", "w") as f:
        f.write(html)

    pdfkit.from_string(html, pdf_output_file)


if __name__ == "__main__":
    main()
