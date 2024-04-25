import csv

from tools.dir_tools import check_file_exist


class CSVManager:
    def __init__(self, csv_filename):
        self.csv_file = None
        self.writer = None
        self.csv_filename = csv_filename

    def open_csv_file(self, mode):
        return open(self.csv_filename, mode, encoding="utf-8", newline="")

    def close_csv_file(self):
        self.csv_file.close()

    def writer_row_csv(self,data):
        self.writer.writerow(data)

    def writer_file_csv(self):
        self.writer = csv.writer(self.csv_file)

    def create_header(self, file_exists, header):
        self.writer_file_csv()
        if header and not file_exists:
            self.writer_row_csv(header)

    def create_file_csv(self, header=None):
        file_exists = check_file_exist(self.csv_filename)
        mode = 'a' if file_exists else 'w'
        self.csv_file = self.open_csv_file(mode)
        self.create_header(file_exists, header)

