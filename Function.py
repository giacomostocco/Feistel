class Function:
	
	@staticmethod
	def permutation(data, key):
		#print "->", data.length()-key
		permutationData = data[(data.length()-key):]
		#print "->", permutationData
		permutationData.extend(data[0:data.length()-key])
		#print "->", data[0:data.length()-key]
		#print "->", permutationData
		return permutationData
