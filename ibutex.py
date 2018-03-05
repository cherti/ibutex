#!/usr/bin/env python3

import os, argparse, glob, shutil, subprocess

latexbase = ['lualatex']
bibtexbase = ['bibtex']

parser = argparse.ArgumentParser(description='IbuTex - LaTeX-tooling to reduce pain')
parser.add_argument('-c', '--clean', action="store_true", dest='cleanbuild', default=False, help='clean build, remove temporary and cached data before')
parser.add_argument('-f', '--full', action="store_true", dest='full', default=False, help='full build, multiple runs of latex + bibtex')
parser.add_argument('-m', '--material', action="store", dest='materialdir', default='img', help='directory containing material like images')
parser.add_argument('-s', '--sections', action="store", dest='sectiondir', default='sections', help='directory containing sections or chapters if singled out')
parser.add_argument('-b', '--bibfile', action="store", dest='bibfile', default='bibfile.bib', help='bibliography file')
parser.add_argument('--build-only', action="store_false", dest='showpdf', default=True, help='show the compiled documend afterwards')

args = parser.parse_args()

texfiles = glob.glob('*.tex')

if len(texfiles) > 1:
	print(':: Please select tex-file to compile:')
	for i, v in enumerate(texfiles):
		print('    {}: {}'.format(i, v))
	selection = int(input('  Select:'))
	texfile = texfiles[i]
else:
	texfile = texfiles[0]

if len(texfiles) < 1:
	print(':: no *.tex-files found for compilation')

if args.cleanbuild and os.path.exists('.texbuild'):
	shutil.rmtree('.texbuild')

os.makedirs('.texbuild', exist_ok=True)
os.chdir('.texbuild')
if not os.path.islink(args.materialdir):
	os.symlink('../{}'.format(args.materialdir), args.materialdir)
if args.sectiondir and not os.path.islink(args.sectiondir):
	os.symlink('../{}'.format(args.sectiondir), args.sectiondir)
if args.bibfile and not os.path.islink(args.bibfile):
	os.symlink('../{}'.format(args.bibfile), args.bibfile)

fullcmd = latexbase + ['../' + texfile]
fullbib = bibtexbase + [os.path.splitext(texfile)[0]]

rv = subprocess.call(fullcmd)
if rv != 0:
	print(":: error compiling")
	exit(1)

if args.full:
	subprocess.call(fullbib)
	subprocess.call(fullcmd)
	subprocess.call(fullcmd)

pdffile = texfile[:-4] + '.pdf'
shutil.copy(pdffile, '../' + pdffile)

if args.showpdf:
	subprocess.call(['zathura', pdffile])
