import click
import PIL.Image
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import filedialog
class Steganography(object):

    def __int_to_bin(rgb):
        #Change RGB (Values) to binary
        r, g, b = rgb
        return ('{0:08b}'.format(r),
                '{0:08b}'.format(g),
                '{0:08b}'.format(b))

    def __bin_to_int(rgb):
        #change binary values to RGB (values)
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

    def __merge_rgb(rgb1, rgb2):
        #merges two rgb Values (in Binary)
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb

    def merge(img1, img2):
        #Merges image2 inside PIL.Image 1

        # Check the images dimensions are suitable for merge
        if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
            raise ValueError('PIL.Image 2 should not be larger than PIL.Image 1!')

        # Get the pixel map of the two images
        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        # Create a new PIL.Image that will be outputted
        new_image = PIL.Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()

        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = Steganography.__int_to_bin(pixel_map1[i, j])

                # Use a black pixel as default
                rgb2 = Steganography.__int_to_bin((0, 0, 0))

                # Check if the pixel map position is valid for the second PIL.Image
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = Steganography.__int_to_bin(pixel_map2[i, j])

                # Merge the two pixels and convert it to a integer tuple
                rgb = Steganography.__merge_rgb(rgb1, rgb2)

                pixels_new[i, j] = Steganography.__bin_to_int(rgb)

        return new_image

    @staticmethod
    def unmerge(img):
        #Unmerges a PIL.Image

        # Load the pixel map
        pixel_map = img.load()

        # Create the new PIL.Image and load the pixel map
        new_image = PIL.Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        # Tuple used to store the PIL.Image original size
        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = Steganography.__int_to_bin(pixel_map[i, j])

                # Extract the last 4 bits (corresponding to the hidden PIL.Image)
                # Concatenate 4 zero bits because we are working with 8 bit
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')

                # Convert it to an integer tuple
                pixels_new[i, j] = Steganography.__bin_to_int(rgb)

                # If this is a 'valid' position, store it
                # as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        # Crop the PIL.Image based on the 'valid' pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image


#Global Variables for storing image names
hostname=""
secretname=""
decodename=""

if __name__ == '__main__':
    #GUI initiated
    interface = Tk()

    #Assigning Host image name
    def openhost():
        global hostname
        hostname = filedialog.askopenfilename()

    #Assigning Secret image name
    def opensecret():
        global secretname
        secretname = filedialog.askopenfilename()

    #Assigning encoded image name
    def choosedec():
        global decodename
        decodename = filedialog.askopenfilename()

    #Function to call merge method
    def encodeb():
        print(secretname)
        print(hostname)
        merge = Steganography.merge(PIL.Image.open(str(hostname)),PIL.Image.open(str(secretname)))
        merge.save('encoded_i.png')
    
    #function to call unmerge method
    def decode():
        print(decodename)
        unmerg = Steganography.unmerge(PIL.Image.open(str(decodename)))
        unmerg.save('decoded_i.png')


    #Buttons for GUI
    button = ttk.Button(interface, text="Host Image", command=openhost)  # <------
    button.grid(column=1, row=1,ipady=5,ipadx=5)

    button2 = ttk.Button(interface,text="Secret Image",command=opensecret)
    button2.grid(column=3,row=1,ipady=5,ipadx=5)

    button3 = ttk.Button(interface,text="Encode",command=encodeb)
    button3.grid(column=2,row=2,ipady=5,ipadx=20)

    button4 = ttk.Button(interface,text="Decoded Image",command=choosedec)
    button4.grid(column=1,row=3,ipady=5,ipadx=5)

    button5 = ttk.Button(interface,text="Decode",command=decode)
    button5.grid(column=2,row=4,ipady=5,ipadx=20)

    interface.mainloop()