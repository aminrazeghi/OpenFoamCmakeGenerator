#!/usr/bin/env python

import os
import shutil

with open("Make/options", 'r') as f:
    options = f.readlines()

with open("Make/files", 'r') as f:
    files = f.readlines()

scrfiles = []
targetname = ""

wm_project_version = str(os.getenv("WM_PROJECT_VERSION"))
foam_version = wm_project_version[1:]

defines =  ["-Dlinux64", "-m64", "-pthread", "-DWM_DP", "-DPOPENFOAM=" + foam_version, "-DWM_LABEL_SIZE=32", "-fpermissive", "-DNoRepository", "-O3"]

FOAM_SRC = str(os.getenv("FOAM_SRC"))
FOAM_LIBBIN = str(os.getenv("FOAM_LIBBIN"))

includes = [
  "include_directories(" + os.getcwd() +")", 
  "include_directories(" + FOAM_SRC + "/OpenFOAM/include)", 
  "include_directories(" + FOAM_SRC + "/OpenFOAM/lnInclude)", 
  "include_directories(" + FOAM_SRC + "/foam/lnInclude)", 
  "include_directories(" + FOAM_SRC + "/OSspecific/POSIX/lnInclude)"
]

libs=[
   # FOAM_LIBBIN + "/libfoam.so",
   FOAM_LIBBIN + "/libOpenFOAM.so"
]

for l in options:
    opt = l.strip(" \\\n")
    if opt.startswith("-I"):
        arg = opt[2:]
        if arg.startswith("$(LIB_SRC)"):
            arg = arg.strip("$(LIB_SRC)")
            arg = arg.strip("/")
            path_lib = os.path.join(FOAM_SRC , arg)
            arg = "include_directories(" +  path_lib + ")"
            includes.append(arg)
    elif opt.startswith("-l"):
        arg = opt[2:]
        arg = "lib" + arg + ".so"
        arg = os.path.join(FOAM_LIBBIN, arg)
        libs.append(arg)

scrfiles2 = files[0].strip().split('.')[0]
for l in files:
    ls = l.strip(' \n')
    if l.startswith('EXE'):
        lsp = ls.split('/')
        targetname = lsp[-1]
    elif not ls == "":
        scrfiles.append(l)

if (os.path.exists("CMakeLists.txt")):
    shutil.copyfile("CMakeLists.txt", "CMakeLists.txt.bak")


with open("CMakeLists.txt", 'w') as cm:
    cm.write("cmake_minimum_required(VERSION 3.10)\n\n")
    cm.write("project(" + targetname +")\n\n")
    cm.write("add_definitions(\n")
    for d in defines:
        cm.write("\t" + d + "\n")
    cm.write(")\n\n")

    for inc in includes:
        cm.write(inc + "\n")
    cm.write("\n\n")

    cm.write("add_executable(" + targetname + '\n')
    for src in scrfiles:
        cm.write("\t" + src + "\n")
    cm.write(")\n\n")

    cm.write("target_link_libraries(" + targetname + "\n")
    for lib in libs:
        cm.write("\t" + lib + "\n")
    cm.write(")\n\n")

