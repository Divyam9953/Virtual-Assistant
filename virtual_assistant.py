#pip install audio
#pip install SpeechRecognition
#pip install gTTS
#pip install wikipedia

#Importing Libraries
import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

# Ignore any warning messages
warnings.filterwarnings('ignore')

# Record Audio and return it as string
def recordAudio():

	#Record the audio
	r = sr.Recognizer() # Creating a recognizer object

	# Opening the microphone and start recording
	with sr.Microphone() as source:
		print('Say Something!')
		audio = r.listen(source)

	# Use Google's Speech Recognition
	data = ''
	try:
		data = r.recognize_google(audio)
		print('You said: ' + data)
	except sr.UnknownValueError:# Check for unknown value errors
		print('Google Speech Recognition could not understand the audio, unknown error')
	except sr.RequestError as e:
		print('Request results from Google Speech Recognition service error ' + e)

	return data

# Function to get the virtual assistant response
def assistantResponse(text):

	print(text)

	#Convert the text to Speech
	myobj = gTTS(text=text, lang='en', slow=False)

	# Save the converted audio to a file
	myobj.save('assistant_response.mp3')


	# Play the converted file
	os.system('start assistant_response.mp3')


# Function for wake word(s) or phrase
def wakeWord(text):
	WAKE_WORDS = ['hi computer', 'okay computer'] # List of wake words


	text = text.lower() # Converting the text to all lower case

	# Check to see if the users command/text contains a wake word/phrase
	for phrase in WAKE_WORDS:
		if phrase in text:
			return True
	# If the wake word isn't found in the text from the loop and so it returns false
	return False

# Function to give the correct date
def getDate():

	now = datetime.datetime.now()
	my_date = datetime.datetime.today()
	weekday = calendar.day_name[my_date.weekday()] #e.g. Friday
	monthNum = now.month
	dayNum = now.day

	# A list of months
	month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']

	# A list of ordinal numbers
	ordinalNumbers = ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th','13th',
					  '14th','15th','16th','17th','18th','19th','20th','21st','22nd','23rd','24th','25th',
					  '26th','27th','28th','29th','30th','31st']

	return 'Today is '+ weekday + ' ' + month_names[monthNum - 1] + ' the ' + ordinalNumbers[dayNum - 1] + '. '

# Function to return a random greeting response
def greeting(text):

	#Greeting input
	GREETING_INPUTS = ['hi','hey','hola','greetings','wassup','hello']

	#Greeting response
	GREETING_RESPONSES = ['howdy','whats good','hello','hey there']

	#If the users inpiut is a greeting then return a randomly chosen greeting response
	for word in text.split():
		if word.lower() in GREETING_INPUTS:
			return random.choice(GREETING_RESPONSES) + '.'

	#If no greeting was detected then return an empty string
	return ''

# Function to get the persons first and last name from the text
def getPerson(text):

	wordList = text.split() #Splitting the text into list of words

	for i in range(0,len(wordList)):
		if i+3 <= len(wordList) - 1 and wordList[i].lower()=='who' and wordList[i+1].lower()=='is':
			return wordList[i+2] + ' '+ wordList[i+3]




while True:

    #record the audio
    text = recordAudio()
    response = '' 

    #check for the wake word / phrase
    if (wakeWord(text) == True):
        
        #check for greetings by the user
        response = response + greeting(text)

        #check to see if the user has said anything about data
        if('date' in text):
            get_date = getDate()
            response = response + ' '+get_date

        #check to see if the user said 'who is' 
        if('who is' in text):
            person = getPerson(text) 
            wiki = wikipedia.summary(person, sentences=2)
            response = response +' '+ wiki

        #assistant respond back using audio and text from response
        assistantResponse(response)