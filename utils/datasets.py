import random
from dataclasses import dataclass
from datetime import timedelta, date
import datetime


@dataclass
class FinancialStability:
    """
    class keeping data for financial stability
    """
    date: datetime.date
    own_capital: float
    borrowed_capital: float
    assets: float
    lt_liabilities: float
    current_liability: float
    current_asset: float
    non_current_assets: float
    long_credits: float

    def __init__(self, date, own_capital, borrowed_capital, current_liability, current_asset, long_credits):
        self.date = date
        self.own_capital = own_capital
        self.borrowed_capital = borrowed_capital
        self.current_liability = current_liability
        self.current_asset = current_asset
        self.long_credits = long_credits

    def __str__(self):
        return f'{self.date}, '\
               f'{self.own_capital:.2f}, '\
               f'{self.borrowed_capital:.2f}, '\
               f'{self.assets:.2f}, '\
               f'{self.lt_liabilities:.2f}, '\
               f'{self.current_liability:.2f}, '\
               f'{self.current_asset:.2f}, '\
               f'{self.non_current_assets:.2f}, '\
               f'{self.long_credits:.2f}\n'


@dataclass
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


def write_csv_finance(name: str, first_date, last_date=date.today()):
    file = open(file_name(name), 'a+')
    file.write(title_csv(FinancialStability))

    if first_date < date.today():
        lines = int((date.today() - first_date).days)
    else:
        lines = int((last_date - date.today()).days)

    for i in range(lines):
        fs = FinancialStability(
            date=first_date + timedelta(days=i+1),
            own_capital=random.uniform(10**7 + i * 10**4, 15**7 + i * 10**4),
            borrowed_capital=random.uniform(7**7 + i * 10**4, 10**7 - i * 10**4),
            current_liability=random.uniform(7**7 + i * 10**7, 10**7 - i * 10**4) * 0.33,
            current_asset=random.uniform(7**7 + i * 10**4, 10**7 - i * 10**4),
            long_credits=random.uniform(7**7 + i * 10**4, 10**7 - i * 10**4) * 0.66,
        )
        fs.assets = 0.5 * fs.own_capital + fs.current_asset
        fs.lt_liabilities = fs.long_credits + fs.current_liability
        fs.non_current_assets = fs.assets - fs.current_asset

        file.write(str(fs))


def write_csv_personal(name: str, first_date, last_date=date.today()):
    file = open(file_name(name), 'a+')
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


def file_name(name: str):
    if 'train' in name:
        return 'data/train/' + name + '.csv'
    elif 'test' in name:
        return 'data/test/' + name + '.csv'
    else:
        return 'data/' + name + '.csv'


# write_csv_personal(name='train_personal', first_date=date(2007, 1, 1))
# write_csv_personal(name='test_personal', first_date=date.today(), last_date=date(2021, 12, 31))
write_csv_finance(name='train_finance', first_date=date(2007, 1, 1))
write_csv_finance(name='test_finance', first_date=date.today(), last_date=date(2021, 12, 31))

