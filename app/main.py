from flask import send_from_directory
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import render_template
from url_utils import get_base_url
import os
import torch
import random #we use random to generate random numbers
import math #might not use this
import time

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12641
base_url = get_base_url(port)



# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

    
app.secret_key = os.urandom(12).hex()
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

'''
ABOVE IS NOT SUPER IMPORTANT
'''

model = torch.hub.load("ultralytics/yolov5", "custom", path = 'best.pt', force_reload=True)

def easy_mode(user_input):
    if user_input.lower() == "rock":
        return True, "Scissors"
    elif user_input.lower() == "scissors":
        return True, "Paper"
    elif user_input.lower() == "paper":
        return True, "Rock"
    else:
        return True, "I give up!"

def regular_mode(user_input):
    AI_choice=random.randint(0, 2)
    if AI_choice==0:
        AI_input="Rock"
    elif AI_choice==1:
        AI_input="Scissors"
    elif AI_choice==2:
        AI_input="Paper"

    if AI_input==user_input:
        return False, AI_input
    elif AI_input.lower()=="rock" and user_input.lower()=="paper":
        return True, AI_input
    elif AI_input.lower()=="paper" and user_input.lower()=="scissors":
        return True, AI_input
    elif AI_input.lower()=="scissors" and user_input.lower()=="rock":
        return True, AI_input
    elif AI_input.lower()=="paper" and user_input.lower()=="rock":
        return False, AI_input
    elif AI_input.lower()=="scissors" and user_input.lower()=="paper":
        return False, AI_input
    elif AI_input.lower()=="rock" and user_input.lower()=="scissors":
        return False, AI_input

    return False, AI_input

def extreme_mode(user_input):
    if user_input.lower() == "rock":
        return False, "Nuke"
    elif user_input == "scissors":
        return False, "Poison"
    elif user_input.lower() == "paper":
        return False, "Paper Shredder"
    else:
        return False, "Black Hole"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route(base_url, methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename

        selection = str(request.form['fav_language']) #easy, normal, or extreme.

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename).lower()
            if ".png" in filename:
                filename = filename[:-4] + ".jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename, selection = selection))

    return render_template('home.html')


@app.route(base_url + '/uploads/<filename>_<selection>', methods=['GET', 'POST'])
def uploaded_file(filename, selection):

    if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename

        selection = str(request.form['fav_language']) #easy, normal, or extreme.

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename).lower()
            if ".png" in filename:
                filename = filename[:-4] + ".jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename, selection = selection))

    else: 
        here = os.getcwd()
        image_path = os.path.join(here, app.config['UPLOAD_FOLDER'], filename)
        results = model(image_path, size=416)

        if len(results.pandas().xyxy) > 0:
            results.print()
            save_dir = os.path.join(here, app.config['UPLOAD_FOLDER'])
            results.save(save_dir=save_dir)

            def and_syntax(alist):
                if len(alist) == 1:
                    alist = "".join(alist)
                    return alist
                elif len(alist) == 2:
                    alist = " and ".join(alist)
                    return alist
                elif len(alist) > 2:
                    alist[-1] = "and " + alist[-1]
                    alist = ", ".join(alist)
                    return alist
                else:
                    return

            confidences = list(results.pandas().xyxy[0]['confidence'])
            # confidences: rounding and changing to percent, putting in function
            format_confidences = []
            for percent in confidences:
                format_confidences.append(str(round(percent*100)) + '%')
            format_confidences = and_syntax(format_confidences)

            labels = list(results.pandas().xyxy[0]['name'])
            # labels: sorting and capitalizing, putting into function
            labels = set(labels)
            labels = [emotion.capitalize() for emotion in labels]
            labels = and_syntax(labels)

            did_win = False
            computer_guess = "None"
            if (labels is None):
                found = False
                return render_template('results.html', labels='No Emotion', old_filename=filename, filename=filename)

            if (len(labels) > 0):
                if selection == "easy":
                    did_win, computer_guess = easy_mode(labels)
                elif selection == "normal":
                    did_win, computer_guess = regular_mode(labels)
                elif selection == "extreme":
                    did_win, computer_guess = extreme_mode(labels)

            return render_template('results.html', confidences=format_confidences, labels=labels,
                                   old_filename=filename,
                                   filename=filename, did_win = did_win, computer_guess = computer_guess, selection = selection)
        else:
            found = False
            return render_template('results.html', labels='No Emotion', old_filename=filename, filename=filename)


@app.route('/files/<path:filename>')
def files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'coding.ai-camp.dev'
    
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)
