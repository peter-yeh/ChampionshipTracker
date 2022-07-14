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
