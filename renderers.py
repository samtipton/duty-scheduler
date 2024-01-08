import json

from schedule import Schedule

EMPTY_HEADER_CELL = "<th class='empty'></th>"
EMPTY_DATA_CELL = "<td class='empty'></td>"


def render_service_header_row(service_schedule, max_num_services):
    dates = [
        f'<th class="day">{service_day}</th>'
        for service_day in service_schedule["days"]
    ]
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


def render_duty_assignment_cells(duty, num_services, schedule: Schedule):
    return EMPTY_DATA_CELL.join(
        [
            f"<td>{schedule.assignments(i)[duty['key']]}</td>"
            for i in range(0, num_services)
            if duty["key"] in schedule.assignments(i)
        ]
    )


def render_duty_row(duty, days, schedule, num_services):
    padding = ""
    if len(days) < num_services:
        padding = EMPTY_DATA_CELL + "<td></td>"

    return f"""
        <tr>
            <td>{duty['name']}</td>
            {EMPTY_DATA_CELL}
            {render_duty_assignment_cells(duty, num_services, schedule)}
            {padding}
        </tr>
    """


def render_duty_assignment_rows(service_assignments, schedule, num_services):
    # print(service_schedule)
    days = service_assignments["days"]
    duties = [duty for duty in service_assignments["duties"]]

    return "".join(
        [render_duty_row(duty, days, schedule, num_services) for duty in duties]
    )


def render_service(service, schedule, max_num_services, header=True):
    header_html = ""

    if header:
        header_html = (
            f"<thead>{render_service_header_row(service, max_num_services)}</thead>"
        )

    return f"""
        <table>
            {header_html}
            <tbody>{render_duty_assignment_rows(service, schedule, max_num_services)}</tbody>
        </table>
    """


def render_monthly_assignments(schedule: Schedule):
    if schedule.assignments(0):
        return "".join(
            [
                f"""
                    <tr>
                        <td class="monthly">{duty['name']}</td>
                        <td class="assignment">{schedule.assignments(0)[duty['key']]}</td>
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
