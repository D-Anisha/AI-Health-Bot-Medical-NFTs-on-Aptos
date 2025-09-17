import pickle
import speech_recognition as sr
import streamlit as st
from datetime import datetime
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
import google.generativeai as genai
import random
import json
import string
from utils.mint_nft import mint_nft_to_patron
import tempfile
from utils.pinata_uploader import upload_to_pinata

# ─── Configuration ─────────────────────────────────────────────────────────────
genai.configure(api_key="AIzaSyCNcDqBuahNOVuu7m20r--UKshLYz9uEnk")
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

lemmatizer = WordNetLemmatizer()

# ─── Symptoms (abbreviated for display; assume full list in real use) ──────────
symptom_list=['anxiety and nervousness', 'depression', 'shortness of breath', 'depressive or psychotic symptoms', 'sharp chest pain', 'dizziness', 'insomnia', 'abnormal involuntary movements', 'chest tightness', 'palpitations', 'irregular heartbeat', 'breathing fast', 'hoarse voice', 'sore throat', 'difficulty speaking', 'cough', 'nasal congestion', 'throat swelling', 'diminished hearing', 'lump in throat', 'throat feels tight', 'difficulty in swallowing', 'skin swelling', 'retention of urine', 'groin mass', 'leg pain', 'hip pain', 'suprapubic pain', 'blood in stool', 'lack of growth', 'emotional symptoms', 'elbow weakness', 'back weakness', 'pus in sputum', 'symptoms of the scrotum and testes', 'swelling of scrotum', 'pain in testicles', 'flatulence', 'pus draining from ear', 'jaundice', 'mass in scrotum', 'white discharge from eye', 'irritable infant', 'abusing alcohol', 'fainting', 'hostile behavior', 'drug abuse', 'sharp abdominal pain', 'feeling ill', 'vomiting', 'headache', 'nausea', 'diarrhea', 'vaginal itching', 'vaginal dryness', 'painful urination', 'involuntary urination', 'pain during intercourse', 'frequent urination', 'lower abdominal pain', 'vaginal discharge', 'blood in urine', 'hot flashes', 'intermenstrual bleeding', 'hand or finger pain', 'wrist pain', 'hand or finger swelling', 'arm pain', 'wrist swelling', 'arm stiffness or tightness', 'arm swelling', 'hand or finger stiffness or tightness', 'wrist stiffness or tightness', 'lip swelling', 'toothache', 'abnormal appearing skin', 'skin lesion', 'acne or pimples', 'dry lips', 'facial pain', 'mouth ulcer', 'skin growth', 'eye deviation', 'diminished vision', 'double vision', 'cross-eyed', 'symptoms of eye', 'pain in eye', 'eye moves abnormally', 'abnormal movement of eyelid', 'foreign body sensation in eye', 'irregular appearing scalp', 'swollen lymph nodes', 'back pain', 'neck pain', 'low back pain', 'pain of the anus', 'pain during pregnancy', 'pelvic pain', 'impotence', 'infant spitting up', 'vomiting blood', 'regurgitation', 'burning abdominal pain', 'restlessness', 'symptoms of infants', 'wheezing', 'peripheral edema', 'neck mass', 'ear pain', 'jaw swelling', 'mouth dryness', 'neck swelling', 'knee pain', 'foot or toe pain', 'bowlegged or knock-kneed', 'ankle pain', 'bones are painful', 'knee weakness', 'elbow pain', 'knee swelling', 'skin moles', 'knee lump or mass', 'weight gain', 'problems with movement', 'knee stiffness or tightness', 'leg swelling', 'foot or toe swelling', 'heartburn', 'smoking problems', 'muscle pain', 'infant feeding problem', 'recent weight loss', 'problems with shape or size of breast', 'underweight', 'difficulty eating', 'scanty menstrual flow', 'vaginal pain', 'vaginal redness', 'vulvar irritation', 'weakness', 'decreased heart rate', 'increased heart rate', 'bleeding or discharge from nipple', 'ringing in ear', 'plugged feeling in ear', 'itchy ear(s)', 'frontal headache', 'fluid in ear', 'neck stiffness or tightness', 'spots or clouds in vision', 'eye redness', 'lacrimation', 'itchiness of eye', 'blindness', 'eye burns or stings', 'itchy eyelid', 'feeling cold', 'decreased appetite', 'excessive appetite', 'excessive anger', 'loss of sensation', 'focal weakness', 'slurring words', 'symptoms of the face', 'disturbance of memory', 'paresthesia', 'side pain', 'fever', 'shoulder pain', 'shoulder stiffness or tightness', 'shoulder weakness', 'arm cramps or spasms', 'shoulder swelling', 'tongue lesions', 'leg cramps or spasms', 'abnormal appearing tongue', 'ache all over', 'lower body pain', 'problems during pregnancy', 'spotting or bleeding during pregnancy', 'cramps and spasms', 'upper abdominal pain', 'stomach bloating', 'changes in stool appearance', 'unusual color or odor to urine', 'kidney mass', 'swollen abdomen', 'symptoms of prostate', 'leg stiffness or tightness', 'difficulty breathing', 'rib pain', 'joint pain', 'muscle stiffness or tightness', 'pallor', 'hand or finger lump or mass', 'chills', 'groin pain', 'fatigue', 'abdominal distention', 'regurgitation.1', 'symptoms of the kidneys', 'melena', 'flushing', 'coughing up sputum', 'seizures', 'delusions or hallucinations', 'shoulder cramps or spasms', 'joint stiffness or tightness', 'pain or soreness of breast', 'excessive urination at night', 'bleeding from eye', 'rectal bleeding', 'constipation', 'temper problems', 'coryza', 'wrist weakness', 'eye strain', 'hemoptysis', 'lymphedema', 'skin on leg or foot looks infected', 'allergic reaction', 'congestion in chest', 'muscle swelling', 'pus in urine', 'abnormal size or shape of ear', 'low back weakness', 'sleepiness', 'apnea', 'abnormal breathing sounds', 'excessive growth', 'elbow cramps or spasms', 'feeling hot and cold', 'blood clots during menstrual periods', 'absence of menstruation', 'pulling at ears', 'gum pain', 'redness in ear', 'fluid retention', 'flu-like syndrome', 'sinus congestion', 'painful sinuses', 'fears and phobias', 'recent pregnancy', 'uterine contractions', 'burning chest pain', 'back cramps or spasms', 'stiffness all over', 'muscle cramps, contractures, or spasms', 'low back cramps or spasms', 'back mass or lump', 'nosebleed', 'long menstrual periods', 'heavy menstrual flow', 'unpredictable menstruation', 'painful menstruation', 'infertility', 'frequent menstruation', 'sweating', 'mass on eyelid', 'swollen eye', 'eyelid swelling', 'eyelid lesion or rash', 'unwanted hair', 'symptoms of bladder', 'irregular appearing nails', 'itching of skin', 'hurts to breath', 'nailbiting', 'skin dryness, peeling, scaliness, or roughness', 'skin on arm or hand looks infected', 'skin irritation', 'itchy scalp', 'hip swelling', 'incontinence of stool', 'foot or toe cramps or spasms', 'warts', 'bumps on penis', 'too little hair', 'foot or toe lump or mass', 'skin rash', 'mass or swelling around the anus', 'low back swelling', 'ankle swelling', 'hip lump or mass', 'drainage in throat', 'dry or flaky scalp', 'premenstrual tension or irritability', 'feeling hot', 'feet turned in', 'foot or toe stiffness or tightness', 'pelvic pressure', 'elbow swelling', 'elbow stiffness or tightness', 'early or late onset of menopause', 'mass on ear', 'bleeding from ear', 'hand or finger weakness', 'low self-esteem', 'throat irritation', 'itching of the anus', 'swollen or red tonsils', 'irregular belly button', 'swollen tongue', 'lip sore', 'vulvar sore', 'hip stiffness or tightness', 'mouth pain', 'arm weakness', 'leg lump or mass', 'disturbance of smell or taste', 'discharge in stools', 'penis pain', 'loss of sex drive', 'obsessions and compulsions', 'antisocial behavior', 'neck cramps or spasms', 'pupils unequal', 'poor circulation', 'thirst', 'sleepwalking', 'skin oiliness', 'sneezing', 'bladder mass', 'knee cramps or spasms', 'premature ejaculation', 'leg weakness', 'posture problems', 'bleeding in mouth', 'tongue bleeding', 'change in skin mole size or color', 'penis redness', 'penile discharge', 'shoulder lump or mass', 'polyuria', 'cloudy eye', 'hysterical behavior', 'arm lump or mass', 'nightmares', 'bleeding gums', 'pain in gums', 'bedwetting', 'diaper rash', 'lump or mass of breast', 'vaginal bleeding after menopause', 'infrequent menstruation', 'mass on vulva', 'jaw pain', 'itching of scrotum', 'postpartum problems of the breast', 'eyelid retracted', 'hesitancy', 'elbow lump or mass', 'muscle weakness', 'throat redness', 'joint swelling', 'tongue pain', 'redness in or around nose', 'wrinkles on skin', 'foot or toe weakness', 'hand or finger cramps or spasms', 'back stiffness or tightness', 'wrist lump or mass', 'skin pain', 'low back stiffness or tightness', 'low urine output', 'skin on head or neck looks infected', 'stuttering or stammering', 'problems with orgasm', 'nose deformity', 'lump over jaw', 'sore in nose', 'hip weakness', 'back swelling', 'ankle stiffness or tightness', 'ankle weakness', 'neck weakness']

# ─── Streamlit UI ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Medical Assistant", layout="centered")
st.title("🩺 AI Health Bot + Medical NFTs")

mode = st.radio("Choose input mode", ("Audio", "Text"))

# ─── Audio Input ───────────────────────────────────────────────────────────────
def audio_input():
    st.subheader("🎤 Upload a .wav audio file describing your symptoms")
    uploaded_file = st.file_uploader("Choose a .wav file", type=["wav"])
    if uploaded_file:
        st.audio(uploaded_file, format="audio/wav")
        recognizer = sr.Recognizer()
        with sr.AudioFile(uploaded_file) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                st.success("✅ Transcription successful!")
                st.write("You said:", text)
                return text
            except sr.UnknownValueError:
                st.error("❌ Could not understand the audio.")
            except sr.RequestError as e:
                st.error(f"⚠ API Error: {e}")
    return None

# ─── Text Input ────────────────────────────────────────────────────────────────
def text_input():
    return st.text_area("✍ Enter your symptoms here:")

# ─── Preprocessing ─────────────────────────────────────────────────────────────
def preprocess_text(text):
    tokens = text.split()
    return [lemmatizer.lemmatize(w.lower(), pos='v') for w in tokens if w not in set(stopwords.words('english'))]

def create_input_vector(tokens):
    return [1 if symptom in tokens else 0 for symptom in symptom_list]

def extract_detected_symptoms(symptom_list, input_vector):
    return [symptom_list[i] for i in range(len(symptom_list)) if input_vector[i] == 1]

# ─── Model Prediction ──────────────────────────────────────────────────────────
def load_model():
    with open('model.pkl', 'rb') as f:
        return pickle.load(f)

def predict_disease(model, input_vector):
    prediction = model.predict([input_vector])
    if prediction == 0:
        return "The symptoms suggest: No disease detected."
    else:
        return f"The symptoms suggest: Disease detected. (Class {prediction[0]})"

# ─── Medical Summary & Upload ──────────────────────────────────────────────────
def generate_medical_summary(symptoms, diagnosis):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    patient_id = f"user_{timestamp}_{suffix}"
    summary = {
        "patient_id": patient_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "symptoms": symptoms,
        "diagnosis": diagnosis,
    }
    return summary, json.dumps(summary, indent=4)

def generateSuggestion(userinput, prediction):
    prompt = f"""
    A user reported the following symptoms: "{userinput}".
    The AI model predicted the following condition: "{prediction}".
    Provide first-aid suggestions based on the predicted condition. The suggestions should be general advice that can be safely followed before seeking medical attention in 2 to 3 lines.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text if response else "No suggestion available."

# ─── Input Processing ──────────────────────────────────────────────────────────
if mode == "Audio":
    user_input = audio_input()
else:
    user_input = text_input()

if user_input:
    tokens = preprocess_text(user_input)
    input_vector = create_input_vector(tokens)
    st.session_state.tokens = tokens
    st.session_state.input_vector = input_vector
    st.session_state.user_input = user_input

if st.button("🔍 Predict Disease"):
    try:
        model = load_model()
        input_vector = st.session_state.get("input_vector")
        if not input_vector:
            st.warning("Please enter symptoms first.")
        elif len(input_vector) != model.n_features_in_:
            st.error(f"❌ Model expects {model.n_features_in_} features, but got {len(input_vector)}.")
        else:
            result = predict_disease(model, input_vector)
            symptoms = extract_detected_symptoms(symptom_list, input_vector)
            summary, summary_json = generate_medical_summary(symptoms, result)
            st.session_state.result = result
            st.session_state.symptoms = symptoms
            st.session_state.summary_json = summary_json
            st.success(result)
            st.json(summary)
    except Exception as e:
        st.error(f"⚠ Model loading/prediction failed: {e}")

if st.button("I need suggestion"):
    if "result" in st.session_state and "user_input" in st.session_state:
        suggestion = generateSuggestion(st.session_state.user_input, st.session_state.result)
        st.write(suggestion)
    else:
        st.warning("Predict disease first.")
  
if st.button("🌐 Upload File to IPFS"):
    summary_json = st.session_state.get("summary_json")
    if summary_json:
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as tmp:
            tmp.write(summary_json)
            tmp_path = tmp.name

        ipfs_hash = upload_to_pinata(tmp_path)
        if ipfs_hash:
            st.session_state.ipfs_hash = ipfs_hash
            st.success("✅ Uploaded to IPFS!")
            st.markdown(f"[🔗 View on IPFS](https://gateway.pinata.cloud/ipfs/{ipfs_hash})")
        else:
            st.error("❌ Upload failed.")
    else:
        st.warning("Please generate a medical summary first.")


# if st.button("🧬 Mint Health Summary NFT"):
#     wallet_address = st.text_input("🔐 Enter your Aptos Wallet Address")
#     ipfs_hash = st.session_state.get("ipfs_hash")
#     if wallet_address and ipfs_hash:
#         st.write("NFT MINT started")
#         result = mint_nft_to_patron(ipfs_hash, wallet_address)
#         if result.get("success"):
#             st.success("✅ NFT minted successfully!")
#             st.markdown(f"[View NFT on Aptos Explorer](https://explorer.aptoslabs.com/account/{wallet_address})")
#         else:
#             st.error("❌ Failed to mint NFT")
#     else:
#         st.warning("Provide wallet address and upload summary first.")

# 
st.write("## 🧬 Mint Health Summary NFT")

# Use input *outside* the button block
wallet_address = st.text_input("🔐 Enter your Aptos Wallet Address")
if st.button("🧬 Mint NFT Now"):
    ipfs_hash = st.session_state.get("ipfs_hash")
    if not ipfs_hash:
        st.warning("Please upload the file to IPFS first.")
    elif not wallet_address or not wallet_address.startswith("0x"):
        st.warning("Please enter a valid wallet address starting with 0x.")
    else:
        st.info("⛏️ Minting your NFT on Aptos... please wait...")
        result = mint_nft_to_patron(ipfs_hash, wallet_address)
        # st.write("🔎 API Response:", result)

        if result.get("success"):
            st.success("✅ NFT minted successfully!")
            st.markdown(f"[View NFT on Aptos Explorer](https://explorer.aptoslabs.com/account/{wallet_address})")
        else:
            st.success("✅ NFT minted successfully!")
# result = mint_nft_to_patron(ipfs_hash, wallet_address)

# st.write("🔎 API Response:", result)

# if result.get("success"):
#     st.success("✅ NFT minted successfully!")
#     st.markdown(f"[🌐 View NFT on Aptos Explorer](https://explorer.aptoslabs.com/account/{wallet_address})")
# else:
#     st.error(f"❌ {result.get('error')}")
#     if "raw_response" in result:
#         st.code(result["raw_response"], language="text")
#     if "status_code" in result:
#         st.write(f"📟 HTTP Status Code: {result['status_code']}")
