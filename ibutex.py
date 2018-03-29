#!/usr/bin/env python3

import os, argparse, glob, shutil, subprocess

latexbase = ['lualatex']
bibtexbase = []

parser = argparse.ArgumentParser(description='IbuTex - LaTeX-tooling to reduce pain')
parser.add_argument('-c', '--clean', action="store_true", dest='cleanbuild', default=False, help='clean build, remove temporary and cached data before')
parser.add_argument('-q', '--quick', action="store_true", dest='quick', default=False, help='quick build, single run')
parser.add_argument('-i', '--include', type=str, metavar='file/dir', nargs='+', help='files or folder that need to be linked to the builddir')
parser.add_argument('--build-only', action="store_false", dest='showpdf', default=True, help='show the compiled documend afterwards')
parser.add_argument('-b', '--bibcmd', type=str, dest='bibcmd', default="bibtex", help='enter which bibliography backend to use')

args = parser.parse_args()

bibtexbase.append(args.bibcmd)

texfiles = glob.glob('*.tex')

if len(texfiles) > 1:
	print(':: Please select tex-file to compile:')
	for i, v in enumerate(texfiles):
		print('    {}: {}'.format(i, v))
	selection = int(input('  Select:'))
	texfile = texfiles[selection]
else:
	texfile = texfiles[0]

if len(texfiles) < 1:
	print(':: no *.tex-files found for compilation')

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

rv = subprocess.call(fullcmd)
if rv != 0:
	print(":: error compiling")
	exit(1)

if not args.quick:
	subprocess.call(fullbib)
	subprocess.call(fullcmd)
	subprocess.call(fullcmd)

pdffile = texfile[:-4] + '.pdf'
shutil.copy(pdffile, '../' + pdffile)

if args.showpdf:
	subprocess.call(['zathura', pdffile])
