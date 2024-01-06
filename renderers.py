import json

empty_header_cell = "<th class='empty'></th>"
empty_data_cell = "<td class='empty'></td>"


def render_service_header_row(service_schedule, max_num_services):
    dates = [
        f'<th class="day">{service_day}</th>'
        for service_day in service_schedule["days"]
    ]
    num_dates = len(dates)

    if num_dates < max_num_services:
        dates.append(empty_header_cell)

    dates_html = empty_data_cell.join(dates)
    return f"""
        <tr>
            <th class="service-name">{service_schedule['name']}</th>
            {empty_header_cell}
            {dates_html}
        </tr>
    """


def render_duty_assignment_cells(duty, days, schedule):
    return empty_data_cell.join(
        [f"<td>{schedule['assignments'][i][duty]}</td>" for i in range(len(days))]
    )


def render_duty_row(duty, days, schedule, duty_labels, max_num_services):
    padding = ""
    if len(days) < max_num_services:
        padding = empty_data_cell + "<td></td>"

    return f"""
        <tr>
            <td>{duty_labels[duty]}</td>
            {empty_data_cell}
            {render_duty_assignment_cells(duty, days, schedule)}
            {padding}
        </tr>
    """


def render_duty_assignment_rows(
    service_assignments, schedule, duty_labels, max_num_services
):
    # print(service_schedule)
    days = service_assignments["days"]
    duties = [duty for duty in service_assignments["duties"]]

    return "".join(
        [
            render_duty_row(duty, days, schedule, duty_labels, max_num_services)
            for duty in duties
        ]
    )


def render_service(service_key, schedule, duty_labels, max_num_services, header=True):
    services = schedule[service_key]
    header_html = ""

    if header:
        header_html = (
            f"<thead>{render_service_header_row(services, max_num_services)}</thead>"
        )

    return f"""
        <table>
            {header_html}
            <tbody>{render_duty_assignment_rows(services, schedule, duty_labels, max_num_services)}</tbody>
        </table>
    """


def render_monthly_assignments(schedule, duty_labels):
    if schedule["assignments"]:
        return "".join(
            [
                f"""
                    <tr>
                        <td class="monthly">{duty_labels[duty]}</td>
                        <td class="assignment">{schedule['assignments'][0][duty]}</td>
                    </tr>"""
                for i, duty in enumerate(schedule["monthly"]["duties"])
            ]
        )
    else:
        return ""


def render_monthly_duties(schedule, duty_labels):
    return f"""
        <table>
            <tbody>
                {render_monthly_assignments(schedule, duty_labels)}
            </tbody>
        </table>
    """


def render_schedule(schedule, duty_labels):
    with open("./style.css", "r") as f:
        style = f.read()

    # max number of services between sunday and wednesday
    num_services = max(
        len(schedule["sunday-9am"]["days"]), len(schedule["wednesday"]["days"])
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
                    <h1>{schedule['month']}</h1>
                </div>
                {render_service('sunday-9am', schedule, duty_labels, num_services)}
                <div class="banner dark-background">
                    2nd Service 10:30
                </div>
                {render_service('sunday-1030am', schedule, duty_labels, num_services, header=False)}
                {render_service('wednesday', schedule, duty_labels, num_services)}
                {render_service('weekly', schedule, duty_labels, num_services, header=False)}
                {render_monthly_duties(schedule, duty_labels)}
            </body>
        </html>
        """
