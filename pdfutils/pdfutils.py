import io
import os
import click
from sys import platform
from string import Template
from time import gmtime, strftime
from os.path import basename, isfile, splitext, exists

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm, inch
from reportlab.lib import pagesizes
from reportlab.lib.colors import HexColor


def get_paper_size(size):
    return {
        'A0': pagesizes.A0,
        'A1': pagesizes.A1,
        'A2': pagesizes.A2,
        'A3': pagesizes.A3,
        'A4': pagesizes.A4,
        'A5': pagesizes.A5,
        'A6': pagesizes.A6,
        'LETTER': pagesizes.LETTER,
        'LEGAL': pagesizes.LEGAL,
        'B0': pagesizes.B0,
        'B1': pagesizes.B1,
        'B2': pagesizes.B2,
        'B3': pagesizes.B3,
        'B4': pagesizes.B4,
        'B5': pagesizes.B5,
        'B6': pagesizes.B6,
    }.get(size, pagesizes.A4)


def get_page_size(options):
    if options.page_width and options.page_height:
        width, height = options.page_width * cm, options.page_height * cm
    else:
        width, height = get_paper_size(options.paper_size)
        if options.landscape:
            width, height = height, width
    return width, height


def isfexists(filename):
    return False if not filename else isfile(filename)


def get_sys_state():
    "get the current system time, date, user"
    mtime = gmtime()
    time = strftime("%H:%M:%S", mtime)
    date = strftime("%Y-%m-%d", mtime)
    user = os.environ['LOGNAME'] or os.environ['USER'] or os.environ['LNAME'] or os.environ['USERNAME']
    return {
        "time": time,
        "date": date,
        "user": user
    }


def create_font_args(options):
    if isfexists(options.font):
        font_name, font_path = (basename(splitext(options.font)[0]),
                                options.font)
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    else:
        font_name = 'zenhei'
        if platform.startswith('linux'):
            if exists('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'):
                pdfmetrics.registerFont(
                    TTFont(
                        font_name,
                        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
                    )
                )
            elif exists('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttf'):
                pdfmetrics.registerFont(
                    TTFont(
                        font_name,
                        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttf'
                    )
                )
            elif exists('/usr/share/fonts/wenquanyi/wqy-zenhei/wqy-zenhei.ttc'):
                pdfmetrics.registerFont(
                    TTFont(
                        font_name,
                        '/usr/share/fonts/wenquanyi/wqy-zenhei/wqy-zenhei.ttc'
                    )
                )
        elif platform.startswith('darwin'):
            pdfmetrics.registerFont(
                TTFont(
                    font_name,
                    '/Library/Fonts/Arial Unicode.ttf'
                )
            )
        elif platform.startswith('win'):
            font_name = 'STSong-Light'
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    try: 
        pdfmetrics.getFont(font_name)
    except:
        raise ValueError('Font %s not found.' % font_name)
    options.font_name = font_name


def create_footer(options):
    if not options.text:
        return None, "No text to write, exiting"

    gbklen = (lambda b: len(b.decode('utf8').encode('gbk')))
    watermark = Template(options.text).safe_substitute(get_sys_state())
    watermarks = watermark.strip('\n').split()
    max_line = max(gbklen(i) for i in watermarks)

    pdf = io.BytesIO()
    width, height = get_page_size(options)
    can = canvas.Canvas(pdf, pagesize=(width, height))
    can.rotate(options.rotate)
    color = HexColor(options.font_color)
    can.setFillColorRGB(color.red, color.green, color.blue, options.alpha)
    can.setFont(options.font_name, options.font_size)

    if options.top and options.side:
        can.drawString(
            options.side * cm, (height - options.top) * cm, watermark)
    elif options.whole:
        y = height - inch
        width_ = int(width)
        while y > -10 * inch:
            for element in watermarks:
                line = "{}{}".format(element, "  " * (max_line - gbklen(element) + 2))
                can.drawString(0, y,  line * (width_ // gbklen(line) + 1))
                y -= 1 * inch
            y -= 1 * inch
    else:
        y = height / 2.0 
        width_ = int(width)
        for element in watermarks:
            line = "{}{}".format(element, "  " * (max_line - gbklen(element) + 2))
            can.drawString(0, y, line * (width_ // gbklen(watermark_line) + 1))
            y -= 1 * inch
    can.save()
    return pdf, None


def merge_files(options, footer):
    footer.seek(0)
    new_pdf = PdfFileReader(footer)

    if not isfexists(options.input):
        print("Could not read the input file - did you specify one?")
        exit(1)

    if not options.output:
        print("No output path specified")
        exit(1)

    try:
        book = PdfFileReader(open(options.input, "rb"))
    except (Exception, e):
        print("Unable to load input PDF - {}".format(e))
        exit(1)

    output = PdfFileWriter()

    if options.author:
        output.addMetadata({"/Author": options.author})

    if options.subject:
        output.addMetadata({"/Subject": options.subject})

    with click.progressbar(book.pages) as bar:
        for index, page in enumerate(bar):
            page = book.getPage(index)
            if index >= options.skip_pages:
                page.mergePage(new_pdf.getPage(0))
            output.addPage(page)

    outputStream = open(options.output, "wb")
    output.write(outputStream)
    outputStream.close()
    print("Written {}".format(options.output))
