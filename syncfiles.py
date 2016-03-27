#!/usr/bin/python
# coding: utf-8
""" Synchronize files

* Copy from newest file to others.
* Error when all files are not exist.
"""
import sys
import os


def main(scriptname, args):
    """ main function

    @param scriptname: script file name
    @param args: command line arguments
    @return: exit status
    """
    if len(args) < 2:
        usage(scriptname)
        return os.EX_USAGE

    return syncfiles(args)


def usage(scriptname):
    """ display usage

    @param scriptname: script file name
    """
    command = os.path.basename(scriptname)
    message = "Usage: {0} <file> <file> [<file> ...]".format(command)
    print3(message, file=sys.stderr)


def syncfiles(filenames):
    """ body

    @param filenames: list of filenames to be synchronized
    @return: exit status
    """
    # newest file as master
    filename_master = get_newest_filename(filenames)
    if filename_master is None:
        print3("Error: No files exist", file=sys.stderr)
        return os.EX_NOINPUT

    print3("Master file: {0}".format(filename_master))
    for filename in filenames:
        if file_same_contents(filename_master, filename):
            continue

        file_copy(filename_master, filename)

    return os.EX_OK


def get_newest_filename(filenames):
    """ get newest(last modified) filename

    @param filenames: list of filenames
    @return: newest file or None
    """
    newest_filename = None
    newest_mtime = -1
    for filename in filenames:
        try:
            # compare mtimes
            mtime = os.path.getmtime(filename)
            if mtime <= newest_mtime:
                continue

            # update filename and mtime
            newest_filename = filename
            newest_mtime = mtime

        except OSError:
            pass

    return newest_filename


def file_same_contents(filename1, filename2):
    """ same contents?

    @param filename1: filename 1
    @param filename2: filename 2
    @return: Yes/No
    """
    import filecmp

    if filename1 == filename2:
        return True

    try:
        return filecmp.cmp(filename1, filename2)

    except OSError:
        return False


def file_copy(filename_src, filename_dst):
    """ copy file and display message

    @param filename_src: source filename
    @param filename_dst: destination filename
    """
    import shutil

    shutil.copy(filename_src, filename_dst)
    print3("Copied: {0} -> {1}".format(filename_src, filename_dst))


def print3(*objects, **params):
    """ print function like Python3

    @param objects: output objects
    @param sep: separate string
    @param end: end string
    @param file: output file
    """
    sep = params.get("sep", " ")
    end = params.get("end", "\n")
    file = params.get("file", sys.stdout)
    file.write(sep.join(str(object) for object in objects))
    file.write(end)


if __name__ == "__main__":
    sys.exit(main(sys.argv[0], sys.argv[1:]))
