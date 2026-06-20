# 📚 AI Notes Generator

Generate exam-ready study notes with AI + beautiful PDFs. For engineering students & exam prep.

**Made by Curious Arvind** ✨

---

## ⚡ Quick Start

### Setup
```bash
# Install
pip install -e .

# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# Run
streamlit run app.py
```

### How to Use
1. Enter **Subject** (e.g., "Data Structures")
2. Enter **Topic** (e.g., "Binary Search Trees")  
3. Click "Generate Notes"
4. Get PDF in `generated_notes/` folder ✅

---

## ✨ What It Does

- 🤖 **AI Notes**: Uses Google Gemini to generate structured exam notes
- 📄 **Pro PDFs**: Beautiful handwritten-style formatting
- **Every page gets**: Footer with "by curious arvind" + page number
- **Smart formatting**: Auto-bolds important points in red
- **Structured output**: Definition, Key Points, Q&A, Advantages, Applications, etc.

---

## 📁 Project Structure

```
ai-notes-generator/
├── app.py              # Main app (Streamlit)
├── modules/
│   ├── ai_generator.py       # AI note generation
│   └── pdf_generator.py      # PDF creation
├── pyproject.toml      # Dependencies
└── generated_notes/    # Output PDFs
```

---

## 🔧 What You Need

- Python 3.11+
- Google Gemini API Key (free from [here](https://aistudio.google.com/apikey))
- That's it!

---

## 📦 Dependencies

```
google-generativeai>=0.8.6
streamlit>=1.58.0
reportlab>=5.0.0
python-dotenv>=1.2.2
```

---

## 📝 What The PDF Looks Like

- **Title**: SUBJECT - TOPIC (centered, big)
- **Font**: Courier (clean, professional handwritten style)
- **Important Stuff**: Red + Bold
- **Footer**: "by curious arvind" | "page X"
- **Colors**: Black title, dark blue headings, red for important

---

## 🐛 Quick Fixes

| Problem | Solution |
|---------|----------|
| "API Key Error" | Check `.env` file has `GEMINI_API_KEY` |
| "No notes generated" | Internet working? API key valid? |
| "PDF failed" | Check folder permissions in `generated_notes/` |

---

## 📊 How Fast?

- Note Generation: ~5-15 sec
- PDF Creation: ~1-3 sec
- PDF File Size: ~50-200 KB

---

## 🎯 Perfect For

✅ Engineering exam prep  
✅ Quick study materials  
✅ Professional reference docs  
✅ Q&A compilation  

---

## License

Open source by Curious Arvind
