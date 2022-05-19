from PySide2.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidgetItem, QVBoxLayout, QTableWidget, QListWidgetItem, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtGui import *
import os
import subprocess
import xlrd
from threading import  Thread

class Table_det:

    def __init__(self):
        self.image_dir = ""
        self.file_num = 0

        self.ui = QUiLoader().load('ui/main.ui')
        self.checking = QUiLoader().load('ui/checking.ui')

        self.ui.file_dir.clicked.connect(self.select_file_dir)
        self.ui.check_start.clicked.connect(self.start)
        self.ui.save.clicked.connect(self.save)
        self.ui.listWidget.itemClicked.connect(self.select_image)

        self.window_set()

    def window_set(self):
        self.ui.model_select.addItems(["MyOCRModel", "PaddleOCRModel"])

        # 设置图标
        self.ui.file_dir.setIcon(QIcon("icons/file.png"))
        # 设置图标大小
        self.ui.file_dir.setIconSize(QSize(30, 30))

    def save(self):
        QMessageBox.information(
            self.ui,
            '保存',
            '识别结果已保存至：' + self.image_dir + '/table')

    def select_file_dir(self):
        self.ui.listWidget.clear()
        self.file_num = 0

        path = QFileDialog.getExistingDirectory(self.ui, "选择存储路径")
        path.replace('\\', '/')
        self.image_dir = path
        print(path)
        files = os.listdir(path)
        for f in files:
            if ((f.find(".png") != -1)) :
                icon = QIcon("icons/Auto.png")
                item = QListWidgetItem()
                item.setIcon(icon)
                item.setText(f)
                self.ui.listWidget.addItem(item)
                self.file_num += 1
                print(f)

    def start(self):
        order = "python "
        predict = "PaddleOCR/ppstructure/predict_system.py "
        det = "--det_model_dir=PaddleOCR/inference/det_DB "
        rec = "--rec_model_dir=PaddleOCR/inference/ch_ppocr_server_v2.0_rec_infer "
        table = "--table_model_dir=PaddleOCR/inference/en_ppocr_mobile_v2.0_table_structure_infer "
        image = "--image_dir=" + self.image_dir + " "
        rec_char = "--rec_char_dict_path=PaddleOCR/ppocr/utils/ppocr_keys_v1.txt "
        table_char = "--table_char_dict_path=PaddleOCR/ppocr/utils/dict/table_structure_dict.txt "
        output = "--output=" + self.image_dir + "/table "
        vis = "--vis_font_path=PaddleOCR/doc/fonts/simfang.ttf"

        #ret = os.system(order + predict + det + rec + table + image + rec_char + table_char + output + vis)
        cmd = order + predict + det + rec + table + image + rec_char + table_char + output + vis

        print(cmd)

        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding='utf8',
            bufsize=1
        )

        self.checking.progressBar.setRange(0, self.file_num)
        self.checking.show()

        def workerThreadFunc():
            self.checking.textBrowser.append("正在初始化检测环境，请稍等...")
            self.checking.textBrowser.ensureCursorVisible()
            i = 1
            while subprocess.Popen.poll(p) is None:
                stream = p.stdout.readline()
                if (stream.find("png") != -1):
                    print(stream)
                    self.checking.progressBar.setValue(i)
                    i += 1
                    self.checking.textBrowser.append(stream)
                    self.checking.textBrowser.ensureCursorVisible()

            self.checking.progressBar.setValue(self.file_num)
            self.checking.textBrowser.append("检测完成!")
            self.checking.textBrowser.ensureCursorVisible()

        worker = Thread(target=workerThreadFunc)
        worker.start()

    def select_image(self):
        file = self.ui.listWidget.currentItem().text()
        print("select " + file)
        path = self.image_dir + '/' + file
        img = QPixmap(path)
        img = img.scaled(self.ui.image.size(), aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)

        self.ui.image.setPixmap(img)

        file_name = file.split('.')
        #print(file_name)
        self.select_table(file_name[0])

    def select_table(self, file_name):
        output = self.image_dir + "/table/structure/"
        path = output + file_name
        if(not os.path.exists(path)):
            self.ui.tableWidget.setRowCount(1)
            self.ui.tableWidget.setColumnCount(1)
            self.ui.tableWidget.setColumnWidth(0, 180)
            self.ui.tableWidget.setItem(0, 0, QTableWidgetItem(str("该图片未进行表格检测")))
            return
        files = os.listdir(path)
        i = 1
        for f in files:
            if(f.find(".xlsx") != -1):
                file = path + "/" + f
                if(i == 1):
                    self.show_table(file, self.ui.tableWidget)
                    i += 1
                else:
                    tableWidget = QTableWidget()
                    self.show_table(file, tableWidget)
                    t = QWidget()
                    layout = QVBoxLayout()
                    layout.addWidget(tableWidget)
                    t.setLayout(layout)
                    tab_name = "Tab" + str(i)
                    self.ui.tabWidget.addTab(t, tab_name)
                    i += 1

    def show_table(self, path, tableWidget):
        print(path)
        excel = xlrd.open_workbook(path)  # 打开文件并返回一个工作蒲对象
        sheet_num = excel.nsheets  # 获取excel里面的sheet的数量
        sheet_names = excel.sheet_names()  # 获取到Excel里面所有的sheet的名称列表，即使没有sheet也能用。
        sheet = excel.sheet_by_index(0)  # 通过索引的方式获取到某一个sheet，也可以通过sheet的名称进行获取，sheet_by_name('sheet名称')
        rows = sheet.nrows  # 获取sheet页的行数，一共有几行
        columns = sheet.ncols  # 获取sheet页的列数，一共有几列

        tableWidget.setRowCount(rows)
        tableWidget.setColumnCount(columns)

        for i in range(0, rows):
            for j in range(0, columns):
                cell = sheet.cell(i, j)
                val = cell.value
                tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

        tableWidget.horizontalHeader().setStretchLastSection(True)


app = QApplication([])
table = Table_det()
table.ui.show()
app.exec_()