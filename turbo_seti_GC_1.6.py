import os
import time
from pathlib import Path
from turbo_seti.find_doppler.find_doppler import FindDoppler
import glob
from IPython.display import Image, display
import argparse
from tqdm import tqdm
import subprocess
import nbformat as nbf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import sys

# Create the parser
parser = argparse.ArgumentParser(description='Process some integers.')

# Add the arguments
parser.add_argument('date', metavar='date', type=str, help='the date to analyze')
parser.add_argument('s_value', metavar='s_value', type=int, help='the s value')
parser.add_argument('f_value', type=int, help='The f_value for the script')
parser.add_argument('off_value', type=str, help='The off_value for the script')

# Parse the arguments
args = parser.parse_args()

# Define the base directory
BASEDIR = os.path.join("/datax/users/obs/simone", args.date)

if args.off_value == "on":
    OUTPUT_DIR = "/datax/users/obs/simone/OUTPUT"
else:
    OUTPUT_DIR = "/datax/users/obs/simone/OUTPUT_REVERSED"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# Get a list of all subfolders in the date directory
subfolders = [f.name for f in os.scandir(BASEDIR) if f.is_dir()]

# Iterate over the subfolders
for subfolder in subfolders:
    # Construct the DATADIR path
    DATADIR = os.path.join(BASEDIR, subfolder)

    # Construct the output directory path
    subfolder_output_dir = os.path.join(OUTPUT_DIR, args.date, subfolder, f"s_value_{args.s_value}")

    # Construct the f_value subdirectory path
    f_value_subdir = os.path.join(subfolder_output_dir, f"f_value_{args.f_value}")

    # Check if the s_value subfolder already exists
    if not os.path.exists(subfolder_output_dir):
        # Create the output directory if it doesn't exist
        os.makedirs(subfolder_output_dir, exist_ok=True)

        # Check if the f_value subfolder already exists
        if os.path.exists(f_value_subdir):
            print("Already done!")
            sys.exit()

        # Create the f_value subdirectory if it doesn't exist
        os.makedirs(f_value_subdir, exist_ok=True)

        # glob will create a list of specific files in a directory
        fillist = sorted(glob.glob(os.path.join(DATADIR, '*.fil')))

        # Reverse the order of the list
        # fillist.reverse()

        # Iterate over the .fil files
        print("\nAll .fil files in " + subfolder + " are going to be processed.\n")

        for file in tqdm(fillist):
            # Execute turboSETI in the terminal
            console = ['turboSETI', file, '-M', '4', '-s', str(args.s_value), '-o', subfolder_output_dir]
            process = subprocess.Popen(console, stdout=subprocess.PIPE, cwd=subfolder_output_dir)

            # Wait for the process to finish
            process.communicate()

        print("\nAll .fil files in " + subfolder + " have been successfully processed.")   

    if not os.path.exists(f_value_subdir):
        # Construct the f_value subdirectory path
        f_value_subdir = os.path.join(subfolder_output_dir, f"f_value_{args.f_value}")

        # Create the f_value subdirectory if it doesn't exist
        os.makedirs(f_value_subdir, exist_ok=True)

    console = f"plotSETI -f {args.f_value} -c {args.off_value} -o {f_value_subdir} {subfolder_output_dir}"
    subprocess.call(console, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    pnglist = sorted(glob.glob(os.path.join(f_value_subdir, '*.png')))

    # Initialize the counter
    png_counter = len(pnglist)
    print(f"\n {png_counter} PNG files of " + subfolder + " have been generated.")

    # Use the f_value to format the output file name
    output_file_name = f"({png_counter} png) f_value_{args.f_value}.pdf"

    # Create a new PDF in the same directory as the PNG files
    with PdfPages(os.path.join(f_value_subdir, output_file_name)) as pdf:
        for i in range(0, len(pnglist), 25):  # 25 images per page
            fig, axs = plt.subplots(5, 5, figsize=(15, 15))
            for j, ax in enumerate(axs.flat):
                if i + j < len(pnglist):
                    img = plt.imread(pnglist[i + j])
                    ax.imshow(img)
                    ax.axis('off')
                    ax.set_title(os.path.basename(pnglist[i + j]), fontsize=8)
                else:
                    ax.axis('off')  # Hide axes if there's no image

            # Save the current figure to the PDF
            pdf.savefig(fig, dpi=300)
            plt.close(fig)

    print(f"\nPDF file {output_file_name} has been created.")
