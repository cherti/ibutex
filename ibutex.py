#!/usr/bin/env python3

import sys, os, argparse, glob, shutil, subprocess, re

parser = argparse.ArgumentParser(description='IbuTex - LaTeX-tooling to reduce pain')
parser.add_argument('-c', '--clean', action="store_true", dest='cleanbuild', default=False, help='clean build, remove temporary and cached data before')
parser.add_argument('-q', '--quick', action="store_true", dest='quick', default=False, help='quick build, single run')
parser.add_argument('-i', '--include', type=str, metavar='file/dir', nargs='+', help='files or folder that need to be linked to the builddir')
parser.add_argument('--build-only', action="store_false", dest='showpdf', default=True, help='show the compiled documend afterwards')
parser.add_argument('-l', '--latexcmd', type=str, dest='latexcmd', default="lualatex", help='enter which latex compiler base command to use')
parser.add_argument('-b', '--bibcmd', type=str, dest='bibcmd', default="bibtex", help='enter which bibliography backend to use')
parser.add_argument('-v', '--viewcmd', type=str, dest='viewcmd', default="zathura", help='enter which bibliography backend to use')
parser.add_argument('-m', '--sage', action="store_true", dest='sagemath', default=False, help='enable running sage command to enable sagetex support')

args = parser.parse_args()

latexbase  = args.latexcmd.split()
bibtexbase = args.bibcmd.split()
viewcmd    = args.viewcmd.split()
sagebase = ["sage"]

texfiles = glob.glob('*.tex')

if len(texfiles) < 1:
	print(':: no *.tex-files found for compilation', file=sys.stderr)
	sys.exit(1)

if len(texfiles) > 1:
	print(':: Please select tex-file to compile:')
	for i, v in enumerate(texfiles):
		print('    {}: {}'.format(i, v))
	try:
		selection = int(input('  Select:'))
	except ValueError:
		print(':: invalid input', file=sys.stderr)
		sys.exit(2)

	try:
		texfile = texfiles[selection]
	except KeyError:
		print(':: non-existing selection', file=sys.stderr)
		sys.exit(2)
else:
	texfile = texfiles[0]


if args.cleanbuild and os.path.exists('.texbuild'):
	shutil.rmtree('.texbuild')

os.makedirs('.texbuild', exist_ok=True)
os.chdir('.texbuild')
if not args.include is None:
	for f in args.include:
		if not os.path.exists(f):
			path = os.path.realpath("../{}".format(f))
			os.symlink(path, f)

fullcmd = latexbase + ['../' + texfile]
fullbib = bibtexbase + [os.path.splitext(texfile)[0]]
fullsage =  sagebase + [texfile.replace("tex", "sagetex") + ".sage"]

rv = subprocess.call(fullcmd)
if rv != 0:
	print(":: error compiling")
	sys.exit(3)

if not args.quick:
	subprocess.call(fullbib)
	if args.sagemath:
		success = subprocess.call(fullsage)
		if success != 0:
			print("error running sagetex, aborting tex build! …")
			sys.exit(4)
	subprocess.call(fullcmd)
	subprocess.call(fullcmd)

pdffile = texfile[:-4] + '.pdf'
shutil.copy(pdffile, '../' + pdffile)

if args.showpdf:
	subprocess.call(viewcmd + [pdffile])
