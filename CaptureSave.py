import os
import json


def save(image, image_name='EasyCapture.png'):
    with open('settings.json') as f:
        settings = json.load(f)
    directory = settings['folder']
    copy = 0
    if image_name == 'EasyCapture.png':
        saved_name = image_name.strip('.png') + ' (1).png'
    else:
        saved_name = image_name.strip('.png') + '.png'
    while os.path.exists(directory + "/" + saved_name):
        copy += 1
        saved_name = image_name.strip('.png') + ' ({})'.format(copy) + '.png'
    image.save(directory + '/' + saved_name, 'PNG')

