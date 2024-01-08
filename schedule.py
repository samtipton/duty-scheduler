import calendar
import json

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


class Schedule:
    def __init__(self, year, month_int, service_duties):
        self.year = year
        self.month_int = month_int
        self.month = MONTH_NAMES[month_int - 1]
        cal = calendar.monthcalendar(year, month_int)

        self._assignments = [{} for week in cal]
        self._services = self.init_service_duties(cal, service_duties)

    def init_service_duties(self, cal, service_duties):
        services = service_duties.copy()

        for service_name, service in service_duties.items():
            service["days"] = []
            for day in service["daysOfWeek"]:
                for week in cal:
                    if week[day]:
                        service["days"].append(week[day])
            service["days"].sort()

        return services

    def services(self):
        return self._services

    def service(self, service_name):
        return self._services[service_name]

    def assign(self, week, duty_key, name):
        self._assignments[week][duty_key] = name

    def assignments(self, week):
        return self._assignments[week]

    def assignment(self, week, duty_key):
        return self._assignments[week][duty_key]

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
