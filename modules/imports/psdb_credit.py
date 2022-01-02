import calendar
import csv
from datetime import date, datetime
from io import StringIO
import xlrd
import eml_parser
from beancount.core import data
from beancount.core.data import Note, Transaction
from bs4 import BeautifulSoup
import dateparser
from . import (DictReaderStrip, get_account_by_guess,
               get_income_account_by_guess)
from .base import Base
from .deduplicate import Deduplicate

AccountAssetUnknown = 'Assets:Unknown'
AccountPSDB = 'Liabilities:CreditCard:PSDB:6061'

class PSDBCredit():

    def __init__(self, filename, byte_content, entries, option_map):
        if not filename.endswith('xls'):
            raise ValueError("Not PSDB!")
        parsed_xls = xlrd.open_workbook_xls(filename)
        sheet_names = parsed_xls.sheet_names()
        if '账单明细' != sheet_names[0]:
            raise ValueError("Not PSDB!")

        content = parsed_xls.sheet_by_index(0)
        self.names = content.row_values(0)
        self.content = content
        self.deduplicate = Deduplicate(entries, option_map)

    def get_currency(self, currency_text):
        if currency_text == "人民币":
            return 'CNY'
        return currency_text

    def parse(self):
        content = self.content
        transactions = []
        for i in range(1, content.nrows):
            row = dict(zip(self.names, content.row_values(i)))
            meta = {}
            time = row['交易日期']
            time_year = int(time[:4])
            time_month = int(time[4:6])
            time_day = int(time[6:])
            # time = time_year + '-' + time_month + '-' + time_day
            description = row['交易摘要']
            print('Importing {} at {}'.format(description, time))
            account = get_account_by_guess(description, description, time)
            flag = "*"
            currency = row['交易币种']
            currency = self.get_currency(currency)
            amount_string = row['交易金额']
            amount = float(amount_string)
            if account == "Unknown":
                flag = "!"

            meta = data.new_metadata(
                'beancount/core/testing.beancount',
                12345,
                meta
            )
            entry = Transaction(
                meta,
                date(time_year, time_month, time_day),
                flag,
                description,
                " ",
                data.EMPTY_SET,
                data.EMPTY_SET, []
            )
            data.create_simple_posting(
                entry, account, amount_string, currency)
            data.create_simple_posting(entry, AccountPSDB, None, None)
            if not self.deduplicate.find_duplicate(entry, -amount, None, AccountPSDB):
                transactions.append(entry)

        self.deduplicate.apply_beans()
        return transactions







# psdb = PSDBCredit('psdb.xls')
# psdb.parse()
