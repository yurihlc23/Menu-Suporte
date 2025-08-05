@echo off
setlocal
@break off

:: Alerta inicial
cls
echo =======================================================================================
echo =======================================================================================
echo                      ***  ATENCAO - PROCEDIMENTO CRITICO  ***
echo.
echo        Este processo ira iniciar a tentativa de RECUPERACAO do banco de dados.
echo.
echo        Certifique-se de que todos os programas do Gplus estao FECHADOS em todos
echo        os computadores da loja!
echo.
echo        PARA CONTINUAR, DIGITE [1] E PRESSIONE ENTER.
echo        Para CANCELAR, feche esta janela agora.
echo =======================================================================================
echo =======================================================================================

set /p confirm="Digite 1 e pressione ENTER para continuar: "
if NOT "%confirm%"=="1" (
    echo Operacao cancelada pelo usuario.
    pause
    exit /b
)

:: Verificar se está sendo executado como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo [ERRO] Este script deve ser executado como administrador.
    pause
    exit /b
)

echo -------------------------------------------
echo Descorromper banco de dados GPLUS - INICIO
echo -------------------------------------------

:: Caminhos base do Firebird
set "FB_25=C:\Program Files\Firebird\Firebird_2_5"
set "FB_50=C:\Program Files\Firebird\Firebird_5_0"
set "FB_PATH="
set "FB_DB_PATH="

:: Detectar versão instalada e definir caminho correto
if exist "%FB_50%" (
    set "FB_PATH=%FB_50%"
    set "FB_DB_PATH=%FB_50%"
    echo Versao do Firebird detectada: 5.0
) else if exist "%FB_25%" (
    set "FB_PATH=%FB_25%"
    set "FB_DB_PATH=%FB_25%\bin"
    echo Versao do Firebird detectada: 2.5
) else (
    echo [ERRO] Nenhuma versao suportada do Firebird foi encontrada.
    pause
    exit /b
)

:: Caminhos auxiliares
set "GP_DB=C:\Gplus\DADOS\GPLUS.fdb"
set "TEMP_DB=%FB_DB_PATH%\GPLUS.fdb"
set "NEW_DB=%FB_DB_PATH%\Gplusok.fdb"
set "FINAL_DB=C:\Gplus\DADOS\GPLUS.fdb"
set "BACKUP_DB=C:\Gplus\DADOS\GPLUSOLD.fdb"

echo.
echo [1] Copiando banco GPLUS para pasta do Firebird...
copy "%GP_DB%" "%TEMP_DB%" /Y
if errorlevel 1 (
    echo [ERRO] Falha ao copiar GPLUS.fdb para %TEMP_DB%
    pause
    exit /b
)

echo.
echo [2] Executando procedimento de recuperacao (gfixed embutido)...
cd /d "%FB_DB_PATH%"

echo -------------------------------------------
echo    Executando procedimento de recuperacao
echo               de dados 
echo -------------------------------------------

del "dados.OLD" >nul 2>&1
del "dados.FBK" >nul 2>&1

echo Iniciando...
rename "GPLUS.fdb" "dados.FDB"
if errorlevel 1 (
    echo [ERRO] Nao foi possível renomear GPLUS.fdb para dados.FDB
    pause
    exit /b
)

echo O Gplus esta analisando seu Banco de Dados... 
GFIX -v -full -user SYSDBA -password masterkey "dados.FDB"

echo O Gplus vai reparar seu banco de Dados...
GFIX -rollback all -user SYSDBA -password masterkey "dados.FDB"
GFIX -mend -full -ignore -user SYSDBA -password masterkey "dados.FDB"

echo ...
pause

echo Iniciando GBAK...
GBAK -backup -v -ignore -user SYSDBA -password masterkey "dados.FDB" "dados.FBK"
REN "dados.FDB" "dados.OLD"

GBAK -create -v -user SYSDBA -password masterkey "dados.FBK" "dados.FDB"

echo -------------------------------------------
echo   Procedimento de recuperacao de dados
echo        finalizado com sucesso
echo -------------------------------------------

rename "dados.FDB" "Gplusok.fdb"

echo.
echo [3] Verificando se o arquivo Gplusok.fdb foi criado...
if exist "%NEW_DB%" (
    echo Sucesso: Gplusok.fdb encontrado.
) else (
    echo [ERRO] O arquivo Gplusok.fdb nao foi criado. Abortando...
    pause
    exit /b
)

echo.
echo [4] Copiando Gplusok.fdb de volta para a pasta DADOS...
copy "%NEW_DB%" "C:\Gplus\DADOS\Gplusok.fdb" /Y

echo.
echo [5] Parando serviço Firebird...
sc stop "FirebirdServerDefaultInstance"
timeout /t 5 >nul

echo.
echo [6] Renomeando banco antigo para GPLUSOLD...
rename "%GP_DB%" "GPLUSOLD.fdb"

echo [7] Renomeando Gplusok.fdb para GPLUS.fdb...
rename "C:\Gplus\DADOS\Gplusok.fdb" "GPLUS.fdb"

echo.
echo [8] Iniciando serviços do Gplus...
sc start "FirebirdServerDefaultInstance"
sc start "GplusAPI"
sc start "GplusEstoque"
sc start "GplusPromocao"

echo -------------------------------------------
echo Processo concluido. Banco descorrompido!
echo -------------------------------------------
pause >nul
exit
