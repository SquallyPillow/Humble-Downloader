#!D:\James\James' Documents\python\Humle Download\venv\Scripts\python

import os
import time
import requests
import argparse
import auto_save_hb_html

from bs4 import BeautifulSoup
from clint.textui import progress


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--auto-download',
                        const='True',
                        default='False',
                        help='Will automatically save the HTML from your browser',
                        required=False,
                        nargs='?')

    parser.add_argument('-dir',
                        '--directory-name',
                        help='Directory to save files',
                        required=True)

    args = parser.parse_args()

    bundle_html = 'bundle.html'

    if args.auto_download:
        auto_save_hb_html.save_active_window(bundle_html)
    else:
        bundle_html = input('Enter bundle html file: ')

    for _ in range(30):
        if os.path.isfile(bundle_html):
            break
        else:
            time.sleep(1)

    if os.path.isfile(bundle_html):
        with open(bundle_html) as html_doc:
            soup = BeautifulSoup(html_doc, 'html.parser')
    else:
        print('File was not created in the time expected.')
        exit()

    if args.auto_download:
        del_dir('bundle_files')
        os.remove(bundle_html)

    items_to_download = find_download_links(soup)

    create_sub_directories(items_to_download, args.directory_name)

    download_bundle(args.directory_name, items_to_download)


def find_download_links(soup):
    items_to_download = []

    bundle_title = soup.find('div', {'id': 'hibtext'})
    bundle_title = str(bundle_title.text).strip().split('purchasing ', 1)[1]

    for link in soup.findAll('a'):
        if 'dl.humble' in str(link.get('href')):
            items_to_download.append({'bundle_title': bundle_title,
                                      'file_type': get_file_type(link.get('href')),
                                      'download_link': str(link.get('href')),
                                      'file_name': get_file_name(link.get('href')),
                                      'sub_dir': str(link.text).strip()})

    return items_to_download


def get_file_name(name):
    name = str(name).split('humble.com/')[1]
    name = name.split('.')[0]
    return name


def get_file_type(name):
    name = str(name).split('?')[0]
    name = name.split('.')[-1]
    return name


def create_sub_directories(items_to_download, dir_name):
    for item in items_to_download:
        if not os.path.isdir(os.path.join(dir_name, item['sub_dir'])):
            os.makedirs(os.path.join(dir_name, item['sub_dir']))


def download_bundle(path_to_save, items_to_download):
    for item in items_to_download:

        response = requests.get(item['download_link'], stream=True)
        item_path = os.path.join(path_to_save, item['sub_dir'])
        file_name = os.path.join(item_path, item['file_name'] + '.' + item['file_type'])
        print('Saving {}.{}'.format(item['file_name'], item['file_type']))

        if not os.path.isfile(file_name):
            with open(file_name, 'wb') as fout:
                total_length = int(response.headers.get('content-length'))
                for chunk in progress.bar(response.iter_content(1024), expected_size=(total_length / 1024) + 1):
                    if chunk:
                        fout.write(chunk)
                        fout.flush()


def del_dir(dir_name):
    for file in os.listdir(dir_name):
        os.remove(os.path.join(dir_name, file))

    os.removedirs(dir_name)


if __name__ == '__main__':
    main()
