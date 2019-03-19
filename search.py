# USAGE
# python search.py --index index.csv --query queries/103100.png --result-path dataset

# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
import argparse
import cv2
import os
import numpy as np

#Face Detection and Cropping
def crop(image_file,cascade_file = "lbpcascade_animeface.xml"):
	# Create classifier
    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(image_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = cascade.detectMultiScale(gray,
                    # detector options
                    scaleFactor = 1.1,
                    minNeighbors = 5,
                    minSize = (30, 30))
    if np.any(faces):
        for (x, y, w, h) in faces:
            crop_img = image[y:y+h, x:x+w]
            return crop_img
    else:
        return image

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
ap.add_argument("-q", "--query", required = True,
	help = "Path to the query image")
ap.add_argument("-r", "--result-path", required = True,
	help = "Path to the result path")
args = vars(ap.parse_args())

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and describe it

#cropped_query = crop(args["query"])
query = cv2.imread(args["query"])
features = cd.describe(query)

# perform the search
searcher = Searcher(args["index"])
results = searcher.search(features)

print(results)
# display the query
cv2.imshow("Query", query)

# loop over the results
for result in results:
	# load the result image and display it
	image = cv2.imread(args["result_path"] + "/" +result["judul"]+"_"+"frame"+str(result["frame ke"])+".jpg")
	cv2.imshow("Result", image)
	cv2.waitKey(0)
