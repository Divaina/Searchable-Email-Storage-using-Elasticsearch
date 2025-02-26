
# 📧 Searchable Email Storage using Elasticsearch

## 🚀 Introduction  
This project **fetches emails from an IMAP server (Gmail, Outlook, etc.), stores them in Elasticsearch, and allows full-text search and filtering**.  

### 🔹 Key Features:  
✅ Fetch emails from an IMAP server (**Inbox emails**)  
✅ Store emails in **Elasticsearch** for fast searching  
✅ Perform **full-text search** in subject & content  
✅ Filter emails by **folder & account**  
✅ Supports **bulk indexing** for better performance  

---

## 🛠️ Installation & Setup  

### 1️⃣ Install Dependencies  
Make sure you have the following installed:  
- **Python 3.8+** → [Download Python](https://www.python.org/downloads/)  
- **Elasticsearch 8.x** (without Docker) → [Download Elasticsearch](https://www.elastic.co/downloads/elasticsearch)  

Then, install Python libraries:  
```bash
pip install elasticsearch imapclient email
```

### 2️⃣ Configure Email Settings  
Edit `config.py` and update:  
```python
EMAIL_ACCOUNT = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use an App Password for security
IMAP_SERVER = "imap.gmail.com"  # Change for Outlook/Yahoo
```
📌 **Use App Passwords for Gmail/Outlook!** ([Setup Guide](https://support.google.com/accounts/answer/185833?hl=en))  

### 3️⃣ Start Elasticsearch  
- **Windows:** Run `elasticsearch.bat` from the `bin` folder  
- **Mac/Linux:** Run `./elasticsearch` from the `bin` folder  

Verify by visiting:  
```
http://localhost:9200/
```

---

## 🚀 Running the Script  
Run the script in a terminal:  
```bash
python script.py
```
It will:  
✅ **Fetch emails from IMAP**  
✅ **Store them in Elasticsearch**  
✅ **Allow searching & filtering**  

---

## 🔍 Usage  

### 1️⃣ Search Emails  
```python
search_emails("meeting")
```
🔎 **Finds emails with "meeting" in subject or content.**  

### 2️⃣ Filter Emails by Folder & Account  
```python
filter_by_folder_account("INBOX", "your_email@gmail.com")
```
📂 **Returns emails only from the "INBOX" of the given email account.**  

---

## 🛠️ Troubleshooting & FAQs  

### ❌ Elasticsearch Not Connecting?  
Run:  
```bash
curl -X GET "http://localhost:9200/"
```
If it's not running, start it manually.  

### ❌ Email Login Fails?  
✅ If using **Gmail/Outlook/Yahoo**, enable **App Passwords** ([Guide](https://support.google.com/accounts/answer/185833?hl=en)).  

### ❌ No Emails Being Fetched?  
✅ Make sure the **IMAP server details are correct**.  
✅ Try **lowering security settings** (Gmail may block IMAP by default).  

---

## 🎯 Future Enhancements  
🚀 **Web UI (Flask/React) for searching emails**  
🚀 **Advanced search (fuzzy matching, sorting)**  
🚀 **Attachment indexing (PDF, images)**  

---

## 📜 License  
This project is licensed under the **MIT License**.  

---

## 🤝 Contributing  
Pull requests are welcome! If you find a bug or have an idea, feel free to open an issue.  

💬 **Need help?** Reach out via GitHub Issues! 🚀

