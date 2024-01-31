import json
import calendar

calendar.setfirstweekday(calendar.SUNDAY)

from schedule import Schedule

EMPTY_HEADER_CELL = "<th class='empty'></th>"
EMPTY_DATA_CELL = "<td class='empty'></td>"


def render_service_header_row(
    service_schedule, schedule: Schedule, max_num_services, cal
):
    day_of_week = service_schedule["daysOfWeek"][0]

    # if no services this week, leave out of schedule
    dates = [
        ""
        if not schedule.assignments(i)
        else f'<th class="day">{week[day_of_week]}</th>'
        if week[day_of_week]
        else "<th></th>"
        for i, week in enumerate(cal)
    ]

    dates = [date for date in dates if date]
    num_dates = len(dates)

    if num_dates < max_num_services:
        dates.append(EMPTY_HEADER_CELL)

    dates_html = EMPTY_DATA_CELL.join(dates)
    return f"""
        <tr>
            <th class="service-name">{service_schedule['name']}</th>
            {EMPTY_HEADER_CELL}
            {dates_html}
        </tr>
    """


def render_duty_assignment_cells(service, duty, num_services, schedule: Schedule):
    assignments = [
        ""
        if not schedule.assignments(i)
        else f"<td>{schedule.assignments(i)[duty['key']]}</td>"
        if duty["key"] in schedule.assignments(i)
        and any(week[day] for day in service["daysOfWeek"])
        else "<td></td>"
        for i, week in enumerate(schedule.cal)
    ]
    assignments = [assignment for assignment in assignments if assignment]
    return EMPTY_DATA_CELL.join(assignments)


def render_duty_row(service, duty, schedule, num_services):
    padding = ""

    return f"""
        <tr>
            <td>{duty['name']}</td>
            {EMPTY_DATA_CELL}
            {render_duty_assignment_cells(service, duty, num_services, schedule)}
            {padding}
        </tr>
    """


def render_duty_assignment_rows(service, schedule, num_services):
    duties = [duty for duty in service["duties"]]

    return "".join(
        [render_duty_row(service, duty, schedule, num_services) for duty in duties]
    )


def render_service(service, schedule, max_num_services, header=True):
    header_html = ""

    if header:
        header_html = f"<thead>{render_service_header_row(service, schedule, max_num_services, schedule.cal)}</thead>"

    return f"""
        <table>
            {header_html}
            <tbody>{render_duty_assignment_rows(service, schedule, max_num_services)}</tbody>
        </table>
    """


def render_monthly_assignments(schedule: Schedule):
    # may have empty first week, every month has at least 2 weeks
    if schedule.assignments(1):
        return "".join(
            [
                f"""
                    <tr>
                        <td class="monthly">{duty['name']}</td>
                        <td class="assignment">{schedule.assignments(1)[duty['key']]}</td>
                    </tr>"""
                for i, duty in enumerate(schedule.service("monthly")["duties"])
            ]
        )
    else:
        return ""


def render_monthly_duties(schedule):
    return f"""
        <table>
            <tbody>
                {render_monthly_assignments(schedule)}
            </tbody>
        </table>
    """


def render_schedule(schedule):
    with open("./style.css", "r") as f:
        style = f.read()

    # max number of services between sunday and wednesday
    num_services = max(
        len(schedule.service("sunday-9am")["days"]),
        len(schedule.service("wednesday")["days"]),
    )

    return f"""
        <html>
            <head>
                <meta name="pdfkit-page-size" content="Legal"/>
                <meta name="pdfkit-orientation" content="Landscape"/>
                <style>{style}</style>
            </head>
            <body>
                <div class="header">
                    <h1>{schedule.month}</h1>
                </div>
                {render_service(schedule.service('sunday-9am'), schedule, num_services)}
                <div class="banner dark-background">
                    2nd Service 10:30
                </div>
                {render_service(schedule.service('sunday-1030am'), schedule, num_services, header=False)}
                {render_service(schedule.service('wednesday'), schedule, num_services)}
                {render_service(schedule.service('weekly'), schedule, num_services, header=False)}
                {render_monthly_duties(schedule)}
            </body>
        </html>
        """
