from tools import ZipCsvGenerator

if __name__ == '__main__':
    zip_dir = 'zip_dir'
    csv_dir = 'csv_dir'
    zip_count = 1

    zcg = ZipCsvGenerator(zip_dir, csv_dir)

    zcg.generate_zip_files(zip_count)
    zcg.generate_csv_files()
