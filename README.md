# Joe's Burguer

Local development and notes.

## How to run locally

- Create and activate a virtual environment and install dependencies from `requirements.txt`.
- Run `python manage.py migrate` and `python manage.py runserver`.

## Deploy to Render (helper script)

There is a helper PowerShell script at `scripts/deploy_render.ps1` that automates common local steps and pushes to your git remote. It will:

- run `makemigrations`, `migrate`, and `collectstatic`;
- stage and commit migration/static changes if any;
- push to `origin/<branch>` (default branch is `main`).

Usage (PowerShell):

```powershell
.\scripts\deploy_render.ps1 -Branch main
```

After the push, if your GitHub repo is connected to Render, Render will automatically start a build and deploy.

Note: make sure you have `origin` set and authentication configured (SSH key or credential helper) before running the script.
