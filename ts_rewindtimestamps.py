"""
author : standabany

description
Script allowing to rewind time stamp of a git repository to a previous build.

This is useful for instance if you have one repository of your source and use it as a source for two
or more build with different branches
/k/vue.git as source repository
/l/vue13Pro as build directory for the branch trk99
/l/vue12.5 as build directory for the branch vue12.5

Before each compilation launch ts_rewindtimestamps.py with the build directory in which you will
compile and the "create" action.

Then next time you will compile in the same build, if you have done one or more git checkout in the
meantime, you can use the "update" action that will rewind the timestamps and touch only the file
that differed since last compilation

"""

import sys
try:
    import argparse
except:
    import ts_argparse as argparse
import os, posixpath
import time
import re
from stat import *
import shlex, subprocess

"""
accepts pattern a re pattern, file_obj a file object
return a generators giving the key value pair in /file/ for a certain /pattern/
"""
def findKeyValue(pattern, file_obj):
    grepper = re.compile(pattern)
    for line_num, line in enumerate(file_obj):
        if grepper.search(line):
            yield line.split('=')

"""
accepts sourcedir a path, the work-tree for git
        gitsourcedir a path, the git directory (where to find .git/)
        gitargs a string of args to pass to git
return a subprocess with a PIPE as output
"""
def processGit(sourcedir, gitsourcedir, gitargs):
    gitcmdline = "git --work-tree=" + sourcedir + " --git-dir=" + posixpath.normpath(gitsourcedir) + " " + gitargs
    gitargs = shlex.split(gitcmdline)
    return subprocess.Popen(gitargs, stdout=subprocess.PIPE)

"""
Provides the list of files tracked by git
"""
def GitFilesList(args):
    p = processGit(args.sourcedir, args.gitsourcedir, "ls-files --directory .")
    output = p.communicate()[0].split('\n')
    for f in output[:-1]:   #   Git returns an empty line at the end
        f = posixpath.join(os.path.normpath(args.sourcedirtoplevel), f)
        yield f

def ReadTimeStamps(args):
    return {file.strip(): float(timestamp) for (file, timestamp) in [line.strip().split('@') for line in open(args.timestamp_file)][1:]}

"""
parse function for the "create" action
    write a timestamp file which mtime will be reference for future comparison and the content is the
    hash of the current commit
"""
def pfCreate(args):
    if args.verbose:
        print "Creating timestamp file ... ",
    p = processGit(args.sourcedir, args.gitsourcedir, "rev-parse --verify HEAD")
    output = p.communicate()
    with open(args.timestamp_file, 'w') as tsF:
        tsF.write("%s\n" % output[0][:-1])
        for gitF in GitFilesList(args):
            mtime = os.stat(gitF).st_mtime
            tsF.write("%s @ %s\n" % (gitF, mtime))

    if args.verbose:
        print "Sleeping 2s for timestamps accuracy purpose"
    time.sleep(2)

"""
parse function for the "rewind" action
    read the modification time of the timestamp file previously stored by a "create" action
    then for all the gitified files newer than the timestamps, their modification time is rewinded
    to the timestamp file one
"""
def pfRewind(args):
    if args.verbose:
        print "Looking for timestamp file ... ", args.timestamp_file,
    tsmtime = 0
    if not os.path.exists(args.timestamp_file):
        if args.verbose:
            print "[Failed]\nTimestamp file does not exists\n"
        return 6
    else:
        tsmtime = os.stat(args.timestamp_file).st_mtime
        if args.verbose:
            print tsmtime, "[Ok]\n"

    ts_dict = ReadTimeStamps(args)
    for f in GitFilesList(args):
        tsmtime = ts_dict[f]
        mtime = os.stat(f).st_mtime
        if abs(mtime - tsmtime) > 1:
            os.utime(f, (tsmtime, tsmtime))
            if args.verbose:
                print "rewinding ( was ", mtime, "now ", tsmtime, ") ", f

    """
    for root, dirs, files in os.walk(args.builddir, topdown=False, onerror=None, followlinks=True):
        for name in files:
            f = os.path.normpath(posixpath.join(root, name))
            if os.path.exists(f):
                mtime = os.stat(f).st_mtime
                if tsmtime + 1 > mtime:
                    os.utime(f, (tsmtime, tsmtime))
                    if args.verbose:
                        print "forwarding (", mtime, ") ", f
    """
    return 0

def pfUpdate(args):
    res = pfRewind(args)
    if res != 0:
        return res

    with open(args.timestamp_file) as f:
        hashCommit = f.readline().strip()
    
    p = processGit(args.sourcedir, args.gitsourcedir, "diff --name-only " + hashCommit + " HEAD")
    output = p.communicate()[0].split('\n')
    for f in output[:-1]:   #   Git returns an empty line at the end
        f = os.path.normpath(posixpath.join(args.sourcedirtoplevel, f))
        if os.path.exists(f):
            os.utime(f, None)
            if args.verbose:
                print "updating", f
    return 0
    
def main(argv=None):

    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument('-v', '--verbose', action='store_true', help='talk a lot')
    parser.add_argument('builddir', help='the building directory where to store the timestamp')
    parser.add_argument('-s', '--sourcedir', action='store', default='', help='optional, the source directory from which it was build. If not present, will be found in the CMakeCache.txt file in the build directory')
    subparsers = parser.add_subparsers(help='valid sub-command of ts_rewindtimestamps.py', title='commands', description='List of commands', dest='subname')

    #Parser for the "save" command
    parser_create = subparsers.add_parser('save', help='create a new timestamp in the building directory. To use before a compilation')
    parser_create.set_defaults(func=pfCreate)

    #Parser for the "create" command alias of save
    parser_create = subparsers.add_parser('create', help='alias for save')
    parser_create.set_defaults(func=pfCreate)

    #Parser for the "rewind" command
    parser_rewind = subparsers.add_parser('rewind', help='rewind the timestamp of the source directory to the one of the reference timestamp. Not to use, use update instead')
    parser_rewind.set_defaults(func=pfRewind)

    #Parser for the "update" command
    parser_update = subparsers.add_parser('update', help='do a rewind and then update the timestamp of the files git stated to be modified. To use after a git command altering your source files')
    parser_update.set_defaults(func=pfUpdate)

    args = parser.parse_args(argv[1:])
    
    if args.verbose:
        print "Checking the build directory ... ",
    if not os.path.exists(args.builddir) or not os.path.isdir(args.builddir):
        if args.verbose:
            print("[Failed]\nBuild directory", args.builddir, "either not exists or is not a directory\n")
        return 1
    else:
        if args.verbose:
            print ("[Ok]\n")
    
    if args.sourcedir == '':
        if args.verbose:
            print "No source directory provided, checking it in CMakeCache.txt ... ",
        args.cmc = os.path.join(args.builddir, "CMakeCache.txt")
        if not os.path.exists(args.cmc) or not os.path.isfile(args.cmc):
            if args.verbose:
                print("[Failed]\nCMakeCache.txt not present, is it really a build directory ?\n")
            return 2
        else:
            if args.verbose:
                print ("[Ok]\n")
            
        if args.verbose:
            print "Reading CMakeCache.txt to find source directory ... ",
        args.sourcedir = next(findKeyValue(r"^\s*CMAKE_HOME_DIRECTORY", file(args.cmc)))[1][:-1]
        
        if not os.path.exists(args.sourcedir) or not os.path.isdir(args.sourcedir):
            if args.verbose:
                print "[Failed]\nWe found ", args.sourcedir, "as a source directory, but sadly it does not exists or it is not a directory\n"
            return 3
        else:
            if args.verbose:
                print ("[Ok]\n")
    
    args.gitsourcedir = posixpath.join(args.sourcedir, ".git")
    while (not os.path.exists(args.gitsourcedir) or not os.path.isdir(args.gitsourcedir)) and (posixpath.normpath(args.gitsourcedir) != posixpath.normpath(posixpath.join(os.path.dirname(args.gitsourcedir), '..', '.git'))):
        args.gitsourcedir = posixpath.join(os.path.dirname(args.gitsourcedir), '..', '.git')
    
    if (not os.path.exists(args.gitsourcedir) or not os.path.isdir(args.gitsourcedir)):
        if args.verbose:
            print "The source directory found is not a git repository"
        return 10
    
    args.sourcedirtoplevel = posixpath.join(os.path.dirname(args.gitsourcedir))
    args.timestamp_file=os.path.join(args.builddir, ".git.timestamp")
    
    return args.func(args)
    
if __name__ == "__main__":
    sys.exit(main())
