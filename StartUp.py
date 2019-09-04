#Command Line Application to open websites and applications
#Author: Alex Lewin (GitHub: github.com/alexlwn123)
#Version: 1.0 (11/27/18)
#

####################################
#ADD OR UPDATE SUPPORTED SITES AND APPLICATIONS HERE#
##################################################################
                                                                 #
supported_sites = {                                              #
        'Gmail' : 'https://www.google.com/gmail/',               #
        'LinkedIn' : 'https://www.linkedin.com/in/alex--lewin/', #
        'GroupMe' : 'https://web.groupme.com/chats',             #
        'Facebook' : 'https://www.facebook.com/',                #
        'Google Calendar' : 'https://calendar.google.com',       #
        'GitHub' : 'https://github.com/',                        #
        'Kattis' : 'https://open.kattis.com/',                   #
        'Reddit' : 'https://www.reddit.com/',                    #
        'Auburn' : 'http://auburn.edu/',
        'Outlook' : 'C:\Program Files (x86)\Microsoft Office\\root\Office16\OUTLOOK.EXE'#
        }                                                        #
                                                                 #
##################################################################

#Help message:
'''
    usage: StartUp.py [-h] [-n] [-a | -o Site [Site ...]] [-l | -L]

    Call with no args opens the website launch gui

    optional arguments:
      -h, --help          show this help message and exit
      -n, --dry-run       Dry run
      -a, --all           Opens all supported sites
      -o Site [Site ...]  Open named site(s) ("Site": name as appears on list)
      -l, --list          Lists all supported sites
      -L, --list_verbose  Lists all supported sites with urls
'''


from tkinter import *
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
import requests
import os
import argparse
import sys

#Argument Functions
def launch_website(site_name):
  if _Sites[site_name].startswith('http'):
    os.system('explorer %s' % _Sites[site_name])
  else:
    os.startfile(_Sites[site_name])

def launch_all(is_dry):
    global _Sites
    for site in _Sites:
        if not is_dry:
            launch_website(site)
        else:
            print('%s: [%s]' % (site, _Sites[site]))

def list_sites():
    global _Sites
    print('\nList of Supported Sites')
    print('------------')
    print('[Site Title]')
    print('------------')
    for site in _Sites:
        print(site)
    print()

def list_sites_verbose():
    global _Sites
    print('\nList of Supported Sites with URLs')
    print('-----------------')
    print("Site Title: [url]")
    print('-----------------')
    for site in _Sites:
        print('%s: [%s]' % (site, _Sites[site]))
    print('------')


def make_gui(is_dry):
    global _Sites
    root = Tk()
    title = Label(root, text="Website Launcher%s" % (' (dry)' if is_dry else ''), font= 'Times 20 bold')
    title.pack()

    frame = Frame(root)
    frame.pack(side=TOP)

    for name in _Sites:
        callback = Callback(print if is_dry else launch_website, name)
        button = Button(frame, text=name, command = callback).pack(side=LEFT)

    root.mainloop()


def open_sites(site_names, is_dry):
    global _Sites
    has_failed = False
    has_succeed = False
    for site_name in site_names:
        if site_name in _Sites:
            if not is_dry:
                launch_website(site_name)
            else:
                if not has_succeed:
                    print('Dry Launch:')
                    has_succeed = True
                print('%s: [%s]' % (site_name, _Sites[site_name]))
        else:
            print("\"%s\" is not a supported site." % site_name)
            has_failed = True

    if has_failed:
        print("\nUse \"%s -l\" for a list of supported sites." % sys.argv[0])

def get_favorite_sites():
    chrome_url = 'chrome://newtab'
    resp = requests.get(chrome_url)
    soup = BeautifulSoup(resp.text, 'lxml')
    urls = []
    for h in soup.find_all('a'):
        urls.append(h.find('a').attrs['herf'])
    print(str(urls))

#Callback Shim for buttons
class Callback:
    def __init__(self, callback, *firstArgs):
        self.__callback = callback
        self.__firstArgs = firstArgs

    def __call__(self, *args):
        return self.__callback(*(self.__firstArgs + args))


def parse_args(args):
    arg_parser = argparse.ArgumentParser(description = "Call with no args opens the website launch gui")
    arg_parser.add_argument('-n', '--dry-run', dest='dry', help='Dry run', action='store_true')

    open_args = arg_parser.add_mutually_exclusive_group()
    open_args.add_argument('-a', '--all', help='Opens all supported sites', action='store_true')
    open_args.add_argument('-o', dest = 'open', help='Open named site(s) (\"Site\": name as appears on list)', nargs='+', metavar='Site')

    list_args = arg_parser.add_mutually_exclusive_group()
    list_args.add_argument('-l', '--list', help='Lists all supported sites', action='store_true')
    list_args.add_argument('-L', '--list_verbose', help='Lists all supported sites with urls', action='store_true')

    return(arg_parser.parse_args())

def execute_args(args):
    if args.all:
        launch_all(args.dry)
    if args.list:
        list_sites()
    elif args.list_verbose:
        list_sites_verbose()
    if args.open:
        open_sites(args.open, args.dry)

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and args.dry): #No Args
        make_gui(args.dry)


def main():
    global supported_sites
    global _Sites
    _Sites = CaseInsensitiveDict(supported_sites)
    args = parse_args(sys.argv[1:])
    execute_args(args)


if __name__ == '__main__':
    if sys.version_info[0] < 3:
        print(str(sys.version_info[0]))
        print("Python 3 required")
        print("Aborting...")
        sys.exit(0)
    main()

