from PIL import Image
import os, sys
import uuid
from io import StringIO, BytesIO
import base64
from PIL import ExifTags
from logokilke.paths import logo_dir, save_dir, logo_list

# 'fb_profile.jpg' logo is excluded, good or bad?

"""
Inserts a given logo on a given image, customize the corner where logo is placed.
0 = top left, 1 = top right, 2 = bottom left, 3 = bottom right
"""
def add_logo(input_img, input_logo, location):
    # Fix img types to support transparency
    if not input_img.mode =="RGBA":
        input_img.convert("RGBA")
    if not input_logo.mode == "RGBA":
        input_logo.convert("RGBA")

    # Flip image if EXIF tags specify direction
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(input_img._getexif().items())

        if exif[orientation] == 3:
            input_img = input_img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            input_img = input_img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            input_img = input_img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass

    # Set up output image variable
    output_img = input_img.copy()

    # Resize logo width to X % of input image's shortest side (horizontal/vertical)
    l_scale = 0.25 # Logo Scale (values 0.00-1.00)
    l_new_width = int(min(input_img.size[0], input_img.size[1]) * l_scale)
    l_percent = (l_new_width / float(input_logo.size[0])) # Logo height scaling Percent
    l_new_height = int((float(input_logo.size[1]) * float(l_percent)))

    rs_l_image = input_logo.resize((l_new_width, l_new_height), Image.ANTIALIAS) # Resize logo

    i_box = input_img.getbbox() # original Image Box
    rs_l_box = rs_l_image.getbbox() #ReSized Logo Box

    # Place the logo to defined corner of input image
    b = int(0.08*l_new_width) # buffer to move the logo from the edge of img
    box_coords = ()

    if location == 0:
        box_coords = (i_box[0] - rs_l_box[0] + b,
                      i_box[1] - rs_l_box[1] + b)
    elif location == 1:
        box_coords = (i_box[2] - rs_l_box[2] - b,
                      i_box[1] - rs_l_box[1] + b)
    elif location == 2:
        box_coords = (i_box[1] - rs_l_box[1] + b,
                      i_box[3] - rs_l_box[3] - b)
    elif location == 3:
        box_coords = (i_box[2] - rs_l_box[2] - b,
                      i_box[3] - rs_l_box[3] - b)

    try:
        output_img.paste(rs_l_image, box_coords, rs_l_image)
    except:
        output_img.paste(rs_l_image, box_coords)

    return output_img


"""
 Create and save multiple logos, returns output file names
 Requires list of corners (values 0-3) and list of logos (filenames) to be used
 quality for saved images from 0 to 95
"""
def logofy(images, logos, corners=[3], quality_level = 95):
    # Store names of saved images
    b64_images = []
    # Create one pic with each logo
    index = 0
    # Loop through all input images
    for image in images:
        # Loop through all input logos
        for logo in logos:
            # Loop through all logo positions
            for corner in corners:
                output = BytesIO()
                new_image = add_logo(image, logo, corner)
                #file_name = str(index) + '-' + uuid.uuid4().hex + '.jpg'
                #new_image.convert('RGB').save(os.path.join(save_dir, file_name), quality=quality_level, optimize=True)
                new_image.convert('RGB').save(output, format='JPEG', quality=quality_level, optimize=True)
                output = output.getvalue()
                index += 1
                b64_images.append('data:image/jpg;base64,' + base64.b64encode(output).decode())
    return b64_images
