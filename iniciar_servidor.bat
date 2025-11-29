@echo off
echo ========================================
echo    JOE'S BURGUER - PAINEL ADMIN
echo ========================================
echo.

echo [1/3] Verificando ambiente...
cd foodmarket

echo [2/3] Aplicando migracoes...
python manage.py migrate

echo [3/3] Iniciando servidor...
echo.
echo ========================================
echo   SERVIDOR INICIADO COM SUCESSO!
echo ========================================
echo.
echo   Admin Panel: http://127.0.0.1:8000/myadmin/login/
echo   Site Principal: http://127.0.0.1:8000/
echo.
echo ========================================
echo.

python manage.py runserver

pause
