from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
import sys
from form import Ui_MainWindow
from PyPDF2 import PdfReader, PdfWriter
import os
from pathlib import Path

class UI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setupUi(self)
        

        self.browse_btn.clicked.connect(self.choose_pdf)


        self.show()

    def choose_pdf(self):
        fname = QFileDialog.getOpenFileName(self, "Choose a PDF File", "", "PDF File (*.pdf)")
        
        if fname:
            filename = fname[0]
            if filename.endswith(".pdf"):
                self.directory_line.setText(filename)

                
                reader = PdfReader(filename)
                basepath = os.path.splitext(filename)[0]
                directory_name = os.path.dirname(filename)
                basename = Path(filename).stem

                new_folder  = os.path.join(directory_name, basename)
                execute = False
                if os.path.exists(new_folder):

                    mssg = QMessageBox.question(self,"",  "Do you Want to Extract into the Existing Folder: " + new_folder + "?", QMessageBox.Yes | QMessageBox.No )

                    if mssg:
                        execute = True
                    else:
                        execute = False
                else:

                    os.mkdir(new_folder)


                if execute:


                    for i, page in enumerate(reader.pages):
                        writer = PdfWriter()
                        writer.add_page(page)


                        
                    
                        extracted_file_name = basename + "_" + str(i).zfill(3) + ".pdf"

                        extracted_file_path = os.path.join(new_folder, extracted_file_name)

                        print(extracted_file_path)


                        with open(extracted_file_path, "wb", i) as a:
                            writer.write(a)
                            a.close()





app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
