# Health Chatbot - Streamlit App Guide

## 🚀 Quick Start

### Prerequisites
1. Make sure Ollama is running locally with the DeepSeek-V3.1 model
2. Ensure you have Python 3.8+ installed
3. The FAISS index should be present in the `faiss_index` folder

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the App

Run the Streamlit app with:
```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

## 📋 Features

- **Chat Interface**: Intuitive conversation-style interface
- **Medical Information**: Get information about:
  - Causes of medical conditions
  - Symptoms
  - Treatment options
  - Medicines
  - Prevention methods
- **Chat History**: View previous questions and answers in the session
- **Clear History**: Reset the conversation anytime
- **Safety Disclaimers**: Built-in warnings about seeking professional medical advice

## 🎯 How to Use

1. Type your health question in the chat input box
2. Press Enter or click the send button
3. Wait for the AI to search the medical knowledge base
4. Review the response with structured information
5. Continue asking follow-up questions as needed

## ⚙️ Configuration

The app uses the following configuration:
- **Model**: DeepSeek-V3.1 (via Ollama)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: FAISS with MMR search
- **Retrieval**: Top 5 most relevant documents

## 🛠️ Troubleshooting

### App won't start
- Check if Ollama is running: `ollama list`
- Verify the FAISS index exists in `faiss_index` folder
- Ensure all dependencies are installed

### Slow responses
- First query may be slower due to model initialization
- Subsequent queries should be faster (cached)

### Connection errors
- Verify Ollama is running on `http://localhost:11434`
- Check if the DeepSeek-V3.1 model is available

## 💡 Tips

- Be specific in your questions for better results
- Ask one question at a time for clearer answers
- Read the disclaimer before using the chatbot
- Remember this is for educational purposes only

## 🔧 Customization

To customize the app:
- Edit `app.py` to change the UI or styling
- Modify `src/prompt.py` to adjust response format
- Update `src/ollama_chain.py` to change model parameters

---

**Note**: Always consult healthcare professionals for medical advice. This chatbot is for educational purposes only.
