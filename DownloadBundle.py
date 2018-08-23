#!D:\James\James' Documents\python\Humle Download\venv\Scripts\python

import os
import time
import requests
import auto_save_hb_html
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Menu
from tkinter import ttk

from bs4 import BeautifulSoup


class App:
    def __init__(self, root):
        frame = tkinter.Frame(root)
        frame.pack()

        root.title('Humble Downloader')
        self.items_to_download = []

        self.menu = Menu(root)
        root.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Import Bundle Page', command=self.get_html)
        self.filemenu.add_command(label='Exit', command=frame.quit)

        self.bundle_name_lbl = tkinter.Label(frame, text='IMPORT FILE TO START', anchor='w')
        self.bundle_name_lbl.grid(row=0, column=0, sticky='w', pady=5, padx=10)

        self.dir_lbl = tkinter.Label(frame, text='Directory to save bundle:', anchor='w')
        self.dir_lbl.grid(row=1, columnspan=2, sticky='w', padx=10)

        self.dir_to_save = tkinter.Text(frame, height=1, width=50)
        self.dir_to_save.grid(row=2, column=0, padx=10)

        self.choose_dir = tkinter.Button(frame, text='...', command=self.directory_dialog)
        self.choose_dir.grid(row=2, column=1, padx=10)

        self.blank_label_3 = tkinter.Label(frame)
        self.blank_label_3.grid(row=3)

        self.file_type_lbl = tkinter.Label(frame, text='What file types would you like to download?')
        self.file_type_lbl.grid(row=4, sticky='w', padx=10)

        self.list_box_frame = tkinter.Frame(frame)
        self.list_box_frame.grid(row=5, sticky='w', padx=10, pady=5)

        self.file_type_list = tkinter.Listbox(self.list_box_frame, height=5, selectmode=tkinter.MULTIPLE)
        self.file_type_list.pack()

        self.blank_label_1 = tkinter.Label(frame)
        self.blank_label_1.grid(row=7)

        self.prog_bar_label = tkinter.Label(frame, text='Download Progress:')
        self.prog_bar_label.grid(row=7, columnspan=2, sticky='w', padx=10)

        self.prog_bar = ttk.Progressbar(frame, length=100)
        self.prog_bar.grid(row=8, padx=10, sticky='ew', columnspan=2)

        self.save_btn = tkinter.Button(frame, text='Download Bundle', command=self.save_bundle)
        self.save_btn.grid(row=9, pady=5, padx=10, sticky='ew', columnspan=2)

        self.status = tkinter.Label(frame, text='Status', bd=1, relief=tkinter.SUNKEN, anchor='w')
        self.status.grid(row=10, column=0, sticky='ew', columnspan=2)

    def directory_dialog(self):
        self.dir_to_save.delete(1.0, tkinter.END)
        self.dir_to_save.insert(1.0, filedialog.askdirectory())

    def get_html(self):
        file_name = 'bundle.html'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.join(dir_path, file_name)

        message = 'Press OK and then you have 5 seconds to make the browser with the bundle active.\n\n' \
                  'The web page will then be saved and processed automatically.\n' \
                  'Please keep focus on the window until download has started.'

        if messagebox.askokcancel('Start Download', message):
            html_import = False
            for i in range(6):
                self.status['text'] = 'Starting save in {}'.format(5 - i)
                self.status.update()
                time.sleep(1)
            self.status['text'] = 'Saving HTML...'
            self.status.update()
            auto_save_hb_html.save_active_window(dir_path)
            for _ in range(10):
                self.status['text'] = 'Waiting for save to finish.'
                self.status.update()
                if os.path.isfile(dir_path):
                    self.status['text'] = 'Parsing HTML.'
                    self.status.update()
                    html_import = self.parse_html(dir_path)
                    break
                else:
                    time.sleep(1)

            if html_import:
                self.status['text'] = 'Removing temporary files.'
                self.status.update()
                self.del_dir(os.path.dirname(os.path.realpath(__file__)))
                os.remove(dir_path)
                self.status['text'] = 'Parsing completed.'
                self.status.update()
            else:
                messagebox.showinfo('Download Error',
                                    'The file was not downloaded and parsed correctly, please try again.')
                self.status['text'] = 'File Import Error'
                self.status.update()

    def parse_html(self, file_name):
        if os.path.isfile(file_name):
            with open(file_name) as html_doc:
                soup = BeautifulSoup(html_doc, 'html.parser')
            self.find_download_links(soup)
            self.create_file_list_box()

            return True
        else:
            return False

    def find_download_links(self, soup):
        bundle_title = soup.find('div', {'id': 'hibtext'})
        bundle_title = str(bundle_title.text).strip().split('purchasing ', 1)[1]
        self.bundle_name_lbl['text'] = '{} is ready to download!'.format(bundle_title)

        for link in soup.findAll('a'):
            if 'dl.humble' in str(link.get('href')):
                self.items_to_download.append({'bundle_title': bundle_title,
                                               'file_type': get_file_type(link.get('href')),
                                               'download_link': str(link.get('href')),
                                               'file_name': get_file_name(link.get('href')),
                                               'sub_dir': str(link.text).strip()})

    @staticmethod
    def del_dir(dir_name):
        download_directory = os.path.join(dir_name, 'bundle_files')
        for file in os.listdir(download_directory):
            os.remove(os.path.join(download_directory, file))
        os.removedirs(download_directory)

    def create_file_list_box(self):
        file_types = set()
        for item in self.items_to_download:
            file_types.add(item['sub_dir'])

        self.file_type_list.delete('0', tkinter.END)

        for file in file_types:
            self.file_type_list.insert(tkinter.END, file)

    def create_sub_directories(self, list_of_dir):
        self.status['text'] = 'Creating Sub Directories'
        self.status.update()
        for directory in list_of_dir:
            if not os.path.isdir(os.path.join(str(self.dir_to_save.get('1.0', tkinter.END)).strip(), directory)):
                os.makedirs(os.path.join(str(self.dir_to_save.get('1.0', tkinter.END)).strip(), directory))

    def save_bundle(self):
        byte_size = 2048

        dir_list = []
        for x in self.file_type_list.curselection():
            dir_list.append(self.file_type_list.get(x))

        self.create_sub_directories(dir_list)

        download_these_items = [item for item in self.items_to_download if item['sub_dir'] in dir_list]

        print(len(download_these_items))
        for item in download_these_items:
            print(item)

        for x, item in enumerate(download_these_items, 1):
            item_path = os.path.join(str(self.dir_to_save.get('1.0', tkinter.END)).strip(), item['sub_dir'])
            file_name = os.path.join(item_path, item['file_name'] + '.' + item['file_type'])
            self.status['text'] = 'Saving item {} of {}.   {}.{}'.format(x, len(download_these_items),
                                                                         item['file_name'], item['file_type'])

            if not os.path.isfile(file_name):
                response = requests.get(item['download_link'], stream=True)
                if response.status_code == requests.codes.ok:
                    with open(file_name, 'wb') as fout:
                        total_chunks_to_download = int(int(response.headers.get('content-length')) / byte_size)
                        chunks_downloaded = 0
                        for chunk in response.iter_content(byte_size):
                            self.prog_bar['value'] = int((chunks_downloaded / total_chunks_to_download) * 100)
                            self.prog_bar.update()
                            chunks_downloaded += 1
                            if chunk:
                                fout.write(chunk)
                                fout.flush()
                else:
                    self.status['text'] = 'There was an error connecting to the download link, please reload the ' \
                                          'page and try again. '

        self.status['text'] = 'Download Complete'


def main():
    root = tkinter.Tk()
    app = App(root)
    # root.geometry('600x500')

    root.mainloop()


def get_file_name(name):
    name = str(name).split('humble.com/')[1]
    name = name.split('.')[0]
    name = name.replace('/', '-')
    return name


def get_file_type(name):
    name = str(name).split('?')[0]
    name = name.split('.')[-1]
    return name


if __name__ == '__main__':
    main()
