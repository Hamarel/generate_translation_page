# importing modules
import collections
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def generate_array(fname):
    dict_pages = {}
    with open(fname, 'r', encoding="utf8") as f:
        lineno = 0
        row = 0
        page = 1
        chars_on_page = ""
        for line in f:
            for i in line:
                chars_on_page += i
                lineno += 1
                if i == "\n":
                    lineno = 0
                    row += 1
                if (lineno > 12):
                    lineno = 0
                    row += 1
                if (row > 6):

                    row = 0
                    dict_pages[page] = chars_on_page
                    page += 1
                    chars_on_page = ""
                    lineno = 0
        dict_pages[page] = chars_on_page
    orderd_pages = collections.OrderedDict(sorted(dict_pages.items()))
    return orderd_pages

def generate_page(k, v, pdf):
    pdf.translate(cm, cm)

    pdf.setFont("Kaiti", 30)

    # Adjusting the Sizes, mom 13x7 = test91 character spaces
    hanzisize = 43
    half_hanzi = hanzisize / 2
    wordsize = 16
    margin_between = 20
    width_org, height_org = A4

    cell = 3 * wordsize + hanzisize
    width = ((int(width_org)) // hanzisize) * hanzisize
    width_margin = -10

    height = (int(height_org) // (cell + margin_between)) * (cell + margin_between)
    if ((height + cell + margin_between) < int(height_org)):
        height = height + cell

    pdf.setFont("Kaiti", 40)
    for h in range(13, height, cell + margin_between):
        pdf.setLineWidth(2)
        pdf.line(width_margin, h, width + width_margin, h)  # (start x, start y,  end x, end y)
        pdf.setLineWidth(1)
        pdf.line(width_margin, h + wordsize, width + width_margin, h + wordsize)  # (start x, start
        # y,  end x, end y)
        pdf.line(width_margin, h + wordsize + hanzisize, width + width_margin,
                 h + wordsize + hanzisize)  # (start x, start y,  end x, end y)
        pdf.line(width_margin, h + cell, width + width_margin, h + cell)  # (start x, start y,  end x, end y)

        # Grid
        pdf.line(width_margin, h, width_margin, h + wordsize * 3 + hanzisize)  # first
        # horizontal line3

        pdf.setStrokeColorRGB(0.75, 0.75, 0.75, 0.2)
        pdf.line(width_margin, h + wordsize + half_hanzi, width + width_margin,
                 h + wordsize + half_hanzi)  # (start x, start y,  end x, end y)
        for y in range(width_margin, width + width_margin, hanzisize):
            pdf.setStrokeColorRGB(0, 0, 0, 1)
            pdf.line(y, h, y, h + wordsize + hanzisize)  # (start x, start y,  end x, end y)
            if (y < width + width_margin):
                # Grid
                pdf.setStrokeColorRGB(0.75, 0.75, 0.75, 0.2)
                pdf.line(y + 1, h + wordsize + 1, y + hanzisize - 1,
                         h + wordsize + hanzisize - 1)  # (start x, start y,  end x, end y)
                pdf.line(y + 1, h + wordsize + hanzisize - 1, y + hanzisize - 1,
                         h + wordsize + 1)  # (start x, start y,  end x, end y)
                pdf.line(y + half_hanzi, h + wordsize + 1, y + half_hanzi,
                         h + wordsize + hanzisize - 1)  # (start x, start y,  end x, end y)
            pdf.setStrokeColorRGB(0, 0, 0, 1)
        pdf.line(width_margin + width, h, width + width_margin, h + wordsize * 3 + hanzisize)  # Last horizontal line
        pdf.setLineWidth(2)
        pdf.line(width_margin, h + cell - wordsize, width + width_margin,
                 h + cell - wordsize)  # (start x, start y,  end x, end y)

    pdf.setFillColorRGB(0, 0, 0, 0.4)
    column = 0
    row = 0
    start_pos_y = 63
    counter=0

    for char in v:
        if counter == 13:
            column = 0
            row += 1
            counter = 0
        if char == "\n":
            if column == 0:
                continue
            column = 0
            row += 1
            counter = 0
            continue
        pdf.drawString(column *hanzisize -10 , start_pos_y + row* (cell+ margin_between), char)
        column+=1
        counter+=1

    pdf.setFont("Kaiti", 20)
    pdf.setStrokeColorRGB(0, 0, 0,0.2)
    pdf.setFillColorRGB(0, 0, 0,0.2)
    pagenumber = "- " + str(k) + " -"
    pdf.drawString(width_org/2.35, 800, pagenumber)
    pdf.showPage()

fileOK = False
while not fileOK:
    filename = input("Enter txt-file: ")

    if os.path.exists(filename):
        pdfname = input("Enter Name for PDF: ")
        pdf = canvas.Canvas(pdfname + ".pdf", bottomup=0)

        pdf.setTitle(pdfname + " Translation Worksheet")

        pdfmetrics.registerFont(
            TTFont('Kaiti', os.path.join(os.getcwd(), 'STKaiti.ttf'))
        )

        pages = generate_array(filename)
        for k, v in pages.items():
            generate_page(k, v, pdf)

        pdf.save()
        fileOK = True
