from tools import ZipCsvGenerator

if __name__ == '__main__':
    zip_dir = 'zip_dir'
    csv_dir = 'csv_dir'
    zip_count = 50

    zg = ZipCsvGenerator(zip_dir, csv_dir)

    zg.generate_zip_files(zip_count)
    zg.generate_csv_files()
