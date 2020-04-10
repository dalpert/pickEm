To make changes to this repository, follow these steps:
1.) Clone this repo locally:
```bash
git init
git clone https://github.com/ablassman/TownHallTrivia.git
```
	
2.) create a local working branch
```bash
git checkout -b <newBranchName>
```
  - type ```git branch``` to see a list of all the local branches you have
  
3.) Make local changes

4.) Test your changes

  1.) To run the flask app, enter the following python command in the same directory as the file ```application.py```
```python
flask run
```
  2.) Open a web browser and navigate to ```localhost:5000```
        
    - You can leave the flask app running while making a code change, just be sure to clear the cache in the web browser and reload the page and your code changes will appear.

5.) Create and push your changes to a remote branch.
```bash
git push -u origin <newBranchName>
```
6.) Let other's review your changes before merging the changes to master through the Github UI
