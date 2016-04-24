# -*- coding: utf-8 -*-

import PIL.Image as pil
import PIL.ImageOps as pilops
import numpy as np
import time
import random
import csv

def create_image_list(csv_path, predict=False):
	'''This method takes the path to a CSV file and saves all images in a list. If the parameter 'predict' is 'True', the labels will be ignored.'''
	
	# create list, which saves a dictionary for each image
	image_list = []

	# open CSV file to read images
	with open(csv_path) as csv_file:
		# create CSV reader
		csv_reader = csv.reader(csv_file, delimiter=";")

		# skip first line, which contains the headlines
		next(csv_reader)

		# iterate over images
		for image_row in csv_reader:
			# append image to image list
			if predict:
				image_list.append({'path': image_row[0]})
			else:
				image_list.append({'path': image_row[0], 'leftEyeX': image_row[3], 'leftEyeY': image_row[4], 'rightEyeX': image_row[5], 'rightEyeY': image_row[6]})

	#shuffle images
	random.shuffle(image_list)

	return image_list

def read_data(csv_path, resolution, d=None, normalize=True, autocontrast=True, return_image_properties=False, predict=False):
	'''In order to construct the data structures, which contain the training and test data, this method takes the path to a csv file, which saves information about the images. In addition, this method takes the 'resolution' to which the images are to be scaled, a parameter 'd' which determines how many images are to be processed, a boolean parameter 'normalize' which controls whether the images shall be normalized to the interval [0,1] and a boolean parameter 'autocontrast' which controls whether a PIL intern method shall be used to increase the contrast of the images. The boolean parameter 'return_image_properties' can be set to 'True' in order to return the image list created by the create_image_list method called within this method. If the flag 'predict' is set to 'True', the labels will be ignored'''
	#create image list
	image_list = create_image_list(csv_path, predict)

	# check whether there is a limit for the images to be loaded
	num_images = d if d is not None else len(image_list)

	# throw away everything behind the first d elements
	if d != len(image_list):
		image_list = image_list[:d]

	# create empty arrays with appropriate size
	X = np.empty((num_images, 3, resolution[0], resolution[1]), dtype=float)
	if not predict:
		y = np.empty((num_images, 4))

	# iterate over images
	for idx, image in enumerate(image_list):
		if idx >= num_images:
			break

		# open the image
		im = pil.open(image['path'])

		# autocontrast
		if autocontrast:
			im = pilops.autocontrast(im)

		# resize image to desired size
		im = im.resize(resolution)

		# save image as array within the result array
		X[idx] = np.transpose(np.asarray(im), [2,1,0])

		if not predict:
			# save target values
			y[idx][0] = image['leftEyeX']
			y[idx][1] = image['leftEyeY']
			y[idx][2] = image['rightEyeX']
			y[idx][3] = image['rightEyeY']

	# normalize images to range [0,1] if desired
	if normalize:
		X /= 255.0

	if not predict:
		if return_image_properties:
			return X, y, image_list
		else:
			return X, y
	else:
		if return_image_properties:
			return X, image_list
		else:
			return X


if __name__ == "__main__":
	X, y = read_data("data/MUCT_fixed/muct-landmarks/MUCT_TRAIN.csv", (48,68))
