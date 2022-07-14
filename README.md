# Championship Tracker

## Key design conideration
- This application is developed within a week, with the main focus on code maintainability and user experience (in terms of the inputting and error)
- This is deployed on heroku https://joli-maison-71130.herokuapp.com/

## Assumptions
- The user is expected to know what they are doing, the algorithm do not enforce 2 groups of 6 team each. This would allow for flexible groups and teams should the participation rate change, allowing for the app to be reused.
- The groupings and team matchup and assumed to be well planned and correct such that all teams plays the same number of matches.

## Features
- Handle multiple line input field and throw error when the format is wrong
- Allows for inputting of team information and match result and the calculating of ranking in each groupings
- Clearing of database
- Data entered is stored in a database and persists through reboot
- App is deployed on Heroku

## Installation
| | Version |
| --- | --- |
| Python | 3.10.5 |
| NodeJs | 16.16.0 |
| NPM | 8.11.0 |

## Backend
Run on initialization
```
cd Backend
python -m venv env
source env/bin/activate # Linux
./env/Scripts/activate # For Windows
python -m pip install --upgrade pip
pip install -r requirements.txt
python init_db.py
```

To start backend
```
cd Backend
# Activate env
flask run
```

Helpful commands
```
pip install <Package Name>
pip freeze > requirements.txt
```

## Frontend
```
npm install
ng serve // Goto http://localhost:4200/
```

## Deployment
1. Create heroku instance
`heroku create`

2. Update `Frontend/env.ts` to use the new link

3. `ng build`
- Move dist/Frontend `index.html` into `/templates` and the rest into `/static`
- Rename all src and href in `index.html` to `../static`

4. Commit and push the changes to heroku
git subtree push --prefix Backend/ heroku main

5. Use dyno
heroku ps:scale web=1
