import calendar
import json
import sys
import pdfkit
import os

from loaders import load_men, load_service_duties, load_duty_index
from renderers import render_schedule

men = load_men()
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
    "December"
]

def add_duties_for_service(service_name, service_day_ord, schedule, round_robin_seed):
    service_schedule = {}

    for i, duty in enumerate(service_duties[service_name]['duties']):
        # print(f'i={i}')
        # print(f'seed={round_robin_seed}')
        # print(f'index={duty_index[duty["key"]]}')
        # print(f"index={(i + round_robin_seed) % len(duty_index[duty['key']])}")
        # print(f"len={len(duty_index[duty['key']])}")
        # print(f"choice={duty_index[duty['key']][(i + round_robin_seed) % len(duty_index[duty['key']])]}")

        # assign a man to a duty in this service
        service_schedule[duty['name']] = duty_index[duty['key']][(i + round_robin_seed) % len(duty_index[duty['key']])]

    if service_name not in schedule:
        schedule[service_name] = {}
        
        # add meta information
        schedule[service_name]['meta'] = {}
        schedule[service_name]['meta']['duties'] = [duty['name'] for duty in service_duties[service_name]['duties']]
        schedule[service_name]['meta']['days'] = [f'{service_day_ord}']

        if 'name' in service_duties[service_name]:
            schedule[service_name]['meta']['name'] = service_duties[service_name]['name']
    else:
        schedule[service_name]['meta']['days'].append(f'{service_day_ord}')

    if service_day_ord == -1:
        schedule[service_name]['assignments'] = [service_schedule]
    else:
        if not 'assignments' in schedule[service_name]:
            schedule[service_name]['assignments'] = [service_schedule]
        else:
            schedule[service_name]['assignments'].append(service_schedule)


def main():
    # Accept month and year from command line arguments
    if len(sys.argv) < 4:
        print("Usage: python schedule.py <month> <year> </path/to/output_file>")
        sys.exit(1)

    month = int(sys.argv[1])
    year = int(sys.argv[2])
    pdf_output_file = sys.argv[3]

    debug = '--debug' in sys.argv

    year_month = year + month  # for round robin index
    cal = calendar.monthcalendar(year, month)

    schedule = {}
    schedule['month'] = MONTH_NAMES[month-1]

    # need to handle constraints
    for i, week in enumerate(cal):

        if week[6]:
            add_duties_for_service('weekly', week[6], schedule, i + year_month)
            add_duties_for_service('sunday-9am', week[6], schedule, i + year_month)
            add_duties_for_service('sunday-1030am', week[6], schedule, i + year_month)

        if week[2]:
            # todo handle singing service on last wednesday with its own duty
            add_duties_for_service('wednesday', week[2], schedule, i + year_month)

    add_duties_for_service('monthly', -1, schedule, i + year_month)

    # todo handle special events (e.g. Gospel Meetings)

    if debug:
        print(json.dumps(schedule))

    html = render_schedule(schedule)

    if debug:
        os.makedirs(os.path.dirname('./build/schedule.html'), exist_ok=True)
        with open('./build/schedule.html', 'w') as f:
            f.write(html)

    # with --page-size=Legal and --orientation=Landscape
    pdfkit.from_string(html, pdf_output_file)


if __name__ == "__main__":
    main()
