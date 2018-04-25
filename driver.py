#Qianze Zhang 2018
#BibMerge: A tool to merge all preexisting .bib files from the USC Meaning lab while preserving maximum information
#To use:

#class definition for an individual bib entry
class Entry(object):
    def __init__(self, sitekey, entrytype, attributes):
    #all required fields!
        #Strings
        self.sitekey = sitekey
        self.entrytype = entrytype

        #dictionary (begins as empty)
        self.attributes = attributes

'''HELPER FUNCTIONS'''
def loadEntries(fileName):
	# this list holds all instances of entry objects
	entryList = []

	# read in the .bib entries
	in_file = open(fileName, "rt")  # open file for reading text data
	contents = in_file.read()  # read the entire file into a string variable
	in_file.close()  # close the file
	# print(contents)  		          # print contents (just for testing)

	# put individual entries in a list for processing
	entries = contents.split('@')

	# here is the for loop where you handle the entries
	for entry in entries:
		# get the entry type
		entrytype = entry.split('{', 1)[0]

		# get the entry sitekey
		entryAttributes = entry[len(entrytype) + 1:-2]
		#print(entryAttributes)

		sitekey = entryAttributes.split(',', 1)[0]

		entryAttributes = entryAttributes[len(sitekey) + 1:]
		# print(entryAttributes)

		# now each of the attribute should be on individual lines in entryAttributes

		# get all the attributes and put them into a dictionary
		attributesDict = {}

		# but first put all the attributes and their values into a list
		attributes = entryAttributes.split('\n')
		for attribute in attributes:
			# split the attributes into a dictionary, using the equals sign as a delimeter
			attrKey = attribute.split('=')[0]
			attrVal = attribute[len(attrKey) + 2:]
			attributesDict[attrKey] = attrVal

		newEntry = Entry(sitekey, entrytype, attributesDict)

		entryList.append(newEntry)

	return entryList

'''Capitalizes Significant words in given journal titles'''
def capTitle(title):

	return ''

'''MAIN METHOD'''
def main():
	entryList = loadEntries("test.txt")

	#this contains the sitekeys of all entries that lack DOIs
	#after processing all entries the contents of this list are outputted to noDOI.txt
	noDOI = []

	#check for duplicates using sitekeys
	#if duplicate sitekey is found, check to see if title is the same
	#if title is not the same, continue (these entries are not actually duplicates, they just have the same site keys)


	#load duplicate-free file into program and perform remaining content checks
	for entry in entryList:
		print(entry.attributes.keys())
		if entry.entrytype.lower() == "journal":
			#print("This entry is of journal type")
			#make sure journal title attribute field is properly titled
			entry.attributes['\tJournal'] = capTitle(attributes['\tJournal'])

		#if none of the attributes is a DOI, add the sitekey to a list of entries without DOIs
		if "\tDOI " not in entry.attributes.keys():
			noDOI.append(entry.sitekey)


	# write contents of noDOI into a file for other RAs to reference
	noDOIFile = open('noDOI.txt','w')

	for entry in noDOI:
		noDOIFile.write(entry)
		noDOIFile.write('\n')

	noDOIFile.close()

#for entry in noDOI:
		#print(entry)

		#if author name has intials, add the sitekey to a list of entries without full author names
		




	#choose the output file
	#rebuild file contents by going through the list of entries
	#close file stream

	


main()