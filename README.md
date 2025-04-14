# 🤖 Facebook Group Posting Automation Bot

This Python project automates the process of logging into Facebook accounts and posting media (images/videos) with captions in multiple Facebook groups using Selenium. It's designed to save time and streamline group content sharing across multiple accounts.

---

## 🚀 Features

- 🔐 **Multi-Account Login:** Automatically logs in using multiple Facebook credentials.
- 📢 **Group Posting:** Posts content (caption + media) to all provided Facebook group URLs.
- 🎥 **Media Support:** Supports `.jpg`, `.jpeg`, `.png`, `.mp4`, `.mov`, and `.avi` files.
- 📝 **Custom Captions:** Easily edit the caption using a simple text file.
- 🔁 **Retry Failed Posts:** Retries failed posts up to 2 times and logs them.
- 📂 **Daily Log Files:** Tracks activities and errors with daily rotating log files.

---

## 📁 Project Structure

```
project-root/
│
├── core/
│   ├── facebook_login.py
│   ├── facebook_utils.py
│   └── facebook_poster.py
│
├── data/
│   ├── credentials.txt
│   ├── groups_url.txt
│   └── post_content/
│       ├── description.txt
│       └── media/
│
├── logs/
│   └── (auto-generated log files and failed_posted.txt)
│
├── bot.py
└── README.md
```

---

## 🛠️ Requirements

- Python 3.7+
- Google Chrome browser
- ChromeDriver (matching your Chrome version)
- Selenium

### 🔧 Install Dependencies
```
pip install -r requirements.txt
```

> Make sure you have [ChromeDriver](https://sites.google.com/chromium.org/driver/) installed and added to your system's PATH.

---

## ✍️ Configuration Guide

### 1. `data/credentials.txt`

Add your Facebook accounts (one per line):

email1@example.com,password1

email2@example.com,password2

---

### 2. `data/groups_url.txt`

Add Facebook group URLs (one per line):

https://www.facebook.com/groups/group1

https://www.facebook.com/groups/group2

---

### 3. `data/post_content/description.txt`

Write the caption that will be used in your posts.

---

### 4. `data/post_content/media/`

Add images or videos you want to post. Supported formats:

```
.jpg, .jpeg, .png, .mp4, .mov, .avi
```

---

## ▶️ How to Run

```
python bot.py
```
---

## 📊 Output & Logs

- ✅ Successful posts and ❌ failed attempts are logged.
- Daily logs are saved in the `logs/` directory.
- Failed groups (after 2 retries) are recorded in `logs/failed_posted.txt`.

---

## ⚠️ Disclaimer

This project is for educational purposes only.  
**Use responsibly and at your own risk.**  
Automating interactions with Facebook may violate their terms of service.

---

## 📌 To-Do / Future Improvements

- Add GUI for easier configuration
- Support for scheduled posting
- Enhanced error handling with screenshots
- Proxy and user-agent rotation for better account safety

---

## 🙌 Contributing

Pull requests are welcome! If you'd like to contribute, open an issue or submit a PR.

---

## 📄 License

[MIT License](LICENSE)
