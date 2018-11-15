#!/usr/bin/env python


#  This file is part of the clazy static checker.

#  Copyright (C) 2018 Klaralvdalens Datakonsult AB, a KDAB Group company, info@kdab.com

#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Library General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.

#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Library General Public License for more details.

#  You should have received a copy of the GNU Library General Public License
#  along with this library; see the file COPYING.LIB.  If not, write to
#  the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.


# This is my quick and dirty script to generate clazy app images on each release
# Requires iamsergio/clazy-centos68 docker image to work

import sys, os, getpass

CLAZY_SHA1 = ''
WORK_FOLDER = '/tmp/clazy_work/'
DOCKER_IMAGE = 'iamsergio/clazy-centos68'


def print_usage():
    print sys.argv[0] + ' <clazy sha1>'

def run_command(cmd, abort_on_error = True):
    print cmd
    success = (os.system(cmd) == 0)
    if abort_on_error and not success:
        sys.exit(1)

    return success

def prepare_folder():
    run_command('rm -rf ' + WORK_FOLDER)
    os.mkdir(WORK_FOLDER)

def make_appimage_in_docker():
    cmd = 'docker run -i -t -v %s:%s %s %s' % (WORK_FOLDER, WORK_FOLDER, DOCKER_IMAGE, 'bash -c "/clazy/dev-scripts/docker/make_appimage.sh %s %s"' % (CLAZY_SHA1, str(os.getuid())))
    if not run_command(cmd):
        print 'Error running docker. Make sure docker is running and that you have ' + DOCKER_IMAGE

    os.environ['ARCH'] = 'x86_64'
    dest = WORK_FOLDER + '/Clazy-x86_64.AppImage'
    if not run_command('appimagetool-x86_64.AppImage %s/clazy.AppDir/ %s' % (WORK_FOLDER, dest)):
        return False

    print ''
    print 'Created ' + dest

    return True

if len(sys.argv) != 2:
    print_usage();
    sys.exit(1)


CLAZY_SHA1 = sys.argv[1]

prepare_folder()

if not make_appimage_in_docker():
    sys.exit(1)