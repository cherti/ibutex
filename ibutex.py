#!/usr/bin/env python3

import os, argparse, glob, shutil, subprocess

latexbase = ['lualatex', '-shell-escape']
bibtexbase = ['bibtex']

parser = argparse.ArgumentParser(description='IbuTex - LaTeX-tooling to reduce pain')
parser.add_argument('-c', '--clean', action="store_true", dest='cleanbuild', default=False, help='clean build, remove temporary and cached data before')
parser.add_argument('-q', '--quick', action="store_true", dest='quick', default=False, help='quick build, single run')
parser.add_argument('-m', '--material', action="store", dest='materialdir', default='img', help='directory containing material like images')
parser.add_argument('-s', '--sections', action="store", dest='sectiondir', default='sections', help='directory containing sections or chapters if singled out')
#parser.add_argument('-a', action="store_true", default=False)

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

if args.cleanbuild:
	os.remove('.texbuild')

os.makedirs('.texbuild', exist_ok=True)
os.chdir('.texbuild')
if not os.path.islink(args.materialdir):
	os.symlink('../{}'.format(args.materialdir), args.materialdir)
if args.sectiondir and not os.path.islink(args.sectiondir):
	os.symlink('../{}'.format(args.sectiondir), args.sectiondir)

fullcmd = latexbase + ['../' + texfile]
fullbib = bibtexbase + ['../' + texfile]

subprocess.call(fullcmd)

if not args.quick:
	subprocess.call(fullbib)
	subprocess.call(fullcmd)
	subprocess.call(fullcmd)

name = texfile[:-4] + '.pdf'
shutil.copy(name, '../' + name)
