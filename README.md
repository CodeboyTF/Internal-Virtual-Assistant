# # SISAL ENQUIRY ASSISTANT.

**## OVERVIEW.**

This Project is about A Company based Virtual Assistant (Chatbot).The Sisal Chatbot is an intelligent conversational assistant designed to provide automated responses to user inquiries related to gambling services.
It is built using Flask and Socket.IO for real-time communication and integrates Natural Language Processing (NLP) and fuzzy matching to improve response accuracy.
The chatbot is designed to enhance user engagement and provide instant assistance on a website.

**## FEATURES.**

**1 . Real-time Communication:** Uses Flask and Socket.IO for instant interaction.

**2 . Natural Language Processing (NLP):** Preprocesses user messages using tokenization and stopword removal.

**3 . Fuzzy Matching:** Enhances response accuracy by using similarity matching on user queries.

**4 .Secure Data Handling:**

    -Encrypts all CSV files and datasets to ensure data security.

    -Implements Splunk for logging and monitoring chatbot activity.

**5 .User-Friendly Interface:** Designed with an interactive chat popup on a dummy website.

**6 .Machine Learning Integration (Upcoming):**

    -Improve intent recognition using deep learning models.

    -Implement clustering to classify user queries for better response accuracy.

**## TECHNOLOGIES USED.**

**1. Backend:** Flask, Socket.IO, Python.

**2.Frontend**: HTML, CSS, JavaScript.

**3.NLP Libraries:** NLTK, FuzzyWuzzy.

**4.Data Analysis:** Csv, DataSet.

**5.Security:** CSV encryption, Splunk for logging and monitoring.

**## INSTALLATION**

**1.Clone The Repository.**
```python
git clone https://pta-git2.csir.co.za/FMakharamedzha/sisal-virtual-assistant.git
cd sisal-chatbot
```

**2.Install Dependencies.**
```python
pip install -r requirements.txt
```

**3.Download required NLTK datasets:**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

**4.Run the application:**
```python
python app.py
```
**## PROJECT STRUCTURE**

```python
├── static/
│   ├── css/
|   |-  images/
│   ├── js/
├── templates/
│   ├── index.html
├── tests/
│   ├── test_chatbot.py
├── app.py
├── Enquiries.csv
├── requirements.txt
├── README.md
```

**## SECURITY ENHANCEMENTS**

**### Data Encryption**

**All CSV files and datasets will be encrypted using the cryptography library to protect sensitive information.**

    -AES encryption will be used to secure stored data.

    -Decryption will be performed during chatbot interactions.

**### Logging and Monitoring with Splunk**

    -Integrate Splunk to monitor chatbot interactions and detect anomalies.

    -Store logs securely and analyze query trends.

**## FUTURE ENHANCEMENTS AND (NLP & MACHINE-LEARNING).**

    -Intent Recognition: Implement ML models to classify user queries accurately.

    -Sentiment Analysis: Analyze user sentiment to provide personalized responses.

    -Self-learning Model: Train a model to improve responses over time.

    -Chatbot Analytics Dashboard: Visualize chatbot performance and user engagement.

**## CONTRIBUTIONS**

**### Developers**
```python
1.Fhatuwani Tebogo Makharamedzha - [Lead Developer]

2.Harvest Ngobeni - [Lead Developer]
```

Feel free to contribute by submitting issues or pull requests. Follow the standard development workflow. (Company(csir/sisal developers))

**## LICENSE**

    -csir (Council for Scientific and Industrial Research)

    -sisal (Sport Italia Società a responsabilità limitata)

