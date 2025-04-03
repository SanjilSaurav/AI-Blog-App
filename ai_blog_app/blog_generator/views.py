from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import os
import requests
from dotenv import load_dotenv
import assemblyai as aai
import yt_dlp
from openai import OpenAI

load_dotenv("./.env")

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
        
        # get yt title
        # title = yt_title(yt_link)

        # get transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error':"Failed to get transcript"}, status=500)
        # use openAi to generate the blog
        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error':"Failed to generate blog article."}, status=500)

        #save blog article to database

        # return blog article as a response
        return JsonResponse({'content': blog_content})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# def yt_title(link):
#     yt = YouTube(link)
#     title = yt.title
#     return title

def download_audio(link):
    output_dir = "media"  # Folder where files will be saved
    os.makedirs(output_dir, exist_ok=True)  # Create folder if it doesn't exist

    ydl_opts = {
        'format': 'bestaudio/best',  # Get the best available audio format
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s'  # Save as "downloads/VideoTitle.[ext]"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)  # Download and extract info
        file_path = ydl.prepare_filename(info_dict)  # Get the filename

    return file_path  # Return the downloaded file path

# Function to get transcription using AssemblyAI
def get_transcription(link):
    audio_file = download_audio(link)  # Download audio in original format

    # Set AssemblyAI API key
    aai.settings.api_key = os.getenv("AAI_API_KEY")

    transcriber = aai.Transcriber()  # Initialize transcriber
    transcript = transcriber.transcribe(audio_file)  # Transcribe audio
    return transcript.text  # Return transcription text

def generate_blog_from_transcription(transcription):
    token = os.getenv("GITHUB_TOKEN")
    base_url = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o"

    client = OpenAI(
        base_url=base_url,
        api_key=token,
    )

    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )
    generated_content = response.choices[0].message.content
    return generated_content

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatPassword']

        if password == repeatpassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Errror creating account'
                return render(request, 'signup.html', {'error_message': error_message})

        else:
            error_message = 'Password do no match'
            return render(request, 'signup.html', {'error_message': error_message})
        
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')