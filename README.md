
# 🧠 AI Blog App

The **AI Blog App** is a Django-based web application that takes a **YouTube video link** as input and uses AI (OpenAI's GPT) to generate a blog post based on the video's content. It extracts the video transcript and crafts a well-structured article automatically.

## 🚀 Features

- Paste a YouTube link and get a blog in seconds
- Automatically fetches the transcript using `AssemblyAI-api`
- Generates unique, AI-written content using OpenAI's GPT models
- Simple UI built with Django templates
- Environment-based API key handling with `.env`

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, Django Templates
- **AI**: OpenAI GPT
- **Transcript Extraction**: AssemblyAI-api
- **Env Handling**: python-dotenv

## 📁 Project Structure

```
ai_blog_app/
├── ai_blog_app/          # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── blog/                 # Core app for blog generation
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   └── templates/
│       └── index.html
├── manage.py
├── .env                  # Stores OpenAI API key (not committed)
├── .gitignore
└── README.md
```

## 🧪 Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/SanjilSaurav/AI-Blog-App.git
cd AI-Blog-App
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add your OpenAI API key**

Create a `.env` file in the root folder:
```
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Run the development server**
```bash
python manage.py runserver
```

6. **Visit the application**

Open your browser and go to:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📌 How It Works

1. User inputs a YouTube video link.
2. The app fetches the transcript using `AssemblyAI-api`.
3. The transcript is passed to OpenAI's GPT model.
4. A blog post is generated and displayed on the page.

## ✅ Example

- **Input**: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- **Output**: A well-structured blog post based on the video's transcript.

---

Made with ❤️ by [Saurav Kumar](https://github.com/SanjilSaurav)
