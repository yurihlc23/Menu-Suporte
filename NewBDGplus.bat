@echo off
setlocal enabledelayedexpansion
title Backup e Restauracao do Banco GPLUS

echo.
echo ===================================================
echo    BACKUP E RESTAURACAO DO BANCO DE DADOS GPLUS
echo ===================================================
echo.

:: === CONFIRMAÇÃO DO USUÁRIO ===
set /p CONFIRM="Deseja iniciar o processo de restauracao do banco de dados? (S/N): "
if /i not "!CONFIRM!"=="S" (
    echo Operacao cancelada pelo usuário.
    pause
    exit /b
)

:: === CONFIGURAÇÕES DO USUÁRIO ===
set "USER=SYSDBA"
set "PASS=masterkey"

:: === CAMINHOS DO BANCO DE DADOS ===
set "OLD_DB=C:\Gplus\DADOS\gplus.fdb"
set "BACKUP=C:\Gplus\BACKUP\gplus.fbk"
set "NEW_DB=C:\Gplus\DADOS\gplus_novo.fdb"
set "OLD_RENAME=C:\Gplus\DADOS\gplus_antigo.fdb"

:: === CRIAR PASTA DE BACKUP SE NÃO EXISTIR ===
if not exist "C:\Gplus\BACKUP" (
    echo Criando a pasta de backup: C:\Gplus\BACKUP
    mkdir "C:\Gplus\BACKUP"
)

:: === DETECTAR VERSÃO DO FIREBIRD EM EXECUÇÃO ===
echo.
echo Detectando versao do Firebird em execucao...

:: Tenta localizar o caminho do executável fbserver.exe ou firebird.exe
for /f "tokens=2,* delims=\ " %%A in ('tasklist /FI "IMAGENAME eq fbserver.exe" /FO LIST ^| findstr /I "fbserver.exe"') do (
    set "FB_PROC=%%A\%%B"
)
for /f "tokens=2,* delims=\ " %%A in ('tasklist /FI "IMAGENAME eq firebird.exe" /FO LIST ^| findstr /I "firebird.exe"') do (
    set "FB_PROC=%%A\%%B"
)

:: Caso não tenha encontrado processo
if not defined FB_PROC (
    echo [ERRO] Nenhuma instância do Firebird foi encontrada em execucao.
    pause
    exit /b
)

:: Deduzir o caminho do gbak.exe
set "GBAK_PATH="
if exist "C:\Program Files\Firebird\Firebird_2_5\bin\gbak.exe" (
    set "GBAK_PATH=C:\Program Files\Firebird\Firebird_2_5\bin\gbak.exe"
)
if exist "C:\Program Files\Firebird\Firebird_5_0\gbak.exe" (
    set "GBAK_PATH=C:\Program Files\Firebird\Firebird_5_0\gbak.exe"
)

:: Validação
if not defined GBAK_PATH (
    echo.
    echo [ERRO] gbak.exe nao encontrado nas pastas padrao.
    echo Certifique-se de que Firebird 2.5 ou 5.0 está instalado corretamente.
    pause
    exit /b
)

echo Firebird detectado em: !FB_PROC!
echo gbak encontrado em: %GBAK_PATH%

:: === FAZER BACKUP ===
echo.
echo ----------------------------------------------
echo [1/4] Fazendo backup do banco antigo...
echo ----------------------------------------------
"%GBAK_PATH%" -b -v -user %USER% -password %PASS% "%OLD_DB%" "%BACKUP%"
if errorlevel 1 (
    echo [ERRO] Falha ao fazer backup. Verifique o caminho e permissões.
    pause
    exit /b
)

:: === RESTAURAR NOVO BANCO ===
echo.
echo ----------------------------------------------
echo [2/4] Restaurando para o novo banco...
echo ----------------------------------------------
"%GBAK_PATH%" -c -v -user %USER% -password %PASS% "%BACKUP%" "%NEW_DB%"
if errorlevel 1 (
    echo [ERRO] Falha ao restaurar banco. Verifique o backup.
    pause
    exit /b
)

:: === RENOMEAR BANCO ANTIGO ===
echo.
echo ----------------------------------------------
echo [3/4] Renomeando banco antigo...
echo ----------------------------------------------
if exist "%OLD_RENAME%" (
    echo Apagando versao anterior de %OLD_RENAME%
    del /f /q "%OLD_RENAME%"
)
ren "%OLD_DB%" "gplus_antigo.fdb"

:: === MOVER NOVO BANCO PARA O LUGAR DO ANTIGO COM NOME MAIÚSCULO ===
echo.
echo ----------------------------------------------
echo [4/4] Substituindo banco antigo pelo novo (com nome em maiúsculo)...
echo ----------------------------------------------
move /Y "%NEW_DB%" "C:\Gplus\DADOS\TEMP_RENAME.FDB"
rename "C:\Gplus\DADOS\TEMP_RENAME.FDB" "GPLUS.FDB"

:: === FINAL ===
echo.
echo ==================================================
echo Processo concluido com sucesso!
echo Banco antigo renomeado para: %OLD_RENAME%
echo Banco novo movido para: %OLD_DB%
echo ==================================================
pause
