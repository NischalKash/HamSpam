import random

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

	    words = words[1:]
	    #stores the words in the sentence

	    if label == 'spam':
	    	label = 1
	    else:
	    	label = 0

	    a.append(words)
	    b.append(label)

	return a,b


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



train_words,train_labels = refine_data(train_data)
#Stores the train data set in words and labels
test_words,test_labels = refine_data(test_data)
#Stores the test data set in words and labels



all_spam_words = []
all_ham_words = []
for i in range(len(train_words)):
	if train_labels[i]==1:
		all_spam_words+=train_words[i]
		#stores all the words whose messages were spam
	else:
		all_ham_words+=train_words[i]
		#stores all the words whose messages were ham


total_input_words = all_spam_words + all_ham_words
number_of_spam = len(all_spam_words)
number_of_ham = len(all_ham_words)



total_ham_messages = 0
total_spam_messages = 0
for label in train_labels:
    if label==1:
    	total_spam_messages+=1
    	#Total number of spam messages in dataset
    else:
        total_ham_messages+=1
        #Total number of ham messages in dataset


probability_spam = total_spam_messages/len(data)
probability_ham = total_ham_messages/len(data)



spam_dict = {}; ham_dict = {}
for word in all_spam_words:
	if word not in spam_dict:
		spam_dict[word] = 0
	else:
		spam_dict[word]+=1
#Storing the number of occurences of a word in spam
for word in all_ham_words:
	if word not in ham_dict:
		ham_dict[word] = 0
	else:
		ham_dict[word]+=1
#Storing the number of occurences of a word in ham


predictions = []
for i in range(len(test_words)):
		#initially we consider the test sentence to be spam and ham with their probability as 1
	initial_prob_ham = 1
	initial_prob_spam  = 1

	line = test_words[i]
	for words in line:
		if words in spam_dict:
			initial_prob_spam *= ((spam_dict[words]+0.01) / (number_of_spam + (0.01 * len(total_input_words))))
		else:
			initial_prob_spam *= (0.01/(number_of_spam + (0.01 * len(total_input_words))))
		if words in ham_dict:
			initial_prob_ham *= ((ham_dict[words]+0.01)/(number_of_ham + (0.01 * len(total_input_words))))
		else:
			initial_prob_ham *= (0.01/(number_of_ham + (0.01 * len(total_input_words))))
		#Laplace Smoothing


	final_spam_probability = initial_prob_spam * probability_spam
	final_ham_probability = initial_prob_ham * probability_ham
	#Stores the combined probability of a sentence being a spam or ham

	if final_spam_probability >= final_ham_probability:
		label = 1
	else:
		label = 0
	predictions.append(label)

accuracy_count = 0
for i in range(len(test_labels)):
	if predictions[i]==test_labels[i]:
		accuracy_count+=1
#Predicts accuracy

print("\nAccuracy: ",accuracy_count/len(test_labels)*100)









