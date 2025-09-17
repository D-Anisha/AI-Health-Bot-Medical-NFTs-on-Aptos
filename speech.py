import speech_recognition as sr
import time
import nltk
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources (only the first time)
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Function to get audio input
def audio_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now... (3-second pause max, 15 sec total)")
        r.adjust_for_ambient_noise(source)
        audio_data = []
        end_time = time.time() + 15
        last_audio_time = time.time()

        while time.time() < end_time:
            try:
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
                audio_data.append(audio)
                last_audio_time = time.time()
            except sr.WaitTimeoutError:
                if time.time() - last_audio_time > 2:
                    print("Paused too long. Stopping.")
                    break
                else:
                    continue

        print("Recording done!")

    if audio_data:
        combined_audio = sr.AudioData(
            b''.join([a.get_raw_data() for a in audio_data]),
            audio_data[0].sample_rate,
            audio_data[0].sample_width
        )

        try:
            text = r.recognize_google(combined_audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print(" Sorry, could not understand the audio.")
        except sr.RequestError as e:
            print(" API Error:", e)
    else:
        print(" No audio recorded.")
    return None

# Function to get text input
def text_input():
    user_input = input("Enter your text here: ")
    return user_input

# Choose input mode
mode = input("Choose input mode (audio/text): ").strip().lower()
final_text = None
if mode == "audio":
    final_text = audio_input()
elif mode == "text":
    final_text = text_input()
else:
    print("Invalid input mode. Please choose 'audio' or 'text'.")

# NLP processing
if final_text:
    print("\nFinal captured input:", final_text)

    # Tokenization, Lowercasing, Stopword removal, Lemmatization
    words = nltk.word_tokenize(final_text)
    tokens = [lemmatizer.lemmatize(w.lower(), pos='v') 
              for w in words 
              if w.lower() not in stop_words and w.isalpha()]

    print("Processed tokens:", tokens)

    # Symptom binary vector
    symptom_list = [  # truncated for brevity, keep full list in real code
        'anxiety and nervousness', 'depression', 'shortness of breath', 'chest pain', 
        'headache', 'cough', 'fatigue', 'fever', 'insomnia', 'sore throat'
        # ... (rest of the 770 symptoms)
    ]

    # Binary vector creation
    input_vector = [1 if symptom in ' '.join(tokens) else 0 for symptom in symptom_list]
    print("Symptom vector:", input_vector)
