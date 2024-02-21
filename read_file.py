from datetime import datetime
import os
import pandas as pd
import re


SALES = "sales_report"
INVENTORY = "inventory_report"


class Metadata:
    """
    Parses Poshmark's sales_activity_report.csv to get `username` and the `sr_start_date`, `sr_end_date` and creates `output_folder` if it doesn't exist
    ex.:
    gets data:
        str(): closet = [<@username>] on the first line
        str(): dates from period = [01.01.2019-12.31.2019] on the 2nd line. THIS LINE MUST BE PRESENT, DO CHECK ON THE PURCHASE STAGE
    to call:
        import read_file as rf
        rf.Metadata.parse_report('test_files/inventory_activity_report.csv')

    INPUTS:
    :filename = 'test_files/inventory_activity_report.csv'
    :filename = 'test_files/sales_activity_report.csv'  # where 'username' 12312019 - 11222020
    :output_folder = 'client_' + 'username'; inside of a parent folder (from an input file)
    :sr_period = (.../2019, .../2020); gets the dates from file
    :ir_date str(): "2020/11/23"; gets it from file

    test18: 
        'test_files/sales_activity_report (1)-01_01_2018 - 12_31_2018 - sales_activity_report.csv'
    """

    def __init__(self):
        self.username = None
        self.sr_name = None  # sales_report
        self.ir_name = None  # inventory_report
        self.ir_date = None
        self.sr_start_date = None
        self.sr_middle_date = None
        self.sr_end_date = None
        self.sr_period = None
        self.filename = None
        self.output_folder = "test_files/client_"

    def report_type(self):
        if self.sr_name and not self.ir_name:
            return SALES
        elif self.ir_name and not self.sr_name:
            return INVENTORY
        else:
            return None

    @staticmethod
    def parse_report(csv_file, output_folder=None):  # this method works for both reports
        report = Metadata()
        with open(csv_file, newline='') as f:
            line_count = 0
            while line_count < 10:
                line = f.readline()
                if line is None:
                    raise Exception("Reached 'End-of-file' in less then 10 lines")
                else:
                    line_count += 1
                    sr = re.search(r'(Poshmark Sales Report)+', line)
                    ir = re.search(r'(Poshmark Inventory Report)+', line)
                    n = re.search(r'@([^ ,"\'\n]+)', line)
                    d = re.search(r'^([\d/]+)[- ]+([\d/]+)', line)
                    di = re.search(r'Inventory as of ([\d/]+)', line)
                    if sr:
                        report.sr_name = sr.group(1)
                    if ir:
                        report.ir_name = ir.group(1)
                    if n:
                        report.username = n.group(1)
                        report.output_folder = report.output_folder + report.username
                    if d:
                        report.sr_start_date = d.group(1)
                        report.sr_end_date = d.group(2)
                        report.sr_period = report.sr_start_date, report.sr_end_date
                        datetime_obj_start = datetime.strptime(report.sr_start_date, '%m/%d/%Y')  # str 'date' => into datetime_obj
                        datetime_obj_end = datetime.strptime(report.sr_end_date, '%m/%d/%Y')
                        report.sr_middle_date = datetime_obj_start + ((datetime_obj_end - datetime_obj_start) / 2)  
                    if di:
                        report.ir_date = di.group(1)
        # Get the absolute path to the running file (w/out a filename, just a path) str()
        path = os.path.dirname(os.path.abspath(csv_file))

        # Get the file name of the running file
        report.filename = os.path.basename(csv_file)  # str() of just a filename with '.csv'

        if not report.username:
            raise Exception("username can't be none!")  # it can't be None, it will be used below
        # check if ('parent dir' + 'output_folder dir') exists 
        if output_folder:
            report.output_folder = output_folder
        else:  # this is for local runs
            output_folder_path = os.path.join(path, "../" + report.output_folder)  # TODO cleanup
            if not os.path.isdir(output_folder_path):
                os.mkdir(output_folder_path)
                print("Directory '{}' created".format(report.output_folder))

        return report

    def get_username(self, csv_file): 
        report = self.parse_report(csv_file)
        return report.username


def load_df(filename, meta):
    """
    :param filename: file.csv, where 'file' is sales_report or inventory_report. ex. 'folder/file.csv'
    :param meta: Metadata's class instance
    :return pandas.df obj: cleaned up from Posh notes, without overhead header & a footer of totals.
    ex.
        sr_filename = 'test_files/sales_activity_report.csv' # where: username, 12312019 - 11222020
        inventory_report = pd.read_csv(ir_filename, skiprows=6, header=0, engine='python')
    """
    if meta.sr_name:
        return pd.read_csv(filename, skiprows=10, skipfooter=1, engine='python')
    if meta.ir_name:
        return pd.read_csv(filename, skiprows=6, header=0, engine='python')
