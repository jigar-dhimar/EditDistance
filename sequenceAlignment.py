# Jigar Dhimar 
# Algorithms - HW 6 
# Sequence Alignment 
# Due: 3/30/16 


def alphaCost(alphaSame, alphaDifferent, letter1, letter2):

	vowels = ["a", "e", "i", "o", "u"]

	if letter1 == letter2:
		return 0
	else: 
		if (letter1 in vowels) and (letter2 in vowels):
			return alphaSame
		elif (letter1 in vowels) and (letter2 not in vowels):
			return alphaDifferent
		elif (letter1 not in vowels) and (letter2 in vowels):
			return alphaDifferent
		elif (letter1 not in vowels) and (letter2 not in vowels): 
			return alphaSame

def traceback(costArray, initialString, resultString, delta, alphaSame,alphaDifferent, outputFile):

	i = len(resultString)
	j = len(initialString)

	traceArray = []
	

	while i>0 or j>0:	
		
		insertCost = 1000
		deleteCost = 1000
		swapOrIgnoreCost = 1000

		if costArray[i][j-1] == (costArray[i][j] - delta): 
			deleteCost = costArray[i][j-1]

		if costArray[i-1][j] == (costArray[i][j] - delta): 
			insertCost = costArray[i-1][j]

		if costArray[i][j] == costArray[i-1][j-1]:
			if resultString[i-1] == initialString[j-1]:
				swapOrIgnoreCost = costArray[i-1][j-1]
		elif costArray[i][j] - alphaCost(alphaSame, alphaDifferent, resultString[i-1], initialString[j-1]) == costArray[i-1][j-1]:
			swapOrIgnoreCost = costArray[i-1][j-1]

		########################### Traceback begins here ########################### 
		
		############### Swap or Ignore changes ###############
		if (swapOrIgnoreCost < insertCost) and (swapOrIgnoreCost < deleteCost):

			if resultString[i-1] == initialString[j-1]:

				move = "Ignore " + initialString[j-1] 
				traceArray.append(move)
				i = i - 1 
				j = j - 1 

			else:

				move = "Change " + initialString[j-1] + " to " + resultString[i-1] 
				traceArray.append(move)
				i = i - 1 
				j = j - 1

		elif (swapOrIgnoreCost < insertCost) and (swapOrIgnoreCost == deleteCost):

			if resultString[i-1] == initialString[j-1]:

				move = "Ignore " + initialString[j-1] 
				traceArray.append(move)
				i = i - 1 
				j = j - 1

			else:

				move = "Change " + initialString[j-1] + " to " + resultString[i-1] 
				traceArray.append(move)
				i = i - 1 
				j = j - 1


		elif (swapOrIgnoreCost == insertCost) and (swapOrIgnoreCost < deleteCost):

			if resultString[i-1] == initialString[j-1]:

				move = "Ignore " + initialString[j-1] 
				traceArray.append(move)
				i = i - 1 
				j = j - 1

			else:

				move = "Change " + initialString[j-1] + " to " + resultString[i-1] 
				traceArray.append(move)
				i = i - 1 
				j = j - 1

		############### Delete ###############

		elif (deleteCost < swapOrIgnoreCost):

			if (deleteCost < insertCost) or (deleteCost == insertCost):

				move = "Delete " + initialString[j-1]
				traceArray.append(move)
				j = j -1 

		elif (deleteCost == insertCost):
			
			move = "Delete " + initialString[j-1]
			traceArray.append(move)
			j = j -1 


		############### Insert ################
		
		elif (insertCost < deleteCost) and (insertCost < swapOrIgnoreCost):

			move = "Insert " + resultString[i-1]
			traceArray.append(move)

			i = i - 1
		
	############### Writing edits into the output text file ###############
	
	## Start edit 
	outputFile.write("Start!" + "\t\t\t" + initialString + "\n")
	
	## String to accumulate edits 
	tempString = ""

	## Counters to keep track of what position you're at in each string ##
	indexCounter = 0
	initialStringCounter = 0 
	resultStringCounter = 0
	
	for i in range(1, len(traceArray)+1):
		if "Ignore" in (traceArray[-1*i]):
			tempString = tempString + initialString[initialStringCounter]
			initialStringCounter += 1
			resultStringCounter += 1 

			edit = (traceArray[-1*i]) + "." + "\t\t" + tempString + initialString[initialStringCounter:] + "\n"
			outputFile.write(edit)
		elif "Change" in (traceArray[-1*i]):

			tempString = tempString + (traceArray[-1*i])[12]
			initialStringCounter += 1
			resultStringCounter += 1 

			edit = (traceArray[-1*i]) + "." + "\t\t" + tempString + initialString[initialStringCounter:] + "\n"
			outputFile.write(edit)
		elif "Delete" in (traceArray[-1*i]):
			initialStringCounter += 1

			edit = (traceArray[-1*i]) + "." + "\t\t" + tempString + initialString[initialStringCounter:] + "\n"
			outputFile.write(edit)

		elif "Insert" in (traceArray[-1*i]):

			tempString = tempString + (traceArray[-1*i])[7]
			resultStringCounter += 1 

			edit = (traceArray[-1*i]) + "." + "\t\t" + tempString + initialString[initialStringCounter:] + "\n"
			outputFile.write(edit)


def editDistance(string1, string2, delta, alphaDifferent, alphaSame, outputFile):

	length1 = len(string1)
	length2 = len(string2)


	################## Initializing 2D array ####################### 
	costArray = [[0 for i in range(length1+1)] for j in range(length2+1)] 

	for i in range(1, length2+1):
		costArray[i][0] = delta * i
	for j in range(1, length1+1):
		costArray[0][j] = delta * j 


	################## Write basic info to file ####################### 
	strings = string1 + " " + string2 + "\n"
	outputFile.write(strings)
	costs = str(delta) + " " + str(alphaDifferent) + " " + str(alphaSame) 
	outputFile.write(costs)
	


	################## Actual edit distance code ####################### 

	for i in range(1,length2+1):
		for j in range(1,length1+1):
			
			costArray[i][j] = min( alphaCost(alphaSame, alphaDifferent, string2[i-1], string1[j-1]) + costArray[i-1][j-1] , 
								   delta + costArray[i-1][j], 
								   delta + costArray[i][j-1])


	######### Writing final cost to output file // Call to traceback funnction #########
	outputFile.write("\n")
	traceback(costArray, string1, string2, delta, alphaSame, alphaDifferent, outputFile)

	outputFile.write("\n")
	costString = "Edit Distance:" + " " + str(costArray[length2][length1]) + "\n"
	outputFile.write(costString)
	outputFile.write("\n")
	outputFile.write("-----------------------------------" + "\n")
	outputFile.write("\n")


	################## return array #######################
	return costArray

def main():

	validFile = False
	fileContents = []
	
	################### Getting data from file ###################### 
	while validFile == False: 
		
		prompt = input("Enter name of input text file (include .txt): ")

		try:

			file = open(prompt, "r", encoding="utf-8")
			fileString = file.read()
			fileList = fileString.split()

			file.close()
			for item in fileList:
				fileContents.append(item)
			validFile = True 

		except IOError:

			print("Oops file not found!")
			print("")
	

	################## callng edit distance function ####################### 
	items = 0

	outputFile = open("outputFile.txt", "w")
	
	while items < len(fileContents):
		editDistance(fileContents[0+items], fileContents[1+items], int(fileContents[2+items]), int(fileContents[3+items]), int(fileContents[4+items]), outputFile)
		items+=5

	outputFile.close()
	print("Results have been written to outputFile.txt!")

main()

