#!/usr/bin/env python
# Generate javascript docs in REPOROOT/docs/.build/html/javascript/.
"""
Requires JSDuck: https://github.com/nene/jsduck
"""
from subprocess import call
from os import walk, makedirs
from os.path import exists, join
from shutil import rmtree
from argparse import RawDescriptionHelpFormatter
from sys import exit
import webbrowser

from common import (get_docs_javascriptbuild_dir, DevilryAdmArgumentParser,
                    getprogname, getappsdir)


def find_javascriptfiles():
    jsfiles = []
    for root, dirs, files in walk(getappsdir()):
        is_devilry_doc = 'extjs_classes' in root
        if is_devilry_doc:
            for filename in files:
                if filename.endswith('.js'):
                    filepath = join(root, filename)
                    jsfiles.append(filepath)
    return jsfiles

def build(outdir, openbrowser):
    infiles = find_javascriptfiles()
    if not exists(outdir):
        makedirs(outdir)
    retcode = call(['jsduck', '--verbose', '--output', outdir] + infiles)

    print
    if retcode == 0:
        indexpath = join(outdir, 'index.html')
        print '********************************************************************'
        print "JavaScript docs build successfully. You can view it here:"
        print
        print '   ', indexpath
        print
        print '********************************************************************'
        if openbrowser:
            print 'Opening in browser'
            webbrowser.open_new_tab('file:///' + indexpath)
    else:
        print "JSDuck exited with error code {}.".format(retcode)


def clean(outdir):
    if exists(outdir):
        print "Removing", outdir
        rmtree(outdir)
    else:
        print "Not cleaning", outdir, "because it does not exist."



epilog = 'Example: {prog} --clean --build'.format(prog=getprogname())
description = """{currenthelp}

Requires JSDuck: https://github.com/nene/jsduck

Make sure you install with (notice --pre):

    $ [sudo] gem install --pre jsduck

To get the latest version of jsduck. If you get docs with the same look and
feel as the official ExtJS docs, you have the correct version of JSDuck.
"""
parser = DevilryAdmArgumentParser(description=description,
                                  epilog=epilog,
                                  formatter_class=RawDescriptionHelpFormatter)
parser.add_argument('--nobuild', action='store_true',
                   help='Do not build javascript docs. (Use this with --clean to only clean).')
parser.add_argument('--clean', action='store_true',
                   help='Remove the generated javascript docs.')
parser.add_argument('-b', '--openbrowser', action='store_true',
                    help='Open the docs in your default browser after building.')
parser.add_argument('--completionlist', action='store_true',
                   help='Print completionlist for bash completion.')
args = parser.parse_args()
if args.completionlist:
    print "--nobuild --clean --openbrowser"
    exit(0)


outdir = get_docs_javascriptbuild_dir()

if args.clean:
    clean(outdir)
if not args.nobuild:
    build(outdir, args.openbrowser)
