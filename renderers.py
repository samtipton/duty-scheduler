import html

empty_header_cell = "<th>     </th>"
empty_data_cell = "<td>      </td>"


def render_service_header_row(service_schedule):
    dates = f"{empty_header_cell}".join([f'<th>{service_day}</th>' for service_day in service_schedule.keys() if service_day != 'meta'
                                         ])
    return f"""
        <tr>
            <th>{service_schedule['meta']['name']}</th>
            {empty_header_cell}
            {dates}
        </tr>
    """


def render_duty_assignment_cells(duty, days, service_schedule):
    return empty_data_cell.join([f"<td>{service_schedule[date][duty]}</td>" for date in days])


def render_duty_row(duty, days, service_assignments):

    return f"""
        <tr>
            <td>{duty}</td>
            {empty_data_cell}
            {render_duty_assignment_cells(duty, days, service_assignments)}
        </tr>
    """


def render_service_assignments_row(service_assignments):
    # print(service_schedule)
    days = service_assignments['meta']['days']
    duties = [duty['name'] for duty in service_assignments['meta']['duties']]

    return "".join([render_duty_row(duty, days, service_assignments) for duty in duties])


def render_service(service_key, schedule):
    services = schedule[service_key]
    return f"""
        <table>
            {render_service_header_row(services)}
            {render_service_assignments_row(services)}
        </table>
    """


def render_schedule(schedule):
    return f"""
        <html>
            <head>
                <meta name="pdfkit-page-size" content="Legal"/>
                <meta name="pdfkit-orientation" content="Landscape"/>
                <style>
                    table {{
                        width: 100%;
                        border: 1px solid black;
                        border-collapse: collapse;
                    }}
                    th, td {{
                        border: 1px solid black;
                        border-collapse: collapse;
                    }}
                    .header {{
                        width: 100%;
                        border: 1px solid black;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>{schedule['month']}</h1>
                </div>
                {render_service('sunday-9am', schedule)}
                {render_service('sunday-1030am', schedule)}
                {render_service('wednesday', schedule)}
            </body>
        </html>
        """
