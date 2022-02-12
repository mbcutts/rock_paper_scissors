# Universal Project Scaffold
A scaffold for deploying dockerized flask applications.

### File Structure
The files/directories which you will need to edit are **bolded**

**DO NOT TOUCH OTHER FILES. THIS MAY RESULT IN YOUR PROJECT BEING UNABLE TO RUN**

- .gitignore
- Dockerfile
- READMD.md
- entrypoint.sh
- nginx_host
- app/
     - **main.py**
     - **pytorch_model.bin** <- you will need to upload this yourself after cloning the repo when developing the site
     - **requirements.txt**
     - **utils.py**
     - templates/
          - **index.html**
### pytorch_model.bin ###
The weights file - must upload if you are running file on coding center or are trying to deploy.
### main.py ###
Contains the main flask app itself.
### requirements.txt ###
Contains list of packages and modules required to run the flask app. Edit only if you are using additional packages that need to be pip installed in order to run the project.

To generate a requirements.txt file you can run

`pip list --format=freeze > app/requirements.txt`

the requirements.txt file will then be updated. Keep in mind: some packages you install on one operating system may not be available on another. You will have to debug and resolve this yourself if this is the case.
### static/ ###
Contains the static images, CSS, & JS files used by the flask app for the webpage. You will need to create this and put files in it. Place all your images used for your website in static/images/ so that you can then reference them in your html files.
### utils.py ###
Contains common functions used by the flask app. Put things here that are used more than once in the flask app.
### templates/ ###
Contains the HTML pages used for the webpage. Edit these to fit your project. index.html is the demo page.
### Files used for deployment ###
`Dockerfile`
`entrypoint.sh`
`nginx_host`
**Do not touch these files.**
