# 🩺 AI Health Bot + Medical NFTs on Aptos  
**Domain:** AIML

`AI Health Bot` is a Streamlit-powered web application that classifies diseases based on user-reported symptoms (via text or audio input) using a trained Random Forest model. It integrates **Gemini AI** for health recommendations and securely mints health metadata as NFTs on the **Aptos blockchain (testnet)**.

---

## 🚀 Features

- **🗣️ Symptom Input via Audio or Text**  
  Users can either speak or type their symptoms for a diagnosis.

- **🧠 Disease Classification**  
  Predicts possible diseases from **770 classes** using a trained `RandomForestClassifier` on 378 symptoms.

- **💡 AI-Powered Health Tips**  
  Leverages Gemini API to offer personalized treatment suggestions and lifestyle tips.

- **📦 NFT Minting**  
  Automatically generates a private health summary and mints it as a **secure NFT** on the Aptos blockchain (testnet).

- **🌐 Streamlit UI**  
  Clean and intuitive web interface with support for both audio and text input.

---

## ✅ Real-World Use Cases

### 📍 Scenario 1: **Rural Clinic with No Doctor**
> In a remote village with limited medical access, a villager says:  
> *"Body pain, fever, slight cough…"*  
> AI bot analyzes and replies:  
> *"Possible viral fever. Rest, hydration, paracetamol recommended."*  
> A medical summary is generated and minted as an NFT, creating a tamper-proof, personal digital health record.

### 🏫 Scenario 2: **Students in Hostel**
> A college student reports symptoms at night via the web app.
> Helpful for applying medical leaves.
> The AI generates a diagnosis and mints a medical NFT —  
> The summary can be shown to a doctor, or even for leave approval without sharing full medical history.

### 👷 Scenario 3: **NGO Health Tracking for Migrants**
> Migrant workers without documentation use the bot.  
> Health records are stored securely via **anonymous NFTs** —  
> Ensuring **privacy**, **portability**, and **ownership** of medical data.

---

## 🧬 Tech Stack

| Layer       | Tools & Libraries |
|-------------|-------------------|
| **Frontend** | Streamlit |
| **ML Model** | RandomForestClassifier (`scikit-learn`) |
| **AI Integration** | Gemini API (Google Generative AI) |
| **Speech Input** | `speech_recognition`, `gTTS` |
| **Blockchain** | Aptos Wallet + CLI / SDK |
| **Metadata** | JSON format hosted via IPFS |

---

## 📁 Project Structure

```
ai-health-bot-medical-nfts-on-aptos/
│
├── app.py                     # 🎯 Main Streamlit app (UI + logic)
├── model.pkl                  # 🧠 Trained RandomForestClassifier (770 diseases, 378 symptoms)
├── requirements.txt           # 📦 List of dependencies
├── README.md                  # 📄 Full project description
│
├── idea/
│   └── AI Health Bot.iml      # IDE configuration
│        
├── dataset/
│   └── dataset10.csv          # Training data for disease classification
│   
├── model/
│   └── model.py               # Model training and evaluation scripts
│
├── speech/
│   └── speech.py              # Audio processing and speech recognition
│   
└── utils/
    ├── __init__.py            # Package initialization
    ├── mint_nft.py            # NFT minting functionality on Aptos
    └── pinata_uploader.py     # IPFS metadata upload via Pinata
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Aptos CLI installed
- Gemini API key
- Pinata API credentials (for IPFS)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd ai-health-bot-medical-nfts-on-aptos
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Environment Setup
Create a `.env` file with:
```env
GEMINI_API_KEY=your_gemini_api_key
PINATA_API_KEY=your_pinata_api_key
PINATA_SECRET_KEY=your_pinata_secret_key
APTOS_PRIVATE_KEY=your_aptos_private_key
```

### Step 4: Run Application
```bash
streamlit run app.py
```

---

## 🎯 How It Works

1. **Input Symptoms**: User speaks or types their health symptoms
2. **ML Processing**: RandomForest model analyzes symptoms against 378 features
3. **Disease Prediction**: Returns most likely disease from 770+ possible conditions
4. **AI Recommendations**: Gemini AI provides treatment suggestions and health tips
5. **NFT Generation**: Creates a secure health summary and mints it on Aptos testnet
6. **Blockchain Storage**: Medical metadata stored on IPFS, NFT address on Aptos

---

## 🔒 Privacy & Security

- **Anonymous Health Records**: NFTs can be minted without personal identification
- **Blockchain Immutability**: Medical records cannot be tampered with
- **User Ownership**: Only the user holds the private key to their health NFTs
- **IPFS Storage**: Decentralized metadata storage ensures data availability

---

## 📊 Model Performance

- **Dataset**: 770 disease classes, 378 symptom features
- **Algorithm**: Random Forest Classifier
- **Accuracy**: Optimized for real-world symptom combinations
- **Training Data**: Comprehensive medical symptom-disease mappings

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Disclaimer

**This application is for educational and informational purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with questions regarding medical conditions.**

---

## 📞 Support

For support, email [anisha2004.d@gmail.com] or create an issue in this repository.

---

## 🏆 Acknowledgments

- **Aptos Blockchain** for secure NFT infrastructure
- **Google Gemini AI** for intelligent health recommendations
- **Streamlit** for rapid web app development
- **scikit-learn** for robust machine learning capabilities
