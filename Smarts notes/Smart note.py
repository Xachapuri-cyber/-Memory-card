from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLineEdit, QListWidget, QTextEdit, QWidget, QPushButton, QHBoxLayout, QInputDialog, QLabel, QVBoxLayout
from random import randint

import json

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"]=field_text.toPlainText()
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)



def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def add_note():
    note_name, ok = QInputDialog.getText(
        main_win, "Добавить заметку", "Название заметки: "
    )
    if ok and note_name != "":
        notes[note_name] = {"текст" : "", "теги" : []}
        list_notes.addItem(note_name)
def show_note():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[name]["теги"])

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes.json", "w")as file:
            json.dump(notes, file, sort_keys=True)

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes.json", "w")as file:
            json.dump(notes, file, sort_keys=True)

def search_tag():
    tag = field_tag.text()
    if btn_search_tag.text() == "Искать по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes [note]["теги"]:
                notes_filtered[note]=notes[note]
        btn_search_tag.setText("Cбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif btn_search_tag.text() == "Сбросить поиск":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        btn_search_tag.setText("Искатьм заметки по тегу")

with open("notes.json", "r", encoding="utf-8") as file:
    notes = json.load(file)

#notes = {
#    "Добро пожаловать": {
#        "текст": 'В этом приложении можно создавать заметки с тегами',
#        "теги": ['Умные заметки', 'Инструкция']
#    }
#}

app = QApplication([])
main_win = QWidget()

main_line = QHBoxLayout()
v_line = QVBoxLayout()
line_1 = QHBoxLayout()
line_2 = QHBoxLayout()

field_text = QTextEdit()
field_tag = QLineEdit()
list_tags = QListWidget()
list_notes = QListWidget()

list_notes.addItems(notes)
list_notes.itemClicked.connect(show_note)

btn_add_note = QPushButton('Создать заметку')
btn_add_note.clicked.connect(add_note)
btn_del_note = QPushButton('Удалить заметку')
btn_del_note.clicked.connect(del_note)
btn_save_note = QPushButton('Сохранить заметку')
btn_save_note.clicked.connect(save_note)
btn_add_tag = QPushButton('Добавить к заметке')
btn_add_tag.clicked.connect(add_tag)
btn_del_tag = QPushButton('Открепить от заметки')
btn_del_tag.clicked.connect(del_tag)
btn_search_tag = QPushButton('Искать заметки по тексту')
btn_search_tag.clicked.connect(search_tag)

v_line.addWidget(list_notes)
v_line.addWidget(btn_add_note)
v_line.addWidget(btn_del_note)
v_line.addWidget(btn_save_note)
v_line.addWidget(list_tags)
v_line.addWidget(field_tag)
v_line.addWidget(btn_add_tag)
v_line.addWidget(btn_del_tag)
v_line.addWidget(btn_search_tag)
main_line.addWidget(field_text)


main_line.addLayout(v_line)


main_win.setLayout(main_line)
main_win.show()
app.exec_()
with open("notes.json", "w", encoding="utf-8") as file:
    json.dump(notes, file, sort_keys=True, ensure_ascii=False)
