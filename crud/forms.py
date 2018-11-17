from datetime import datetime
import calendar

from django.forms import ModelForm, widgets, Textarea
from crud.models import Todo

from django.utils import dates as dj_dates


class DateTimeWidget(widgets.MultiWidget):
    """A Date time widgit for year, month, day, hour, minute(15 min intervals).

    Uses a set of 5 Select widgits, one for each range.
    """
    def __init__(self, attrs=None):
        now_year = datetime.now().year
        years = [(year, year) for year in range(now_year, now_year + 5)]
        months = dj_dates.MONTHS_AP.items()
        days = [(i, i) for i in range(1, 32)]
        hours = [(i, i) for i in range(0, 24)]
        minutes = [(i, i) for i in (0, 15, 30, 45)]
        _widgets = (
            widgets.Select(attrs=attrs, choices=days),
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=years),
            widgets.Select(attrs=attrs, choices=hours),
            widgets.Select(attrs=attrs, choices=minutes),
        )
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.day, value.month, value.year, value.hour, value.minute]
        return [None, None, None, None, None]

    def value_from_datadict(self, data, files, name):
        """Parses a valid datetime.  Sets default value to current datetime."""
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            year = int(datelist[2])
            month = int(datelist[1])
            # Deals with day is out of range for month
            day = min(int(datelist[0]), calendar.monthrange(year, month)[1])
            dt = datetime(
                year=year,
                month=month,
                day=day,
                hour=int(datelist[3]),
                minute=int(datelist[4]),
            )
            return dt
        except TypeError:
            return datetime.now()


class TodoForm(ModelForm):
    class Meta:
        model = Todo

        fields = ['text', 'state', 'due_at']
        widgets = {
            'text': Textarea(attrs={'cols': 50, 'rows': 2}),
            'due_at': DateTimeWidget()
        }
