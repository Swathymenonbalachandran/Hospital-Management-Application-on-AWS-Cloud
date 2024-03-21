import os
import random
import string
import requests
from PIL import Image, ImageDraw, ImageFont
from django.shortcuts import render, redirect
from django.contrib import messages
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
    # Save the image to a temporary location
    image_path = '/tmp/captcha.png'
    image.save(image_path)
    return image_path
 
def sign_up(request):
    captcha_response = requests.get('https://gbi3p3szq1.execute-api.eu-west-1.amazonaws.com/dev1/')
    #captcha_value = captcha_response.json()['body']
    print(captcha_response.text)
    captcha_value = captcha_response.json().get('body')
    print(captcha_value)
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            un = form.cleaned_data.get('username')
            messages.success(request,
                'Account has been successfully created for {}!'.format(un))
            return redirect('sign_in')
    else:  
        form = UserSignUpForm()
    captcha_image_url = generate_captcha_image(captcha_value)  # Generate CAPTCHA image
    return render(request, 'users/signup.html', {'form': form, 'captcha_image_url': captcha_image_url})
