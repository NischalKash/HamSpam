import random
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 


def refine_data(train_data):
	a = []
	b = []
	for line in train_data: 
	    line = line.lower()  
	    #converts all letters into lowercase 

	    line = line.replace("\t", ' ')
	    #replaces tab spaces to letter

	    words = line.split(' ')
	    #splits the message to get us the list of list of words

	    label = words[0]
	    #the first word os always the label

	    line_sentence = ' '.join(words[1:])
	    #stores the words as a sentence

	    if label == 'spam':
	    	label = 1
	    else:
	    	label = 0

	    a.append(line_sentence)
	    b.append(label)

	return a,b

def prediction(a,spam_sentences,ham_sentences):

	total1 = 0
	total2 = 0

	for i in spam_sentences:
		test_sentence_data = word_tokenize(a)
		#tokenizes the test data
		predict_sentence_data = word_tokenize(i.lower())
		#tokenizes the train data

		sw = stopwords.words('english')  
		#stores stop words in english
		l1 =[];l2 =[] 

		test_set = set()
		predict_set = set()

		for i in test_sentence_data:
			if i not in sw:
				test_set.add(i)
				#removes stop word from test
		for i in predict_sentence_data:
			if i not in sw:
				predict_set.add(i)
				#removes stop word from train

		rvector = test_set.union(predict_set)
		#Combining test set and train set

		#Checking whether a particular word lies in both test and train
		for j in rvector: 
			if j in test_set: 
				l1.append(1) 
			else: 
				l1.append(0) 
			if j in predict_set: 
				l2.append(1) 
			else: 
				l2.append(0) 
			
		c = 0
   		# Checking how many words are common and its count
		for i in range(len(rvector)): 
			if l1[i]==l2[i]:
				c += 1 

		cosine = c / float((sum(l1)*sum(l2))**0.5) 
		#Cosine Similarity Formula

		total1+=cosine  


	for i in ham_sentences:
		test_sentence_data = word_tokenize(a)
		#tokenizes the test data
		predict_sentence_data = word_tokenize(i.lower())
		#tokenizes the train data

		sw = stopwords.words('english') 
		#stores stop words in english 
		l1 =[];l2 =[] 

		test_set = set()
		predict_set = set()

		for i in test_sentence_data:
			if i not in sw:
				test_set.add(i)
				#removes stop word from test
		for i in predict_sentence_data:
			if i not in sw:
				predict_set.add(i)
				#removes stop word from train

		rvector = test_set.union(predict_set)
		#Combining test set and train set

		#Checking whether a particular word lies in both test and train
		for j in rvector: 
			if j in test_set: 
				l1.append(1) 
			else: 
				l1.append(0) 
			if j in predict_set: 
				l2.append(1) 
			else: 
				l2.append(0) 
			
		c = 0
   		# Checking how many words are common and its count

		for i in range(len(rvector)): 
			if l1[i]==l2[i]:
				c += 1 
		cosine = c / float((sum(l1)*sum(l2))**0.5) 
		#Cosine Similarity Formula

		total2+=cosine  

	return total1,total2 


prediction_count = 0
data = open('spam.csv').readlines()
#reads the input

total_data = len(data)

all_range_numbers = list(range(total_data))
#stores numbers from 0 to length of the messages

random.shuffle(all_range_numbers)
#shuffles the range of numbers 

train_limit = int(0.8*total_data)
#Spliting into test and train data

train_data_range = all_range_numbers[:train_limit]
#Stores train_data indexes corresponding to original data

test_data_range = all_range_numbers[train_limit:]
#Stores test_data indexes corresponding to original data


train_data = []
test_data = []
for i in train_data_range:
	train_data.append(data[i])
	#stores train data

for i in test_data_range:
	test_data.append(data[i])
	#stores test data



train_sentence,train_labels = refine_data(train_data)
#Stores the train data set in sentences and labels

test_sentence,test_labels = refine_data(test_data)
#Stores the test data set in sentences and labels


spam_sentences = []
ham_sentences = []

for i in range(len(train_sentence)):
	if train_labels[i]==1:
		spam_sentences.append(train_sentence[i])
		#separating spam sentences from ham
	else:
		ham_sentences.append(train_sentence[i])
		#separating ham sentences from spam

for i in range(len(test_sentence)):
	spam_val,ham_val = prediction(test_sentence[i].lower(),spam_sentences,ham_sentences)

	if spam_val>ham_val:
		prediction_value = 1
	else:
		prediction_value = 0

	if prediction_value==test_labels[i]:
		prediction_count+=1

print("The Accuracy is ")
#predicts accuracy
print(prediction_count/len(test_labels)*100)