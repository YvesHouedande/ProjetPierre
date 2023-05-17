from datetime import datetime as dt, time, timedelta as td, date
# from workalendar.europe import France


# cal = France()

# print(dir(cal))
# print(cal.get_variable_days(2023))


    # total_seconds = (self.timedelta_()*(date_td.days*24*60 - (nb_days_off+total_time_b))).total_seconds()
    # hrs, rem = divmod(total_seconds, 3600)
    # mins, seconds = divmod(rem, 60)
    # return f"{int(hrs)}:{int(mins):02d}:{int(seconds):02d}"

time_f  = "%H:%M:%S"
date_f = "%d-%m-%y"
workTimeInfo = {
            "Mon-Thurs":{
                "one":[
                    dt.strptime("06:30:00", time_f), 
                    dt.strptime("14:51:00", time_f)
                    ],
                "two":[
                    dt.strptime("14:51:00", time_f),
                    dt.strptime("00:09:00", time_f)
                    ]
            },
            "Fri":[
                dt.strptime("06:30:00", time_f),
                dt.strptime("15:51:00", time_f)
                ],
                
            "timeBreak":{
                "one":"45",
                "two":"48"
            }

        }

days_off = [
    "01-01-23", "09-04-23", 
    "10-04-23","01-05-23",
    "08-05-23", "18-05-23",
    "29-05-23", "14-07-23",
    "15-08-23", "11-11-23",
    "25-12-23", "01-11-23"
    ]

class WorkTime(object):
    def __init__(self, start, end):
        assert end in ["14:51:00", "00:09:00", "15:51:00"],\
            "end is fix and must be in  [14:51:00, 00:09:00, 15:51:00]"
        self.start = dt.strptime(start, time_f) 
        self.end = dt.strptime(end, time_f)
       
    def timedelta_(self, start=None,end=None):
        """
        without parms, take init func parms.
        return time delay bettween two time by substracting the time pause.
        """
        if start and end:
            assert end in ["14:51:00", "00:09:00", "15:51:00"],\
            "end is fix and must be in  [14:51:00, 00:09:00, 15:51:00]"

            self.end, self.start = dt.strptime(end, time_f), dt.strptime(start, time_f)
        tmp = self.end - self.start
        if tmp.total_seconds() > int(self.breakTime().total_seconds()) :
            tmp -= self.breakTime()
        return tmp

    def breakTime(self, days=False):
        """Return the corresponding pause between two times
        """
        start_td = td(hours=self.start.hour, minutes=self.start.minute, seconds=self.start.second)
        end_td =  td(hours=self.end.hour, minutes=self.end.minute, seconds=self.end.second)
        L = workTimeInfo["Fri"] 
        t1 = td(hours=L[0].hour, minutes=L[0].minute, seconds=L[0].second)
        t2 = td(hours=L[1].hour, minutes=L[1].minute, seconds=L[1].hour)
        if  t1 <= start_td <= t2 and t1 <= end_td:
            time_b =  td(minutes=int(workTimeInfo["timeBreak"]["one"]))
        else:
            time_b = td(minutes=int(workTimeInfo["timeBreak"]["two"]), days=-1)
        return time_b


    def nb_days(self, date1, date2):
        """
        Returns:
            Type: (total_days, nb_days_off)
        Return a couple in which:
                total_days: nb days bettween two date,counting days off
                nb_days_off: nb days off between the two dates
        """
        nb_days_off = 0
        date1, date2 = dt.strptime(date1, date_f).date(), dt.strptime(date2, date_f).date()
        assert date2 > date1 and not(date1  in days_off), "date2 must be greater than date1 or date1 is dayoff"
        date_td = date2 - date1
        for day in days_off:
            if  date1 <= dt.strptime(day, date_f).date() <= date2:
                nb_days_off += 1
        return (date_td.days, nb_days_off)

    def hrs_2dates(self, date1, date2):
        """Return The total time of work between two date
        """
        date_td, nb_days_off = self.nb_days(date1, date2)
        total_time_b_second = ((date_td - nb_days_off)*self.timedelta_().total_seconds())
        hrs, rem = divmod(total_time_b_second, 3600)
        mins, seconds = divmod(rem, 60)
        return f"{int(hrs)}:{int(mins):02d}:{int(seconds):02d}"



if __name__ == "__main__":
    wk = WorkTime(start="14:51:00", end="00:09:00")
    print("timedelta", wk.timedelta_())
    # print(wk.breakTime())
    # print(wk.nb_days("04-01-23", "25-12-23"))
    # print(wk.hrs_2dates("04-01-23", "25-12-23"))
    print(wk.breakTime())
