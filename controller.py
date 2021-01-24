import os
import dropbox

TOKEN = "n3HGT35DyvMAAAAAAAAAAdPwRdFRlc-b1ToPuFETfypR5rrGcxGw6qZeNZ3dd2B4"
IMAGES_DIR = 'images'

def upload_image(file, filename):
    print('filename', filename)
    try:
        dbx = dropbox.Dropbox(TOKEN)
        dbx.files_upload(file, f'/images/{filename}')
    except TypeError:
        dbx = dropbox.Dropbox(TOKEN)
        dbx.files_upload(get_file(filename), f'/{filename}',
                         mode=dropbox.files.WriteMode.overwrite)


def get_image(filename):
    dbx = dropbox.Dropbox(TOKEN)
    print('filename', filename)
    result = dbx.files_get_temporary_link(f'/images/{filename}')
    return result.link


def get_file(_filepath):
    f = open(_filepath, 'rb')
    return f.read()


def search(q):
    images_list = os.listdir(IMAGES_DIR)    
    results = list()

    for image in images_list:
        if q in image.title():
            results.append(image)
    return results

# if __name__ == '__main__':
    # for image in os.listdir('/home/amin/PycharmProjects/teacher_meme_bot/images/'):
    #     upload_image(image.title(), 'images/' + image.title().lower())
    #     print(image.title() + 'uploaded.')
    