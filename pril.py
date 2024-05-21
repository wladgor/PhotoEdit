import sqlite3
import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QLabel, QVBoxLayout, QSizePolicy, \
    QWidget

from UI.About import Ui_Form9
from UI.ChoiceMain import Ui_ChoiceMain
from UI.History import Ui_Form
from UI.MainWindow import Ui_MainWindow
from UI.Met1 import Ui_Form1
from UI.Met2 import Ui_Form2
from UI.Met3 import Ui_Form3
from UI.Met4 import Ui_Form4
from UI.Met5 import Ui_Form5
from UI.Met6 import Ui_Form6
from UI.Met7 import Ui_Form7
from scripts import met1rot, met2nas, met3gran, met4ava, met5txt, met6nal, met7rgb


# Главное окно
class MainWindows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Главное окно')
        self.setFixedSize(469, 365)

        self.Start.clicked.connect(self.choice_main)
        self.Exit.clicked.connect(self.close_now)
        self.ImWatch.clicked.connect(self.open_image)
        self.Oprog.clicked.connect(self.about)
        self.BDhis.clicked.connect(self.his)

    def open_image(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Открыть изображение', '', \
                                                  'Изображения (*.png *.jpg *.jpeg *.bmp *.gif)')
        if filePath:
            self.imageWindow = ImageWindow(filePath)
            self.imageWindow.show()

    def close_now(self):
        app.quit()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Вы уверенны?', 'Вы уверены, что хотите закрыть программу?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            app.quit()
        else:
            event.ignore()

    def choice_main(self):
        self.setEnabled(False)
        self.choice_main_show = ChoiceMain()
        self.choice_main_show.show()
        self.choice_main_show.closing.connect(self.return_work_after_close)

    def return_work_after_close(self):
        self.setEnabled(True)

    def about(self):
        self.setEnabled(False)
        self.choice_main_show = AboutWindow()
        self.choice_main_show.show()
        self.choice_main_show.closing.connect(self.return_work_after_close)

    def his(self):
        self.setEnabled(False)
        self.choice_main_show = HistoryViever()
        self.choice_main_show.show()
        self.choice_main_show.closing.connect(self.return_work_after_close)


# Окно о программе
class AboutWindow(QWidget, Ui_Form9):
    closing = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('О программе')
        self.setFixedSize(729, 350)
        self.Pashalka.clicked.connect(self.easter_egg)
        self.Exit.clicked.connect(self.close_button)
        self.Pashalka.setVisible(False)

    def close_button(self):
        self.closing.emit()
        self.close()

    def easter_egg(self):
        QMessageBox.information(self, "Пасхалка", "Ура! Вы нашли пасхалку!")

    def closeEvent(self, event):
        self.closing.emit()
        self.close()


# Редактор историй
class HistoryViever(QWidget, Ui_Form):
    closing = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Редактор историй')
        self.Exit.clicked.connect(self.close_button)
        self.dela.clicked.connect(self.delete)
        self.redac.clicked.connect(self.redact_action)

        self.db_connection = sqlite3.connect('mydatabase.db')
        self.create_table_if_not_exists()

        self.load_data_into_table()

    def create_table_if_not_exists(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
               CREATE TABLE IF NOT EXISTS file_paths (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   file_path TEXT,
                   directory_path TEXT
               )
           ''')
        self.db_connection.commit()

    def load_data_into_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM file_paths')
        data = cursor.fetchall()

        self.model = QStandardItemModel(len(data), 3)
        self.model.setHorizontalHeaderLabels(['ID', 'File Path', 'Directory Path'])

        for row, record in enumerate(data):
            for col, value in enumerate(record):
                item = QStandardItem(str(value))
                self.model.setItem(row, col, item)

        self.tabl.setModel(self.model)

    def redact_action(self):
        selected_index = self.tabl.selectionModel().currentIndex()
        new_value = self.linetxt.text()

        if selected_index.isValid() and new_value:
            row = selected_index.row()
            col = selected_index.column()
            id_item = self.model.item(row, 0)
            if id_item and col > 0:
                record_id = int(id_item.text())

                # Обновление в модели
                self.model.setItem(row, col, QStandardItem(new_value))

                # Обновление в базе данных
                column_name = 'file_path' if col == 1 else 'directory_path'
                cursor = self.db_connection.cursor()
                cursor.execute(f'UPDATE file_paths SET {column_name} = ? WHERE id = ?', (new_value, record_id))
                self.db_connection.commit()

    def delete(self):
        selected_index = self.tabl.selectionModel().currentIndex()
        if selected_index.isValid():
            row = selected_index.row()
            id_item = self.model.item(row, 0)
            if id_item:
                record_id = int(id_item.text())

                # Удаление из базы данных
                cursor = self.db_connection.cursor()
                cursor.execute('DELETE FROM file_paths WHERE id = ?', (record_id,))
                self.db_connection.commit()

                # Удаление из модели
                self.model.removeRow(row)

    def close_button(self):
        self.closing.emit()
        self.close()

    def closeEvent(self, event):
        self.closing.emit()
        self.close()


# Просмотр изображений
class ImageWindow(QWidget):
    def __init__(self, image_path, parent=None):  # image_path обязателен

        super().__init__(parent)
        self.setWindowTitle('Просмотр изображения')

        self.imageLabel = QLabel(self)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        pixmap = QPixmap(image_path)

        self.imageLabel.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        self.setLayout(layout)

        self.resize(pixmap.width(), pixmap.height())

        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())


# Меню выбора
class ChoiceMain(QMainWindow, Ui_ChoiceMain):
    closing = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Выберете опцию')
        self.setFixedSize(480, 289)
        self.Exit.clicked.connect(self.close_button)

        self.met_buttons = {
            self.Met1: Met1,
            self.Met2: Met2,
            self.Met3: Met3,
            self.Met4: Met4,
            self.Met5: Met5,
            self.Met6: Met6,
            self.Met7: Met7

        }

        for button, met_class in self.met_buttons.items():
            button.clicked.connect(lambda _, met_class=met_class: self.open_met(met_class))

    def open_met(self, MetClass):
        self.setEnabled(False)
        self.child_window = MetClass()
        self.child_window.show()
        self.child_window.closing.connect(self.return_work_after_close)

    def closeEvent(self, event):
        self.closing.emit()

    def close_button(self):
        self.close()

    def return_work_after_close(self):
        self.setEnabled(True)


# Родительский класс
class Format(QMainWindow):
    closing = pyqtSignal()

    # К величайшему сожалению нельзя засунуть в родительский класс кнопки например pngr или exit. Как бы я не старался
    def __init__(self):
        super().__init__()
        self.fname = None
        self.directory = None
        self.db_connection = None
        self.create_db_connection()

        self.show_dialogs()

    def create_db_connection(self):
        self.db_connection = sqlite3.connect('mydatabase.db')
        self.create_table_if_not_exists()

    def show_dialogs(self):
        fname, _ = QFileDialog.getOpenFileName(
            None, 'Выберите изображение', '',
            'Изображение (*.png *.jpg);;Все файлы (*)')

        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(None, 'Выберите директорию или папку для сохранения', '',
                                                     options=options)

        if fname and directory:
            self.handle_dialog_result(fname, directory)
            self.create_table_if_not_exists()
        else:  # Что я только не перепробовал: флаги, проверки, return, close и так далее. Всё бесполезно. Прийдется
            # использовать костыль
            QMessageBox.critical(self, 'Ошибка',
                                 'Не выбран файл или директория. Программа не сможет продолжить работу. Пожалуйста, выйдите из окна и введите данные')

    def create_table_if_not_exists(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_paths (
                id INTEGER PRIMARY KEY,
                file_path TEXT,
                directory_path TEXT
            )
        ''')
        self.db_connection.commit()

    def handle_dialog_result(self, fname, directory):
        self.fname = fname
        self.directory = directory
        self.insert_path_to_db(fname, directory)

    def insert_path_to_db(self, fname, directory):
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO file_paths (file_path, directory_path) VALUES (?, ?)', (fname, directory))
        self.db_connection.commit()

    def set_rash(self, rash):
        self.rash = rash

    def clear_text(self, line_edit):
        line_edit.clear()

    def close_button(self):
        self.closing.emit()
        self.close()

    def closeEvent(self, event):
        self.closing.emit()
        self.close()


# Далее методы
class Met1(Format, Ui_Form1):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle('Поворот изображения')
        self.setFixedSize(276, 296)
        self.Val1.clicked.connect(lambda: self.val(1))
        self.Val2.clicked.connect(lambda: self.val(2))
        self.Val3.clicked.connect(lambda: self.val(3))
        self.Val4.clicked.connect(lambda: self.val(4))
        self.Val5.clicked.connect(lambda: self.val(5))
        self.rash = ''
        self.pngr.clicked.connect(lambda: self.set_rash('.png'))
        self.jpgr.clicked.connect(lambda: self.set_rash('.jpg'))
        self.NameSohr.mousePressEvent = lambda event: self.clear_text(self.NameSohr)
        self.Exit.clicked.connect(self.close_button)

    def val(self, rotation):
        try:
            self.text = str(self.NameSohr.text()) + str(self.rash)
            met1rot(rotation, self.text, self.fname, self.directory)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, введите все данные во все окна')


class Met2(Format, Ui_Form2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Настройка изображения')
        self.setFixedSize(389, 363)
        self.Val1.clicked.connect(lambda: self.val(1))
        self.Val2.clicked.connect(lambda: self.val(2))
        self.Val3.clicked.connect(lambda: self.val(3))
        self.Val4.clicked.connect(lambda: self.val(4))
        self.Val5.clicked.connect(lambda: self.val(5))
        self.Val6.clicked.connect(lambda: self.val(6))
        self.Val7.clicked.connect(lambda: self.val(7))
        self.Val8.clicked.connect(lambda: self.val(8))
        self.NameSohr.mousePressEvent = lambda event: self.clear_text(self.NameSohr)
        self.Exit.clicked.connect(self.close_button)
        self.rash = ''
        self.pngr.clicked.connect(lambda: self.set_rash('.png'))
        self.jpgr.clicked.connect(lambda: self.set_rash('.jpg'))

    def val(self, rotation):
        try:
            self.text = str(self.NameSohr.text()) + str(self.rash)
            met2nas(rotation, self.text, self.fname, self.directory)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, введите все данные во все окна')


class Met3(Format, Ui_Form3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Нахождение границ и их тиснение')
        self.setFixedSize(290, 209)
        self.Val1.clicked.connect(self.val)
        self.Exit.clicked.connect(self.close_button)
        self.NameSohr.mousePressEvent = lambda event: self.clear_text(self.NameSohr)
        self.rash = ''
        self.pngr.clicked.connect(lambda: self.set_rash('.png'))
        self.jpgr.clicked.connect(lambda: self.set_rash('.jpg'))

    def val(self):
        try:
            self.text = str(self.NameSohr.text()) + str(self.rash)
            met3gran(self.text, self.fname, self.directory)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, введите все данные во все окна')


class Met4(Format, Ui_Form4):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Скругление изображения')
        self.setFixedSize(228, 201)
        self.Val1.clicked.connect(self.val)
        self.Exit.clicked.connect(self.close_button)
        self.NameSohr.mousePressEvent = lambda event: self.clear_text(self.NameSohr)

    def val(self):
        try:
            self.text = str(self.NameSohr.text()) + '.png'
            met4ava(self.text, self.fname, self.directory)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, введите все данные во все окна')


class Met5(Format, Ui_Form5):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Добавление текста')
        self.setFixedSize(590, 337)
        self.Val1.clicked.connect(lambda: self.val(1))
        self.Val2.clicked.connect(lambda: self.val(2))
        self.Val3.clicked.connect(lambda: self.val(3))
        self.Val4.clicked.connect(lambda: self.val(4))
        self.Val5.clicked.connect(lambda: self.val(5))
        self.CustomShrift.clicked.connect(self.custom_shrift)
        self.Exit.clicked.connect(self.close_button)

        self.rash = ''
        self.shrift = ''
        self.shrift_flag = False
        self.pngr.clicked.connect(lambda: self.set_rash('.png'))
        self.jpgr.clicked.connect(lambda: self.set_rash('.jpg'))
        self.RazmTxt.mousePressEvent = lambda event: self.clear_text(self.RazmTxt)
        self.Text.mousePressEvent = lambda event: self.clear_text(self.Text)
        self.NameSohr.mousePressEvent = lambda event: self.clear_text(self.NameSohr)
        self.ShriftCombo.model().item(0).setEnabled(False)
        self.ShriftCombo.activated.connect(self.combo_choice)

    def combo_choice(self):
        if self.shrift_flag:
            QMessageBox.question(self, 'Внимание!', 'Внимание! Шрифт будет заменён',
                                 QMessageBox.Ok)
        self.shrift = str(self.ShriftCombo.currentText())
        self.shrift_flag = True

    def custom_shrift(self):
        if self.shrift_flag:
            QMessageBox.question(self, 'Внимание!', 'Внимание! Шрифт будет заменён',
                                 QMessageBox.Ok)
        ffname, _ = QFileDialog.getOpenFileName(
            self, 'Выберите шрифт', '',
            'Шрифт (*.ttf);;Все файлы (*)')

        if ffname:
            self.shrift = ffname
            self.shrift_flag = True
            self.ShriftCombo.setCurrentIndex(0)
        else:
            self.shrift = ''
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, выберите шрифт')
            self.shrift_flag = False
            self.ShriftCombo.setCurrentIndex(0)

    def val(self, rotation):
        if not self.shrift_flag:
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, выберите шрифт')
        else:
            try:
                self.text = str(self.NameSohr.text()) + str(self.rash)
                self.razm = int(self.RazmTxt.text())
                self.txt = str(self.Text.text())
                self.sh = str(self.shrift)
                met5txt(rotation, self.razm, self.sh, self.txt, self.text, self.fname, self.directory)
                self.close()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, введите все данные во все окна')


class Met6(Format, Ui_Form6):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Наложение водяного знака')
        self.setFixedSize(306, 458)
        self.Val1.clicked.connect(lambda: self.val(1))
        self.Val2.clicked.connect(lambda: self.val(2))
        self.Val3.clicked.connect(lambda: self.val(3))
        self.Val4.clicked.connect(lambda: self.val(4))
        self.Val5.clicked.connect(lambda: self.val(5))
        self.VaterMark.clicked.connect(self.vater_mark_choice)
        self.Exit.clicked.connect(self.close_button)
        self.NameSohr.mousePressEvent = lambda event: self.clear_text(self.NameSohr)

    def vater_mark_choice(self):
        self.vatermarkname = str(QFileDialog.getOpenFileName(
            self, 'Выберите изображение', '',
            'Изображение (*.png);;Все файлы (*)')[0])

    def val(self, rotation):
        try:
            self.text = str(self.NameSohr.text()) + '.png'
            met6nal(rotation, self.vatermarkname, self.text, self.fname, self.directory)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, введите все данные во все окна')


class Met7(Format, Ui_Form7):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Изменение последовательности каналов RGB или выделение определённых')
        self.setFixedSize(408, 375)
        self.Val1.clicked.connect(lambda: self.val(1))
        self.Val2.clicked.connect(lambda: self.val(2))
        self.Val3.clicked.connect(lambda: self.val(3))
        self.Val4.clicked.connect(lambda: self.val(4))
        self.Val5.clicked.connect(lambda: self.val(5))
        self.Val6.clicked.connect(lambda: self.val(6))
        self.Val7.clicked.connect(lambda: self.val(7))
        self.Val8.clicked.connect(lambda: self.val(8))
        self.Exit.clicked.connect(self.close_button)
        self.NameSohr.mousePressEvent = lambda event: self.clear_text(self.NameSohr)
        self.rash = ''
        self.pngr.clicked.connect(lambda: self.set_rash('.png'))
        self.jpgr.clicked.connect(lambda: self.set_rash('.jpg'))

    def val(self, rotation):
        try:
            self.text = str(self.NameSohr.text()) + str(self.rash)
            met7rgb(rotation, self.text, self.fname, self.directory)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, введите все данные во все окна')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindows()
    main_window.show()
    sys.exit(app.exec_())
