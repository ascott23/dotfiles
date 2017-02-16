import argparse as ap
import PyPDF2 as pdf

parser = ap.ArgumentParser(description='Give the number of degrees to rotate pages by')

parser.add_argument('-i', '--in', nargs=1, help="The file to be rotated.", dest="in_fs")
parser.add_argument('-o', '--output', nargs='?', help="The name of the file to be outputted.", dest="out_fs", default=None)
parser.add_argument('-p', '--pages', nargs='*', help="The pages to be rotated.", dest="pages", default=[])
parser.add_argument('-a', '--angle', nargs=1, type=int, help="The number of 90 degree rotations to make (clockwise).", dest="angle")

args = parser.parse_args()

in_fname = args.in_fs[0]

if not in_fname.endswith(".pdf"):
    in_fname += ".pdf"

out_fname = (in_fname if args.out_fs == None else args.out_fs[0])

if not out_fname.endswith(".pdf"):
    out_fname += ".pdf"

in_f = pdf.PdfFileReader(in_fname)
out_f = pdf.PdfFileWriter()

for i in range(in_f.getNumPages()):
    page = in_f.getPage(int(i))
    if str(i+1) in args.pages:
        page.rotateClockwise(args.angle[0] * 90)
    out_f.addPage(page)

with open(out_fname, 'wb') as f:
    out_f.write(f)

print("Wrote to {}.".format(out_fname))
