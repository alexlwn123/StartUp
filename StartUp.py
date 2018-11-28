#Command Line Application to open websites
#Author: Alex Lewin (GitHub: github.com/alexlwn123)
#Version: 1.0 (11/27/18)
#
#Help message:
'''
    usage: StartUp.py [-h] [-a] [-l | -L] [--open Site [Site ...]]

    Call with no args opens the website launch gui

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Opens all supported sites
      -l, --list            Lists all supported sites
      -L, --list_verbose    Lists all supported sites with urls
      --open Site [Site ...]
                            Open named site(s) ("Site" = Website name as appears
                            on list)
'''


from tkinter import *
import os
import argparse
import sys
from multiprocessing import Process

if sys.version_info[0] < 3:
    print(str(sys.version_info[0]))
    print("Python 3 required")
    print("Aborting...")
    sys.exit(0)

#URLs
_Sites = {
        'Gmail' : 'https://www.google.com/gmail/',
        'LinkedIn' : 'https://www.linkedin.com/in/alex--lewin/',
        'GroupMe' : 'https://web.groupme.com/chats',
        'Facebook' : 'https://www.facebook.com/',
        'Google Calendar' : 'https://calendar.google.com',
        'GitHub' : 'https://github.com/'
        }

#Argument Functions
def launch_website(site_name):
    os.system('explorer %s' % _Sites[site_name])


def launch_all():
    global _Sites
    for site in _Sites:
        launch_website(site)

def list_sites():
    global _Sites
    print('\nList of Supported Sites')
    print('------------')
    print('[Site Title]')
    print('------------')
    for site in _Sites:
        print(site)

def list_sites_verbose():
    global _Sites
    print('\nList of Supported Sites with URLs')
    print('-------------------')
    print("[Site Title]: [url]")
    print('-------------------\n')
    for site in _Sites:
        print('%s: [%s]' % (site, _Sites[site]))

def make_gui():
    root = Tk()
    title = Label(root, text="Website Launcher", font= 'Times 20 bold')
    title.pack()

    frame = Frame(root)
    frame.pack(side=TOP)

    for name in _Sites:
        callback = Callback(launch_website, name)
        button = Button(frame, text=name, command = callback).pack(side=LEFT)

    root.mainloop()

#Callback Shim for buttons
class Callback:
    def __init__(self, callback, *firstArgs):
        self.__callback = callback
        self.__firstArgs = firstArgs

    def __call__(self, *args):
        return self.__callback(*(self.__firstArgs + args))



def main():

    arg_parser = argparse.ArgumentParser(description = "Call with no args opens the website launch gui")
    arg_parser.add_argument('-a', '--all', help='Opens all supported sites', action='store_true')
    list_args = arg_parser.add_mutually_exclusive_group()
    list_args.add_argument('-l', '--list', help='Lists all supported sites', action='store_true')
    list_args.add_argument('-L', '--list_verbose', help='Lists all supported sites with urls', action='store_true')
    arg_parser.add_argument('--open', help='Open named site(s) (\"Site\" = Website name as appears on list)', nargs='+', metavar='Site')
    args = arg_parser.parse_args()

    if args.all:
        launch_all()
    if args.list:
        list_sites()
    elif args.list_verbose:
        list_sites_verbose()
    if args.open:
        has_failed = False
        for site_name in args.open:
            if site_name in _Sites:
                launch_site(site_name)
            else:
                print("\"%s\" is not a supported site." % site_name)
                has_Failed = True
        if has_Failed:
            print("\nUse [-l] argument for a list of supported sites.")

    if len(sys.argv) <= 1: #No Args
        make_gui()


if __name__ == '__main__':
    main()

