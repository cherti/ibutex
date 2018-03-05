# ibutex
## A LaTeX-Wrapper to reduce pain

While Latex is a very useful tool, it is commonly known to cause a not unsignificant amount of friction in its usage.
To reduce that amount of friction, ibutex provides a wrapper around LaTeX

This tool automatically builds latex documents based on latex and optionally bibtex. See `ibutex.py --help` for a detailed list of options.

## Setting

`ibutex` expects your main latex file to be in your base folder. Things that are needed for compilation (folders with sections or graphics, bibfile(s)) can be specified via `-i`/`--include` during the first run (or during cleanbuilds).

It then builds your project in a `.texbuild-$name`-subfolder. This allows you to render multiple Latex documents (i.e. document as well as presentation) from the same set of graphics, for example.

## License

This works is released under the [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.txt). You can find a copy of this license at https://www.gnu.org/licenses/gpl-3.0.txt.

