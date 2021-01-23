import os


IMAGES_DIR = 'images/'

def search(q):
	images_list = os.listdir(IMAGES_DIR)	
	print('images_list', images_list)
	print('q', q)
	results = list()

	for image in images_list:
		if q in image.title():
			results.append(image)
	return results