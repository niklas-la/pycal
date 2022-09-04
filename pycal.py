from typing import Optional

import arrow
import typer
from ics import Calendar


class iCalender(object):
    """A class to handle iCalender files"""

    def __init__(self, filename):
        self.filename = filename

    def __len__(self):
        return len(self.get_calendar().events)

    def get_calendar(self):
        with open(self.filename) as f:
            ical = Calendar(f.read())

            return ical

    def get_range(self, start, stop):
        ical = self.get_calendar()
        if start:
            ical.events = [
                event for event in ical.events if event.begin >= arrow.get(start)]
        if stop:
            ical.events = [event for event in ical.events if event.end <=
                           arrow.get(stop)]

        return ical


def main(path: str = typer.Argument(..., help="Path to iCalendar file"),
         start: Optional[str] = typer.Option(
             None, help="Start of the time period in the format year-month-day"),
         stop: Optional[str] = typer.Option(None, help="End of the time period in the format year-month-day")):
    """A tool to extract time spans from iCalendar files."""
    ical = iCalender(path)
    count = len(ical)
    events = ical.get_range(start, stop)
    with open(path, 'w') as f:
        f.writelines(events.serialize_iter())
    typer.echo(f"Removed {count - len(events.events)} events from {path}")


if __name__ == "__main__":
    typer.run(main)
