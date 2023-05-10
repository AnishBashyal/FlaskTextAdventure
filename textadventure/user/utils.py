import secrets, os
from flask import current_app
from PIL import Image

def save_profile_pic(form_profile_pic, current_image_filename):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_profile_pic.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/profile_pics', image_filename)

    output_size = (125,125)
    i = Image.open(form_profile_pic)
    i.thumbnail(output_size)
    i.save(image_path)

    if current_image_filename != "default.jpg":
        current_image_path = os.path.join(current_app.root_path, 'static/profile_pics', current_image_filename)
        os.remove(current_image_path)

    return image_filename
