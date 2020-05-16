from General import Functions


class TimeRange:

    def __init__(self, start_time, end_time):

        self.start_time = start_time    # these are datetime.datetime objects
        self.end_time = end_time
        self.delta = self.get_delta()

    def get_delta(self):
        return self.end_time - self.start_time

    def __str__(self):
        return "{} - {}".format(Functions.get_nice_time_format(self.start_time),
                                Functions.get_nice_time_format(self.end_time))
