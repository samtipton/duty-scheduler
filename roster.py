import calendar
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


def main():
    # check duty exclusion rule for that slot

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

    # consider using objects
    for i, week in enumerate(cal):

        # weekly duties
        weekly_schedule = {}
        for duty in service_duties['weekly']['duties']:
            weekly_schedule[duty['name']] = duty_index[duty['key']][(i+year_month) % len(
                duty_index[duty['key']])]

        if 'weekly' not in schedule:
            schedule['weekly'] = {}

        schedule['weekly'][f'{week[6]}'] = weekly_schedule

        # need to handle constraints
        if week[6]:
            sunday_9am_schedule = {}
            for duty in service_duties['sunday-9am']['duties']:
                sunday_9am_schedule[duty['name']] = duty_index[duty['key']][(i + year_month) % len(
                    duty_index[duty['key']])]

            if 'sunday-9am' not in schedule:
                schedule['sunday-9am'] = {}

            schedule['sunday-9am'][f'{week[6]}'] = sunday_9am_schedule

            sunday_1030am_schedule = {}
            for duty in service_duties['sunday-1030am']['duties']:
                sunday_1030am_schedule[duty['name']] = duty_index[duty['key']][(i+year_month) % len(
                    duty_index[duty['key']])]

            if 'sunday-1030am' not in schedule:
                schedule['sunday-1030am'] = {}

            schedule['sunday-1030am'][f'{week[6]}'] = sunday_1030am_schedule

        # todo handle singing service on last wednesday with its own duty
        if week[2]:
            wednesday_schedule = {}
            for duty in service_duties['wednesday']['duties']:
                wednesday_schedule[duty['name']] = duty_index[duty['key']][(i+year_month) % len(
                    duty_index[duty['key']])]

            if 'wednesday' not in schedule:
                schedule['wednesday'] = {}

            schedule['wednesday'][f'{week[2]}'] = wednesday_schedule

    monthly_schedule = {}
    for duty in service_duties['monthly']['duties']:
        monthly_schedule[duty['name']] = duty_index[duty['key']
                                                    ][(i + year_month) % len(duty_index[duty['key']])]

    schedule['monthly'] = monthly_schedule
    # create schedule meta information (name, days, duties)
    schedule['sunday-9am']['meta'] = service_duties['sunday-9am']
    schedule['sunday-9am']['meta']['days'] = [str(week[6])
                                              for week in cal if week[6]]
    schedule['sunday-1030am']['meta'] = service_duties['sunday-1030am']
    schedule['sunday-1030am']['meta']['days'] = [str(week[6])
                                                 for week in cal if week[6]]
    schedule['wednesday']['meta'] = service_duties['wednesday']
    schedule['wednesday']['meta']['days'] = [str(week[2])
                                             for week in cal if week[2]]

    schedule['weekly']['meta'] = service_duties['weekly']
    schedule['weekly']['meta']['days'] = [str(week[6])
                                          for week in cal if week[6]]

    # special events

    html = render_schedule(schedule)

    if debug:
        os.makedirs(os.path.dirname('./build/schedule.html'), exist_ok=True)
        with open('./build/schedule.html', 'w') as f:
            f.write(html)

    # with --page-size=Legal and --orientation=Landscape
    pdfkit.from_string(html, pdf_output_file)


if __name__ == "__main__":
    main()
