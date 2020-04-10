To make changes to this repository, follow these steps:

1.) Clone this repo locally:
```bash
git init
git clone https://github.com/ablassman/TownHallTrivia.git
cd TownHallTrivia
```

2.) Create a virtual environment and install the necessary dependencies from ```requirements.txt```.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=application.py
```
	
3.) Create a local working branch
```bash
git checkout -b <newBranchName>
```
  - type ```git branch``` to see a list of all the local branches you have
  
4.) Make local changes and commit them (locally)
```bash
git add <fileName>
git commit -m "<message>"
```
  - If you add any new dependencies (aka you have to run ```pip install``` at some point to get something working), please be sure to add them to ```requirments.txt```. This is because the Azure App Service creates a virtual environment with all dependencies listed in ```requirments.txt``` before deploying our code.
  
    - To write all dependencies in your virtual environment to ```requirements.txt```, run the following command:
```bash
pip freeze > requirements.txt
```

5.) Test your changes locally

  - To run the flask app, enter the following python command in the same directory as the file ```application.py```
```python
flask run
```
  - Open a web browser and navigate to ```localhost:5000```
        
    - You can leave the flask app running while making a code change, just be sure to clear the cache in the web browser and reload the page and your code changes will appear.
    - Enter ```ctrl + c``` to stop the flask app.

6.) Create and push your changes to a remote branch.
```bash
git push -u origin <newBranchName>
```

7.) Go to ```https://github.com/ablassman/TownHallTrivia``` and use the GUI to create a pull request with the remote branch that you created in step 6.

  - To complete your PR, you will need at least one person's approval.
  - Completing the PR will automatically deploy your changes to the website.
  
8.) Go checkout www.TownHallTrivia.com to see the final product!
