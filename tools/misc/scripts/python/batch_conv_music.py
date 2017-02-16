import subprocess as subproc
import argparse as ap
import os

parser = ap.ArgumentParser(description='List files to convert')

parser.add_argument('-i', '--in', nargs='+', help="The files to be converted.", dest="in_files")
parser.add_argument('-f', '--format', nargs=1, help="The format to convert to.", dest="format")
parser.add_argument('-k', '--keep', nargs='?', help="Should the original files be kept.", dest="keep", type=bool, default=True)
parser.add_argument('-v', '--verbose', nargs='?', help="Verbose output.", dest="verbose", type=bool, default=True)
parser.add_argument('-O', '--overwrite', nargs='?', help="Overwrite existing files?", dest="overwrite", type=bool, default=True)

args = parser.parse_args()

def vPrint(str):
   """
   Used to print only if verbose
   """
   if args.verbose:
      print(str)

def main():
   devnull = open(os.devnull, 'w')
   for path in args.in_files:
      # Remove the original format and append the new one
      path = os.path.abspath(path)
      new_path = os.path.splitext(path)[0] + '.' + args.format[0]

      # Run the proc and steal its output
      if os.path.splitext(path)[1] == '.m4a':
         cmd = ['ffmpeg', '-i', path, '-acodec', 'libmp3lame', '-ab', '128k', new_path]
      else:
         cmd = ['sox', path, new_path]
      vPrint('Running {}'.format(' '.join(cmd)))
      proc = subproc.Popen(cmd, stdout=subproc.PIPE, stderr=subproc.STDOUT, stdin=subproc.PIPE,
                           encoding='utf-8')

      # Communicate the process should overwrite if needed
      proc.communicate('y' if args.overwrite else 'n')

      # Wait for the proc to finish
      proc.wait()

      # Check the return code
      if proc.returncode:
         print("Received error {} while running {}".format(proc.returncode, ' '.join(cmd)))
      else:
         vPrint("Conversion completed.")

         if not args.keep:
            # Delete the old file
            os.remove(path)

   devnull.close()


if __name__ == '__main__':
   main()
