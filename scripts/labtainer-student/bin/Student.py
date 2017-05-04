#!/usr/bin/env python
'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
'''

# Student.py
# Description: Create a zip file
#              containing the student lab work

import glob
import json
import os
import sys
import zipfile


print os.path.expanduser("~")

# Usage: Student.py
# Arguments:
#     None
def main():
    #print "Running Student.py"
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: Student.py <username>\n")
        return 1
    StudentHomeDir = os.path.join('/home',sys.argv[1])
    HomeLocal= os.path.join(StudentHomeDir, '.local')
    os.chdir(StudentHomeDir)
    student_email_file=os.path.join(HomeLocal, '.email')
    lab_name_file=os.path.join(HomeLocal, '.labname')
    with open(student_email_file) as fh:
        student_email = fh.read().strip()
    with open(lab_name_file) as fh:
        lab_name = fh.read().strip()
    # NOTE: Always store as e-mail+lab_name.zip
    #       e-mail+lab_name.zip will be renamed by stop.py (add containername)
    ZipFileName = '%s.%s.zip' % (student_email.replace("@","_at_"), lab_name)

    #print 'The lab name is (%s)' % LabName
    #print 'Output ZipFileName is (%s)' % ZipFileName

    OutputName=os.path.join(HomeLocal, ZipFileName)
    TempOutputName=os.path.join("/tmp/", ZipFileName)
    # Remove temp zip file and any zip file in HomeLocal
    if os.path.exists(TempOutputName):
        os.remove(TempOutputName)
    zip_filenames = glob.glob('%s*.zip' % HomeLocal)
    for zip_file in zip_filenames:
        #print "Removing %s" % zip_file
        os.remove(zip_file)

    # Note: Use /tmp to temporary store the zip file first
    # Create temp zip file and zip everything under StudentHomeDir
    zipoutput = zipfile.ZipFile(TempOutputName, "w")
    for rootdir, subdirs, files in os.walk(StudentHomeDir):
        newdir = rootdir.replace("/home/ubuntu", ".")
        for file in files:
            savefname = os.path.join(newdir, file)
            #print "savefname is %s" % savefname
            zipoutput.write(savefname, compress_type=zipfile.ZIP_DEFLATED)
    zipoutput.close()
    os.chmod(TempOutputName, 0666)

    # Rename from temp zip file to its proper location
    os.rename(TempOutputName, OutputName)
    # Store 'OutputName' into 'zip.flist' 
    zip_fname = os.path.join(HomeLocal, 'zip.flist')
    zip_flist = open(zip_fname, "w")
    zip_flist.write('%s ' % OutputName)
    zip_flist.close()
    os.chmod(zip_fname, 0666)
    return 0

if __name__ == '__main__':
    sys.exit(main())

