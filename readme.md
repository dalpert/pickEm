To make changes to this repository, follow these steps:

1.) Clone this repo locally:
```bash
git init
git clone https://github.com/ablassman/TownHallTrivia.git
cd TownHallTrivia
```
	
2.) create a local working branch
```bash
git checkout -b <newBranchName>
```
  - type ```git branch``` to see a list of all the local branches you have
  
3.) Make local changes and commit them (locally)
```bash
git add <fileName>
git commit -m "<message>"
```

4.) Test your changes locally

  - To run the flask app, enter the following python command in the same directory as the file ```application.py```
```python
flask run
```
  - Open a web browser and navigate to ```localhost:5000```
        
    - You can leave the flask app running while making a code change, just be sure to clear the cache in the web browser and reload the page and your code changes will appear.
    - Enter ```ctrl + c``` to stop the flask app.

5.) Create and push your changes to a remote branch.
```bash
git push -u origin <newBranchName>
```

6.) Go to this branch in the GitHub UI and create a pull request.

  - To complete your PR, you will need at least one person's approval.
  - Completing the PR will deploy these changes to the website.
