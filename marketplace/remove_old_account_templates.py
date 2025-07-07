from pathlib import Path

# Arquivos de templates antigos a serem removidos
files_to_remove = [
    'edit_profile.html',
    'edit_email.html',
    'edit_phone.html',
    'change_password.html'
]

base_path = Path(__file__).parent / 'templates'
for fname in files_to_remove:
    f = base_path / fname
    if f.exists():
        f.unlink()
