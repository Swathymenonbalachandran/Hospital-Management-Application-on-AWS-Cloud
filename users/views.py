import os
import random
import string
#import requests
from PIL import Image, ImageDraw, ImageFont
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import UserSignUpForm

def generate_captcha_image(text):
    # Create a blank image with white background
    width, height = 200, 50
    image = Image.new("RGB", (width, height), "white")
    # Load the default font
    font = ImageFont.load_default()
    # Create a draw object
    draw = ImageDraw.Draw(image)
    # Calculate the size of the text
    text_width, text_height = draw.textsize(text, font=font)
    # Draw the text on the image
    draw.text(((width - text_width) // 2, (height - text_height) // 2), text, font=font, fill="black")
    # Save the image to a permanent location
    image_path = os.path.join(settings.CAPTCHA_IMAGE_DIR, 'captcha.png')
    #image_path = 'captcha.png'

    image.save(image_path)
    return image_path

def sign_up(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            un = form.cleaned_data.get('username')
            messages.success(request, 'Account has been successfully created for {}!'.format(un))
            return redirect('sign_in')
    else:
        #captcha_response = requests.get('https://gbi3p3szq1.execute-api.eu-west-1.amazonaws.com/dev1/')
        #captcha_image_url = generate_captcha_image(captcha_response.text)  # Generate CAPTCHA image
        #print('captcha_image_url:',captcha_image_url)
        form = UserSignUpForm()
        
    return render(request, 'users/signup.html', {'form': form})
