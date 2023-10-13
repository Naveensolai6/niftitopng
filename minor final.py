import scipy, numpy, shutil, os, nibabel
import sys, getopt
import imageio
import os
FOLDER_PATH = r'E:\\ip'
inputfiles=[]
def listDir(dir):
    fileNames = os.listdir(dir)
    for fileName in fileNames:
        inputfiles.append(os.path.abspath(os.path.join(dir, fileName)))

    return inputfiles
if __name__ == '__main__':
    listDir(FOLDER_PATH)
inputfiles=listDir(FOLDER_PATH)

def main(argv):


    for inputfile in inputfiles:
        process_nifti(inputfile)

def process_nifti(inputfile):
    outputfolder = "E:\op"  # Modify this as needed for your output folder structure

    print('Input file is ', inputfile)
    print('Output folder is ', outputfolder)

    # set fn as your 4d nifti file
    image_array = nibabel.load(inputfile).get_fdata()
    print(len(image_array.shape))

    # ask if rotate
    ask_rotate = input('Would you like to rotate the orientation? (y/n) ')

    if ask_rotate.lower() == 'y':
        ask_rotate_num = int(input('OK. By 90° 180° or 270°? '))
        if ask_rotate_num == 90 or ask_rotate_num == 180 or ask_rotate_num == 270:
            print('Got it. Your images will be rotated by {} degrees.'.format(ask_rotate_num))
        else:
            print('You must enter a value that is either 90, 180, or 270. Quitting...')
            sys.exit()
    elif ask_rotate.lower() == 'n':
        print('OK, Your images will be converted it as it is.')
    else:
        print('You must choose either y or n. Quitting...')
        sys.exit()

    # If 4D image inputted
    if len(image_array.shape) == 4:
        # set 4d array dimension values
        nx, ny, nz, nw = image_array.shape

        # Create a unique output folder for this input file
        inputfile_basename = os.path.basename(inputfile)
        outputfile = os.path.join(outputfolder, os.path.splitext(inputfile_basename)[0])

        if not os.path.exists(outputfile):
            os.makedirs(outputfile)
            print("Created output directory: " + outputfile)

        print('Reading NIfTI file...')

        total_volumes = image_array.shape[3]
        total_slices = image_array.shape[2]

        # iterate through volumes
        for current_volume in range(0, total_volumes):
            slice_counter = 0
            # iterate through slices
            for current_slice in range(0, total_slices):
                if (slice_counter % 1) == 0:
                    # rotate or no rotate
                    if ask_rotate.lower() == 'y':
                        if ask_rotate_num == 90 or ask_rotate_num == 180 or ask_rotate_num == 270:
                            print('Rotating image...')
                            if ask_rotate_num == 90:
                                data = numpy.rot90(image_array[:, :, current_slice, current_volume])
                            elif ask_rotate_num == 180:
                                data = numpy.rot90(numpy.rot90(image_array[:, :, current_slice, current_volume]))
                            elif ask_rotate_num == 270:
                                data = numpy.rot90(numpy.rot90(numpy.rot90(image_array[:, :, current_slice, current_volume])))
                    elif ask_rotate.lower() == 'n':
                        data = image_array[:, :, current_slice, current_volume]

                    # alternate slices and save as png
                    print('Saving image...')
                    image_name = os.path.join(outputfile, inputfile_basename[:-7] + "_t" + "{:0>3}".format(str(current_volume+1)) + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png")
                    imageio.imwrite(image_name, data)
                    print('Saved.')

                    slice_counter += 1

        print('Finished converting images')

    # else if 3D image inputted
    elif len(image_array.shape) == 3:
        # set 3d array dimension values
        nx, ny, nz = image_array.shape

        # Create a unique output folder for this input file
        inputfile_basename = os.path.basename(inputfile)
        outputfile = os.path.join(outputfolder, os.path.splitext(inputfile_basename)[0])

        if not os.path.exists(outputfile):
            os.makedirs(outputfile)
            print("Created output directory: " + outputfile)

        print('Reading NIfTI file...')

        total_slices = image_array.shape[2]

        slice_counter = 0
        # iterate through slices
        for current_slice in range(0, total_slices):
            # alternate slices
            if (slice_counter % 1) == 0:
                # rotate or no rotate
                if ask_rotate.lower() == 'y':
                    if ask_rotate_num == 90 or ask_rotate_num == 180 or ask_rotate_num == 270:
                        if ask_rotate_num == 90:
                            data = numpy.rot90(image_array[:, :, current_slice])
                        elif ask_rotate_num == 180:
                            data = numpy.rot90(numpy.rot90(image_array[:, :, current_slice]))
                        elif ask_rotate_num == 270:
                            data = numpy.rot90(numpy.rot90(numpy.rot90(image_array[:, :, current_slice])))
                elif ask_rotate.lower() == 'n':
                    data = image_array[:, :, current_slice]

                # alternate slices and save as png
                if (slice_counter % 1) == 0:
                    print('Saving image...')
                    image_name = os.path.join(outputfile, inputfile_basename[:-7] + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png")
                    imageio.imwrite(image_name, data)
                    print('Saved.')

                slice_counter += 1

        print('Finished converting images')
    else:
        print('Not a 3D or 4D Image. Please try again.')

# Call the function to start the program
if __name__ == "__main__":
   main(sys.argv[1:])
   

