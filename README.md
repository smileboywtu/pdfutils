# why pdfutils

pdfutils is a tool to manipulate the pdf with python. this project is inspired by the gerbil[1], but I'm  not satisfied with the function and code style it has, and I write a more powerful tool.

# feature

+ add water mark to powerful
+ convert image to pdf

# install

``` python
	python setup.py install 
```

# usage

``` shell 

Usage: pdfutils [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -t TEXT, --text=TEXT  The text to appear on footer the page, support string
                        template, support user, date, time.
  -i INPUT, --input=INPUT
                        The input file for the text to be addedso.
  -o OUTPUT, --output=OUTPUT
                        The ouput file to be saved.
  -f FONT, --font=FONT  Path to the TrueType font file to be used (*.ttf)
  -c FONT_COLOR, --font-color=FONT_COLOR
                        Hex color, defaults to Grey: #545454
  -s FONT_SIZE, --font-size=FONT_SIZE
                        The font size px to be used (default = 18)
  -a AUTHOR, --author=AUTHOR
                        The author to appear in metadata.
  -u SUBJECT, --subject=SUBJECT
                        The subject to appear in metadata.
  --top=TOP             The padding from the left hand side of the page (cm)
  --side=SIDE           The padding from the top of the page (cm)
  -x PAGE_WIDTH, --page-width=PAGE_WIDTH
                        The width of the page (cm)
  -y PAGE_HEIGHT, --page-height=PAGE_HEIGHT
                        The height of the page (cm)
  -r ROTATE             The string rotation, default to 0.
  -p ALPHA, --alpha=ALPHA
                        Color alpha value to control the transparent. value
                        between 0.0 and 1.0
  -w, --whole-paper     Draw the string whole paper.
  --paper-size=PAPER    Default = A4. The named size of the paper Supported:
                        A0 - A6, B0 - B6, LETTER, LEGAL.  Paramter ignored if
                        -x and -y are supplied
  --landscape           Default = portrait unless this flag is supplied.
                        Defines the page orientation,  (ignored if -x and -y
                        are given)
  --skip-pages=SKIP_PAGES
                        number of pages to skip before stamping starts.
                        Default = 0


```

# example

create a gray color watermark with current logging user and current date inside the whole paper:

``` shell 

pdfutils -i p1.pdf -o 2.pdf -f /usr/share/fonts/gnu-free/FreeMono.ttf -t "\$user \$date" -w -r 30

```


[1]: https://github.com/bwghughes/gerbil 