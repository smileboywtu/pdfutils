from optparse import OptionParser
from .option_checker import SpecializeOption
from .pdfutils import create_font_args, create_footer, merge_files 

import pkg_resources
try:
    version = pkg_resources.require("pdfutils")[0].version
except:
    version = "1.0.0"


def main():
    parser = OptionParser(option_class=SpecializeOption, version=version)
    parser.add_option('-t', '--text',
                      help="The text to appear on footer the page, support string template, support user, date, time.")
    parser.add_option('-i', '--input',
                      help="The input file for the text to be addedso.")
    parser.add_option('-o', '--output',
                      help="The ouput file to be saved.")
    parser.add_option('-f', '--font',
                      default="Bliss-Regular.ttf",
                      help="Path to the TrueType font file to be used (*.ttf)")
    parser.add_option('-c', '--font-color',
                      type="string",
                      default="#545454",
                      help="Hex color, defaults to Grey: #545454")
    parser.add_option('-s', '--font-size',
                      type="float",
                      default=18,
                      help="The font size px to be used (default = 18)")
    parser.add_option('-a', '--author',
                      help="The author to appear in metadata.")
    parser.add_option('-u', '--subject',
                      help="The subject to appear in metadata.")
    parser.add_option('--top',
                      type="float",
                      help="The padding from the left hand side of the page (cm)")
    parser.add_option('--side',
                      type="float",
                      help="The padding from the top of the page (cm)")
    parser.add_option('-x', '--page-width',
                      type="float",
                      help="The width of the page (cm)")
    parser.add_option('-y', '--page-height',
                      type="float",
                      help="The height of the page (cm)")
    parser.add_option('-r',
                      type='float', dest='rotate', default=0.0,
                      help='The string rotation, default to 0.')
    parser.add_option('-p', '--alpha',
                      type='alpha', default=0.5,
                      help='Color alpha value to control the transparent. value between 0.0 and 1.0')
    parser.add_option('-w', '--whole-paper',
                      action='store_true', dest='whole', default=False,
                      help='Draw the string whole paper.')
    parser.add_option('--paper-size',
                      default="A4",
                      help="Default = A4. The named size of the paper Supported: A0 - A6, B0 - B6, LETTER, LEGAL.  Paramter ignored if -x and -y are supplied ")
    parser.add_option('--landscape',
                      action="store_true", dest="landscape", default=False,
                      help="Default = portrait unless this flag is supplied. Defines the page orientation,  (ignored if -x and -y are given)")
    parser.add_option('--skip-pages',
                      type="int",
                      default=0,
                      help="number of pages to skip before stamping starts. Default = 0")

    (options, args) = parser.parse_args()
    create_font_args(options)
    f, err = create_footer(options)
    if err is None:
        merge_files(options, f)
    else:
        print(err)
