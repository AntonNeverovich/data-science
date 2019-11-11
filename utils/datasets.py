import random
from dataclasses import dataclass
from datetime import timedelta, date
import datetime
import numpy as np


@dataclass
class FinancialStability:
    """
    class keeping data for financial stability
    """
    id: int
    date: datetime.date
    own_capital: float
    assets: float
    lt_liabilities: float
    current_liability: float
    current_asset: float
    non_current_assets: float
    long_credits: float

    def __str__(self):
        return f'{self.id}, ' \
               f'{self.date}, '\
               f'{self.own_capital:.2f}, '\
               f'{self.assets:.2f}, '\
               f'{self.lt_liabilities:.2f}, '\
               f'{self.current_liability:.2f}, '\
               f'{self.current_asset:.2f}, '\
               f'{self.non_current_assets:.2f}, '\
               f'{self.long_credits:.2f}\n'


class Personal:
    """
    class keeping data for personal
    """
    id: int
    birth_date: datetime.date
    hiring_date: datetime.date
    dismissal_date: datetime.date
    sex: int  # 0 - male, 1 - female
    qualification: int  # from 0 (low) - 10 (high)
    salary: float
    working_hours: int
    missed_hours: int

    def __init__(self, birth_date, hiring_date, dismissal_date, sex, qualification, salary):
        self.birth_date = birth_date
        self.hiring_date = hiring_date
        self.dismissal_date = dismissal_date
        self.sex = sex
        self.qualification = qualification
        self.salary = salary

    def __str__(self):
        return f'{self.id}, ' \
               f'{self.birth_date}, ' \
               f'{self.hiring_date}, '\
               f'{self.dismissal_date}, '\
               f'{self.sex}, '\
               f'{self.qualification}, '\
               f'{self.salary:.2f}, '\
               f'{self.working_hours}, '\
               f'{self.missed_hours}\n'\


@dataclass
class Investment:
    """
    class keeping data for investments
    """
    id: int
    date: datetime.date
    income: float
    outcome: float
    current_liability: float
    current_asset: float
    long_credits: float

    def __str__(self):
        return f'{self.id}, ' \
               f'{self.date}, '\
               f'{self.income:.2f}, '\
               f'{self.outcome:.2f}, '\
               f'{self.current_liability:.2f}, '\
               f'{self.current_asset:.2f}, '\
               f'{self.long_credits:.2f}\n'


def write_csv(name: str, lines: int):
    file_name = 'data/train/' + name + '.csv'
    file = open(file_name, 'a+')
    title = 'id, Date, Income, Outcome, Long Term Liabilities, Current Liabilities, Current Asset, '\
                'Non Current Asset, Long Credits\n'

    file.write(title)

    first_date = datetime.date(2020, 1, 1)
    lab = 0
    for i in range(lines):
        fs = Investment(
            id=i,
            date=first_date + timedelta(days=i + 1),
            income=random.uniform(1000000 + i * 100, 1500000 + i * 150),
            outcome=random.uniform(1000000 - i * 100, 1500000 - i * 150),
            current_liability=lab,
            current_asset=random.uniform(10000000 + i * 1000, 90000000 + i * 1500),
            long_credits=random.uniform(1000000 + i * 100, 1500000 + i * 150) * 0.33,
        )
        lab += fs.income
        file.write(str(fs))


def write_csv_personal(name: str, first_date, last_date=date.today()):
    file_name = 'data/train/' + name + '.csv'
    file = open(file_name, 'a+')
    file.write(title_csv(Personal))
    if first_date < date.today():
        lines = int((date.today() - first_date).days)
    else:
        lines = int((last_date - date.today()).days)

    for i in range(lines):
        fs = Personal(
            birth_date=first_date + timedelta(days=int(random.uniform(-25550, -6570))),
            hiring_date=first_date + timedelta(days=int(random.triangular(0, 4538, 0))),
            dismissal_date=first_date + timedelta(days=int(random.triangular(0, 4538, 0))),
            sex=int(random.choice([True, False])),
            qualification=int(random.uniform(0, 10)),
            salary=random.triangular(20000 + i * 5, 500000 + i * 60, 90000 + i * 5),
        )
        fs.id = int(abs((fs.__hash__() + random.gauss(fs.__hash__(), 0.75)) / random.randint(100000000, 999999999)))
        experience = int((date.today() - fs.hiring_date).days) * (247 * 8 / 365) if is_working else int((fs.dismissal_date - fs.hiring_date).days) * (247 * 8 / 365)
        fs.missed_hours = int(random.triangular(0, 168, 40))
        fs.working_hours = int(experience - fs.missed_hours)

        file.write(str(fs))


def is_working(dismissed_time):
    return dismissed_time < datetime.datetime.now()


def title_csv(Name):
    keys = list(Name.__dict__['__annotations__'].keys())
    result = ''
    for key in keys:
        result += key + ', '
    return result[:-2] + '\n'


write_csv_personal(name='train_personal', first_date=date(2007, 1, 1))
write_csv_personal(name='test_personal', first_date=date.today(), last_date=date(2021, 12, 31))
