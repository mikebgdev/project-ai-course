import csv

from tools.dit_tools import check_file_exist


class CSVFileManager:
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename

    def open_csv_file(self, mode):
        return open(self.csv_filename, mode, encoding="utf-8", newline="")

    def close_csv_file(self, csv_file):
        csv_file.close()

    def writer_row_csv(self, csv_writer, data):
        csv_writer.writerow(data)

    def writer_file_csv(self, csv_file):
        return csv.writer(csv_file)

    def create_header(self, csv_file, file_exists, header):
        csv_writer = csv.writer(csv_file)
        if header and not file_exists:
            self.writer_row_csv(csv_writer, header)

    def create_file_csv(self, header=None):
        file_exists = check_file_exist(self.csv_filename)
        mode = 'a' if file_exists else 'w'
        csv_file = self.open_csv_file(mode)
        self.create_header(csv_file, file_exists, header)
        return csv_file
