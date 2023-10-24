import tkinter as tk
from tkinter import filedialog, messagebox
import os

rec_path = ''
keep_path = ''

path_to_save = ''
extracted_file_path = ''

# Идея приложения, заключается в том, что каждый jpeg-изображение обладает
# начальным и конечным флагами (FFD8 - начало, FFD9 - конец) в своем байт-код

# Суть в том, что если считать дозаписать после флага FFD9 какой - либо байт-код, то он будет храниться
# внутри изображения, но не коем образом не будет припятствовать использованию изображения

# Во многих случает если объем памяти записываемого файла не велик по отношению к памяти изображения-контейнера,
# то выявить его будет затруднительно

# Данное приложение расчитанно на то, чтобы записывать и считывает байт-код после FFD9,
# реализуя тем самым интересный метод сокрытия и защиты информации

# https://e-scio.ru/wp-content/uploads/2022/07/Вешкин-И.-И.pdf
# https://e-scio.ru/wp-content/uploads/2022/07/%D0%92%D0%B5%D1%88%D0%BA%D0%B8%D0%BD-%D0%98.-%D0%98.pdf

# Функция, реализующая алгоритм записи файла любого расширения в байт-код jpeg-изображения


def write_into_jpg(main_window, sub_window):

    # Импортируем глобальные переменные, хранящие пути до записываемого файла и файла-контейнера (изображение),
    # в который будет записан первый файл

    global rec_path, keep_path

    # Открываем файл-контейнер два раза (в режиме дозаписи и режиме чтения байт-кода),
    # Записываемый файл открывается в режиме считывания байт-кода

    with open(keep_path, 'ab') as keep_file, open(rec_path, 'rb') as rec_file, open(keep_path, 'rb') as keep_file_read:

        # Считывем файл, который будет записан

        content = rec_file.read()

        # Считывем объем памяти файла-контейнера

        f_size = os.path.getsize(keep_path)

        # Считывем объем памяти файла-контейнера до флага FFD9, обозначающий конец изображения

        keep_f = keep_file_read.read()
        keep_f_size = keep_f.index(bytes.fromhex('FFD9')) + 2

        # Если объем занимаймой памяти изображением сопоставим концу байт кода изображени,
        # значит после FFD9 ничего дописано не было

        if f_size <= keep_f_size:

            # Дописывем файл в изображение после FFD9
            keep_file.write(content)

            # Возвращаемся в основное окно

            exit_toplevel(main_window, sub_window)

            # Выводим сообщение об успехе

            messagebox.showinfo(title='Внимание', message='Файл успешно записан!')
            return
        else:

            # Иначе, выводим сообщение об невозможности записи

            messagebox.showwarning(title='Внимание', message='В данный файл уже был записан другой файл')


# Функция, вызывающая меню выбора изображения-контейнера, в которое будет записан файл
# Срабатывает по нажатию на кнопку


def look_for_keeping_file(path_lb):

    global keep_path

    # Открытие меню проводника поиска файла

    keep_path = filedialog.askopenfilename(defaultextension='.jpg',
                                                     filetypes=[('JPEG pictures', '*.jpg')])

    # Если файл был выбран, то отражаем этот путь в интерфейсе

    if keep_path != "":
        keep_path_sepr = keep_path.split('/')
        path_lb['text'] = keep_path_sepr[0] + '/.../' + keep_path_sepr[-1]

    # Иначе путь отсутствует

    else:
        path_lb['text'] = "Отсутствует "

# Функция, вызывающая меню выбора файла, которое будет записано в изображение-контейнер
# Срабатывает по нажатию на кнопку


def look_for_record_file(path_lb):

    global rec_path

    rec_path = filedialog.askopenfilename()

    if rec_path != "":

        rec_path_sepr = rec_path.split('/')
        path_lb['text'] = rec_path_sepr[0] + '/.../' + rec_path_sepr[-1]

    else:

        path_lb['text'] = "Отсутствует "


# Функция, осуществляющая переход в главное окно приложения


def exit_toplevel(main_window, cur_toplevel):

    main_window.update()
    main_window.deiconify()
    cur_toplevel.destroy()


# Функция, вызывающая меню выбора пути, по которому будет создан новый файл, считанный из файла-контейнера


def look_for_saving_path(path_to_save_lb):

    global path_to_save

    path_to_save = filedialog.askdirectory()

    if path_to_save != "":

        path_to_save_sepr = path_to_save.split('/')
        path_to_save_lb['text'] = path_to_save_sepr[0] + '/.../' + path_to_save_sepr[-1]

    else:

        path_to_save_lb['text'] = "Отсутствует "


# Функция, вызывающая меню выбора файла-контейнера, из байт-кода которого будет выгружен другой файл


def look_for_extraction_file(extracted_file_lb):

    global extracted_file_path

    extracted_file_path = filedialog.askopenfilename(defaultextension='.jpg',
                                                     filetypes=[('JPEG pictures', '*.jpg')])

    if extracted_file_path != "":

        extracted_file_path_sepr = extracted_file_path.split('/')
        extracted_file_lb['text'] = extracted_file_path_sepr[0] + '/.../' + extracted_file_path_sepr[-1]

    else:

        extracted_file_lb['text'] = "Отсутствует "


# Функция, реализующая алгоритм выгрузки файла любого расширения из байт-кода jpeg-изображения


def extract_file(main_window, sub_window, filename):

    global path_to_save, extracted_file_path

    with open(extracted_file_path, 'rb') as f, open(extracted_file_path, 'rb') as f_for_read:

        # Считывем файл-контейнер

        extracted_file_content = f.read()

        # Получаем индекс конца файла

        offset = extracted_file_content.index(bytes.fromhex('FFD9')) + 2

        # Переходим в конец байт-кода изображения

        f.seek(offset)

        # Получаем объем всего изображения

        f_size = os.path.getsize(extracted_file_path)

        # Получаем объем изображения до FFD9

        extr_f = f_for_read.read()
        extr_f_size = extr_f.index(bytes.fromhex('FFD9')) + 2

        # Если общий объем больше объема до конца изображения, значит в изображение есть стороний байт-код

        if f_size > extr_f_size:

            # Открываем новый файл на запись байт-кода

            with open(path_to_save + '/' + filename, 'wb') as extracted_f:

                # Записываем считанный байт-код файла

                extracted_f.write(f.read())

                # Выводим сообщение об успехе

                messagebox.showinfo(title='Внимание', message='Файл успешно выгружен из jpg-файла!')

                # Переходим в главное окно

                exit_toplevel(main_window, sub_window)

        # Иначе, выводим сообщение о том, что вшитых файлов не обнаружено
        else:
            messagebox.showwarning(title='Внимание', message='В данный jpg-файл не вшит не один файл!')


# Функция, создающая интерфейс и его логику для модуля выгрузки файла из jpeg-контейнер


def get_file(gui_main):
    gui_main.withdraw()

    # Main Frame

    get_file_window = tk.Toplevel()
    get_file_window.title('Окна сокрытия данных в jpg - файл')

    w_width, w_height = 480, 330

    s_width, s_height = get_file_window.winfo_screenwidth(), get_file_window.winfo_screenheight()

    get_file_window.geometry(
        f"{w_width}x{w_height}+{int((s_width - w_width) / 2)}+{int((s_height - w_height) / 2)}")

    get_file_window.resizable(False, False)

    get_file_frame = tk.LabelFrame(get_file_window, text='Меню выгрузки данных', padx=10, pady=10, labelanchor='n')
    get_file_frame.pack(padx=10, pady=10)

    select_file_to_extract_lb = tk.Label(get_file_frame, text='Выберите файл-контейнер (jpg): ')
    select_file_to_extract_lb.grid(row=1, column=0)

    select_path_to_extract_lb = tk.Label(get_file_frame, text='Выберите путь сохранения: ')
    select_path_to_extract_lb.grid(row=2, column=0, pady=10)

    select_path_to_extract_lb = tk.Label(get_file_frame, text='Введите имя файла: ')
    select_path_to_extract_lb.grid(row=3, column=0)

    extracted_file_name_entry = tk.Entry(get_file_frame, width=30)
    extracted_file_name_entry.insert(0, 'Имя_файла.py')
    extracted_file_name_entry.grid(row=3, column=1, pady=10)

    # Info Frame

    files_info_frame = tk.LabelFrame(get_file_window, text='Информационное меню', padx=10, pady=10, labelanchor='n')
    files_info_frame.pack(padx=10, pady=10)

    extracted_file_lb = tk.Label(files_info_frame, text='Файл-контейнер (jpg): ')
    extracted_file_lb.grid(row=1, column=0)

    extracted_file_path_lb = tk.Label(files_info_frame, text='Отсутствует ')
    extracted_file_path_lb.grid(row=1, column=1)

    path_for_new_file_lb = tk.Label(files_info_frame, text='Путь сохранения: ')
    path_for_new_file_lb.grid(row=2, column=0, pady=10)

    path_for_new_file_data_lb = tk.Label(files_info_frame, text='Отсутствует ')
    path_for_new_file_data_lb.grid(row=2, column=1, pady=10)

    select_file_to_extract_btn = tk.Button(get_file_frame, text='Выбрать файл-выгрузки',
                                           command=lambda: look_for_extraction_file(extracted_file_path_lb))

    select_file_to_extract_btn.grid(row=1, column=1, padx=5)

    select_path_to_save_btn = tk.Button(get_file_frame, text='Выбрать путь',
                                        command=lambda: look_for_saving_path(path_for_new_file_data_lb))

    select_path_to_save_btn.grid(row=2, column=1, pady=10)

    extract_file_from_jpg_btn = tk.Button(get_file_window, text='Выгрузить файл ',
                                          command=lambda: extract_file(gui_main, get_file_window, extracted_file_name_entry.get()))

    extract_file_from_jpg_btn.pack(side=tk.RIGHT, padx=5)

    get_file_window.protocol("WM_DELETE_WINDOW", lambda: exit_toplevel(gui_main, get_file_window))


# Функция, создающая интерфейс и его логику для модуля записи файла в jpeg-контейнер


def hide_file(gui_main):
    gui_main.withdraw()

    # Main Frame

    hide_file_window = tk.Toplevel()
    hide_file_window.title('Окна сокрытия данных в jpg - файл')

    w_width_main, w_height_main = 480, 300

    s_width_main, s_height_main = hide_file_window.winfo_screenwidth(), hide_file_window.winfo_screenheight()

    hide_file_window.geometry(
        f"{w_width_main}x{w_height_main}+{int((s_width_main - w_width_main) / 2)}+{int((s_height_main - w_height_main) / 2)}")

    hide_file_window.resizable(False, False)

    hide_file_frame = tk.LabelFrame(hide_file_window, text='Меню записи данных', padx=10, pady=10, labelanchor='n')
    hide_file_frame.pack(padx=10, pady=10)

    select_file_for_record_lb = tk.Label(hide_file_frame, text='Выберите файл, который будет записан: ')
    select_file_for_record_lb.grid(row=1, column=0)

    select_file_for_keeping_lb = tk.Label(hide_file_frame, text='Выберите файл-контейнер (jpg): ')
    select_file_for_keeping_lb.grid(row=2, column=0, pady=10)

    # Info Frame

    files_info_frame = tk.LabelFrame(hide_file_window, text='Информационное меню', padx=10, pady=10, labelanchor='n')
    files_info_frame.pack(padx=10, pady=10)

    selected_file_for_record_lb = tk.Label(files_info_frame, text='Файл, который будет записан: ')
    selected_file_for_record_lb.grid(row=1, column=0)

    file_for_record_path_lb = tk.Label(files_info_frame, text='Отсутствует ')
    file_for_record_path_lb.grid(row=1, column=1)

    selected_file_for_keeping_lb = tk.Label(files_info_frame, text='Файл-контейнер (jpg): ')
    selected_file_for_keeping_lb.grid(row=2, column=0, pady=10)

    file_for_keeping_path_lb = tk.Label(files_info_frame, text='Отсутствует ')
    file_for_keeping_path_lb.grid(row=2, column=1, pady=10)

    # Buttons to select files

    select_file_for_record_btn = tk.Button(hide_file_frame, text='Выбрать записываемый файл',
                                           command=lambda: look_for_record_file(file_for_record_path_lb))
    select_file_for_keeping_btn = tk.Button(hide_file_frame, text='Выберать файл-контейнер ',
                                            command=lambda: look_for_keeping_file(file_for_keeping_path_lb))

    select_file_for_record_btn.grid(row=1, column=1)
    select_file_for_keeping_btn.grid(row=2, column=1, pady=10)

    record_file_into_jpg_btn = tk.Button(hide_file_window, text='Записать файл ',
                                         command=lambda: write_into_jpg(gui_main, hide_file_window))

    record_file_into_jpg_btn.pack(side=tk.RIGHT, padx=5)

    hide_file_window.protocol("WM_DELETE_WINDOW", lambda: exit_toplevel(gui_main, hide_file_window))


# Главная функция - main


def main():

    gui = tk.Tk()
    gui.title('Приложение для скрытия данных в формате jpeg')

    gui_frame = tk.LabelFrame(gui, text='Возможные действия', padx=100, pady=10, labelanchor='n')
    gui_frame.pack(padx=10, pady=10)
    hide_file_btn = tk.Button(gui_frame, text='Спрятать файл в jpeg', command=lambda: hide_file(gui))
    extract_file_btn = tk.Button(gui_frame, text='Вытащить файл из jpeg', command=lambda: get_file(gui))

    hide_file_btn.pack()
    extract_file_btn.pack(pady=10)

    Author_label = tk.Label(gui, text='by IgorVeshkin, 2021')
    Author_label.pack(side=tk.BOTTOM, padx=5, pady=5)

    w_width, w_height = 480, 240

    s_width, s_height = gui.winfo_screenwidth(), gui.winfo_screenheight()

    gui.geometry(
        f"{w_width}x{w_height}+{int((s_width - w_width) / 2)}+{int((s_height - w_height) / 2)}")

    gui.resizable(False, False)
    gui.mainloop()


# Запуск функции main


if __name__ == "__main__":
    main()
