@echo off
echo ========================================
echo GIT COMMIT E PUSH - JOE'S BURGUER
echo ========================================
echo.

cd foodmarket

echo [1/5] Verificando status do Git...
git status
echo.

echo [2/5] Adicionando todos os arquivos modificados...
git add .
echo.

echo [3/5] Criando commit...
git commit -m "Fix: Corrigido erro CSRF 403 entre login da cozinha e admin + Layout identico para ambos os logins"
echo.

echo [4/5] Enviando para o GitHub...
git push origin main
echo.

echo [5/5] Concluido!
echo.
echo ========================================
echo DEPLOY AUTOMATICO NO RENDER
echo ========================================
echo.
echo O Render detectara as mudancas automaticamente
echo e iniciara o deploy em alguns segundos.
echo.
echo Acompanhe em: https://dashboard.render.com
echo ========================================
echo.

pause
