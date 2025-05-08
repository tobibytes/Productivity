import datetime

class Semester:
    start_date: datetime.datetime = datetime.datetime(2024, 10, 1)
    end_date: datetime.datetime = datetime.datetime(2025, 5, 30)


    def check_in_semester(date: str) -> bool:
        """
        Check if the given date is within the semester range.
        """
        date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        return Semester.start_date <= date <= Semester.end_date
    def get_cur_semester() -> str:
        """
        Get the current semester based on the start and end dates.
        """
        return "Spring 2025"