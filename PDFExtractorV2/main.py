from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import QUrl
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
        self.directory_line.setReadOnly(True)
        self.directory_line.mousePressEvent = self.choose_pdf
        self.extract_all_btn.setEnabled(False)
        self.extract_all_btn.clicked.connect(self.extract_all_pages)
        
        self.viewport.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.viewport.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)


        self.show()

    def extract_all_pages(self):


        output_filepath = QFileDialog.getSaveFileName(self, "Extract File Name", "", "PDF File (*.pdf)")

        if output_filepath:

            output_path = os.path.dirname(output_filepath[0])
            output_basename = Path(output_filepath[0]).stem
            output_basepath = os.path.splitext(output_filepath[0])[0]

            basepath = os.path.splitext(self.filename)[0]
            directory_name = os.path.dirname(self.filename)
            basename = Path(self.filename).stem
            
            new_folder  = os.path.join(output_path, output_basename)
            if os.path.exists(new_folder):

                mssg = QMessageBox.question(self,"",  "Do you Want to Extract into the Existing Folder: " + output_basepath + "?", QMessageBox.Yes | QMessageBox.No )

                if mssg:
                    execute = True
                else:
                    execute = False
            else:

                os.mkdir(new_folder)
                execute = True


            if execute:


                for i, page in enumerate(self.reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)


                    
                
                    extracted_file_name = output_basename + "_" + str(i).zfill(3) + ".pdf"

                    extracted_file_path = os.path.join(new_folder, extracted_file_name)

                    print(extracted_file_path)


                    with open(extracted_file_path, "wb", i) as a:
                        writer.write(a)
                        a.close()


    def choose_pdf(self, e):
        fname = QFileDialog.getOpenFileName(self, "Choose a PDF File", "", "PDF File (*.pdf)")
        
        if fname:

            self.filename = fname[0]
            if self.filename.endswith(".pdf"):

                self.extract_all_btn.setEnabled(True)
                self.directory_line.setText(self.filename)

                self.viewport.load(QUrl.fromLocalFile(self.filename))
                
                self.reader = PdfReader(self.filename)






app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
