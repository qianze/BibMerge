#Qianze Zhang 2018
#BibMerge: A tool to merge all preexisting .bib files from the USC Meaning lab while preserving maximum information

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
	#list of words in journal titles that should not be capitalized
	dontCap = ["is", "of", "the", "a", "an", "to", "at", "in", "for", "on", "by", "and", "or", "nor", "but", "yet", "are", "was", "be", "do", "had"]

	#print(title)

	titleList = title.split(" ")

	#use this counter to tell whether or not the word is the first word in the journal title
	counter  = 0

	newTitleList = []

	for word in titleList:
		#print(word)
		if(word in dontCap) or word[0].isdigit():
			newTitleList.append(word)
			continue
		else:
			#word should be capitalized
			if(counter == 0):#you're on the first word of the title
				capTitle = word[:1] + '{' + word[1:]
				capTitle = capTitle[:3] + '}' + capTitle[3:]
				#print(capTitle)
				counter = counter +1
				newTitleList.append(capTitle)
			else:
				capTitle = '{' + word
				capTitle = capTitle[:2] + '}' + capTitle[2:]
				#print(capTitle)
				newTitleList.append(capTitle)

	#remake the title
	newTitle = ""

	for word in newTitleList:
		newTitle = newTitle + ' ' + word

	#print(newTitle)#note: there's a space in the beginning here, hope that's okay!


	return newTitle

'''MAIN METHOD'''
def main():
	entryList = loadEntries("test.txt")

	#this contains the sitekeys of all entries that lack DOIs
	#after processing all entries the contents of this list are outputted to noDOI.txt
	noDOI = []

	#check for duplicates using sitekeys
	#if duplicate sitekey is found, check to see if title is the same
	#if title is not the same, continue (these entries are not actually duplicates, they just have the same site keys

	authorInitList = []

	#checkin for duplicates
	for entry in entryList:
		tempEntry = entry
		#entryList.remove(entry)
		tempSiteKey = tempEntry.sitekey
		#print(tempSiteKey)
		counter = 0
		for otherEntry in entryList:
			if(otherEntry.sitekey == tempSiteKey):
				#print("we found a matching entry!")
				#check for any attributes that are in one but not the other and add em
				tempAttributes = otherEntry.attributes
				for attribute in tempAttributes:
					if attribute not in entry.attributes:
						entry.attributes[attribute] = otherEntry.attributes[attribute]

	#load duplicate-free file into program and perform remaining content checks
	for entry in entryList:
		if "\tJournal " in entry.attributes.keys():
			#print("This attribute is of journal type")
			#make sure journal title attribute field is properly titled
			entry.attributes['\tJournal '] = capTitle(entry.attributes['\tJournal '])

		if "\tBooktitle " in entry.attributes.keys():
			entry.attributes['\tBooktitle '] = capTitle(entry.attributes['\tBooktitle '])

		#if none of the attributes is a DOI, add the sitekey to a list of entries without DOIs
		if "\tDOI " not in entry.attributes.keys():
			noDOI.append(entry.sitekey)


	# write contents of noDOI into a file for other RAs to reference
	noDOIFile = open('noDOI.txt','w')

	for entry in noDOI:
		noDOIFile.write(entry)
		noDOIFile.write('\n')

	noDOIFile.close()

	#if author name has intials, add the sitekey to a list of entries without full author names
		#how to tell if an author name has initials?
	for entry in entryList:
		if "\tAuthor " in entry.attributes.keys():
			authorList = entry.attributes['\tAuthor '].split(' ')
			for name in authorList:
				if(len(name) == 1):
					authorInitList.append(entry.sitekey)
					break
				if('.' in name):
					authorInitList.append(entry.sitekey)

	authorInitFile = open('initials.txt', 'w')

	for entry in authorInitList:
		authorInitFile.write(entry)
		authorInitFile.write('\n')

	authorInitFile.close()

	#choose the output file
	#rebuild file contents by going through the list of entries
	#close file stream
	result = open('BIG.txt', 'w')

	counter = 0
	for entry in entryList:
		if(counter != 0):
			result.write('@' + entry.entrytype + '{' + entry.sitekey + ',')
			result.write('\n')
			counter = 0
			numAttributes = len(entry.attributes)
			counter2 = 1
			for attribute in entry.attributes:
				if counter != 0:
					result.write(attribute + '= ' + entry.attributes[attribute])
					if(counter2 != numAttributes):
						result.write('\n')
					else:
						result.write('}')
				counter = counter +1
				counter2 = counter2 + 1
			result.write('\n')
		counter = counter +1
	result.close()

main()