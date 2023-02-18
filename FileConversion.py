from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os

# code is from https://clay-atlas.com/us/blog/2021/03/08/python-en-svglib-convert-svg-png/#comment-2460


def convert_svg_to_pdf(svg_filepath):
    # converts the svg files at a location to a rlg files
    SVG_to_RLG_file = svg2rlg(svg_filepath)
    SVG_solution_to_RLG_file = svg2rlg(os.path.splitext(svg_filepath)[0] + '-solution.svg')
    # draws the PDF from the RLG file and saves it to a location
    renderPDF.drawToFile(SVG_to_RLG_file, os.path.splitext(svg_filepath)[0] + '.pdf')
    renderPDF.drawToFile(SVG_solution_to_RLG_file, os.path.splitext(svg_filepath)[0] + '-solution.pdf')





