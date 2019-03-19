# import the necessary packages
import numpy as np
import csv
from operator import itemgetter

class Searcher:
	def __init__(self, indexPath):
		# store our index path
		self.indexPath = indexPath

	def search(self, queryFeatures, limit = 5):
		# initialize our dictionary of results
		results = []
		fps = 23.976
		# open the index file for reading
		with open(self.indexPath) as f:
			# initialize the CSV reader
			reader = csv.reader(f)
			# loop over the rows in the index
			for row in reader:
				# parse out the image ID and features, then compute the
				# chi-squared distance between the features in our index
				# and our query features
				features = [float(x) for x in row[2:]]
				d = self.chi2_distance(features, queryFeatures)
				# now that we have the distance between the two feature
				# vectors, we can udpate the results dictionary -- the
				# key is the current image ID in the index and the
				# value is the distance we just computed, representing
				# how 'similar' the image in the index is to our query
				frame = row[1].split("frame")
				frame = frame[1].split(".jpg")
				frame = int(frame[0])
				detik = int(frame / fps)
				menit = str(int(detik / 60))
				detik = str(detik % 60)
				temp = {
				"judul" : row[0],
				"frame ke" : frame,
				"error" : d,
				"menit" : menit + ":" + detik
				}
				results.append(temp)

			# close the reader
			f.close()

		# sort our results, so that the smaller distances (i.e. the
		# more relevant images are at the front of the list)
		#results = sorted([(v, k) for (k, v) in results.items()])
		results = sorted(results, key=itemgetter('error'))
		# return our (limited) results
		return results[:limit]

	def chi2_distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])

		# return the chi-squared distance
		return d
