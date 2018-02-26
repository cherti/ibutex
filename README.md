# ibutex
## A LaTeX-Wrapper to reduce pain

While Latex is a very useful tool, it is commonly known to cause a not unsignificant amount of friction in its usage.
To reduce that amount of friction, ibutex provides a wrapper around LaTeX

This tool automatically builds latex documents based on latex and optionally bibtex. See `ibutex.py --help` for a detailed list of options.

## Setting

`ibutex` expects your main latex file to be in your base folder, all sections to be in a subfolder (default name `sections`) and all graphics and alike in a subfolder (default name `img`) as well.

It then builds your project in a `.texbuild-$name`-subfolder. This allows you to render multiple Latex documents (i.e. document as well as presentation) from the same set of graphics, for example.

