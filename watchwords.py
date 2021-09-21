import csv

class Watchwords:
    def __init__(self, name, words, report) -> None:
        self.name = name 
        self.words = words
        self.report = report
        self.log = []
    
    
    def write_report(self, write_path):
        with open(write_path, 'a', newline='') as csvf:
            reportwriter = csv.writer(csvf)
            if len(self.report):
                reportwriter.writerow(['ENTRY NUMBER', 'KEYWORK LIST NAME', 'WORD FOUND IN FILE', 'FILE WORD FOUND IN', 'LINE IN FILE'])
                for i, row in enumerate(self.report):
                    print(type(row))
                    reportwriter.writerow([i, row[0], row[1], row[2], row[3]])
            else:
                reportwriter.writerow([0,f'{len(self.words)} words were searched from the {self.name} keyword list and no matches for them were found in the searched files. Please examine log file for informaiotn on diectories thatt wrre not searched by KAPE'])
    
    def write_error_logs(self, write_path):
        with open(write_path, 'a', newline='') as csvf:
            reportwriter = csv.writer(csvf)
            if len(self.log):
                for i, row in enumerate(self.log):
                    reportwriter.writerow([i, row])
