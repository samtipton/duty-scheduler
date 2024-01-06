# Olsen Park church of Christ Duty Roster Generator

## Usage:

`$ source venv/bin/activate`

`$ python3 schedule.py <month_number> <year> path/to/output/file`

Example:

`$ python3 schedule.py 1 2024 ~/Desktop/roster-1-2024.pdf`

## Configuration

This script relies on two .csv files being present in the men and duties directory.

### men/men.csv

`men.csv` contains all the men that serve and the the duties they have signed up to fulfill. A cell value of `'1'` indicates they are willing to serve in the capacity of the responsibility contained in the column.

### duties/exclusions.csv

`exclusions.csv` contains an encoding of all duties that must be performed in exclusion to other duties. That is, duties that cannot be assigned to the same man in the same service, for example, Song Leading and Sound Board Operator.

If the cell contains a 1, then the duties contained in the first row and first column may not be performed together.

##### A note:

In most cases, these exclusions will be mutual exclusions, Lead Bread excludes Lead Cup and vice versa, Lead Cup excludes Lead Bread.

However, you could require a case where Wednesday lessons are excluded from being assigned together with the Sunday lesson, but the Sunday lesson (which many less people will be available to fill), may not exclude the Wednesday lesson.

#### Modifying these files

These files are more easily maintained via spreadsheet and can be found in this [sheet](https://docs.google.com/spreadsheets/d/1ZvrvidGAKMgeG7aW0cY0kQ-0DDIzW-x2EG4FS-oczqI/edit?usp=sharing) for Olsen Park.

For other congregations, I suggest you create your own spreadsheets to import your own csvs.
