import argparse as ap
import PyPDF2 as pdf

parser = ap.ArgumentParser(description='List files to concat')

parser.add_argument('-o', '--output', nargs=1, help="The name of the concatenated file to be outputted.", dest="out_fs")
parser.add_argument('-i', '--in', nargs='+', help="The files to be concatenated.", dest="in_fs")
parser.add_argument('-b', nargs='?', type=bool, help="Write the file name as a bookmark", dest="bookmark", default=True)

args = parser.parse_args()

out_fname = args.out_fs[0]

if not out_fname.endswith(".pdf"):
    out_fname += ".pdf"

out_f = pdf.PdfFileMerger()
for fname in args.in_fs:
    if not fname.endswith(".pdf"):
        fname += ".pdf"

    in_f = pdf.PdfFileReader(fname)

    if args.bookmark:
        out_f.append(in_f, bookmark=fname[:-4])
    else:
        out_f.append(in_f)

    print("Appended {} to {}.".format(fname, out_fname))

print("Done merging files, about to write to {}.".format(out_fname))

out_f.write(out_fname)

print("Wrote to {}.".format(out_fname))
