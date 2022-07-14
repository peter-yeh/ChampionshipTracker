# Championship Tracker

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
```
heroku create # Create a new heroku
# Add database.db into git
# Update Frontend/env.ts with the new link
# ng build
# Move dist/frontend content index.html into /templates and the rest into static folder
# Rename all src and href in index.html to ../static/
git subtree push --prefix Backend/ heroku main
heroku ps:scale web=1
```
