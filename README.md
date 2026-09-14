```bat
@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ============================================================
REM Tomcat9 Maintenance Batch
REM
REM Exit Code
REM   0  : Success
REM   10 : Tomcat service not found
REM   11 : TOMCAT_BASE not found
REM   12 : Tomcat log directory not found
REM   13 : Hi-Surf3 log directory not found
REM   14 : PowerShell not found
REM   15 : robocopy not found
REM   16 : Maintenance log directory write error
REM   20 : Tomcat stop timeout
REM   21 : Tomcat log archive failed
REM   22 : Hi-Surf3 log archive failed
REM   30 : Tomcat start request failed
REM   31 : Tomcat start timeout
REM   50 : Another maintenance process is running
REM ============================================================


REM ============================================================
REM 1. Settings
REM ============================================================

set "SERVICE_NAME=Tomcat9"

set "TOMCAT_BASE=C:\apache-tomcat-9"

set "HISURF3_LOG_DIR=%TOMCAT_BASE%\Hi-Surf3\logs"

set "MAINTENANCE_DIR=C:\tomcat-maintenance"

set "LOG_DIR=%MAINTENANCE_DIR%\logs"

set "ARCHIVE_DIR=%MAINTENANCE_DIR%\archive"

set "LOCK_DIR=%MAINTENANCE_DIR%\tomcat9_maintenance.lock"


REM ------------------------------------------------------------
REM 停止・起動確認
REM 5秒 × 60回 = 最大5分
REM ------------------------------------------------------------

set "CHECK_INTERVAL=5"
set "STOP_MAX_RETRY=60"
set "START_MAX_RETRY=60"


REM ------------------------------------------------------------
REM ログ保持期間
REM ------------------------------------------------------------

set "RETENTION_DAYS=30"

set "EXIT_CODE=0"
set "LOCK_CREATED=0"


REM ============================================================
REM 2. Maintenance directories
REM ============================================================

if not exist "%MAINTENANCE_DIR%" (
    mkdir "%MAINTENANCE_DIR%" >nul 2>&1
)

if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%" >nul 2>&1
)

if not exist "%ARCHIVE_DIR%" (
    mkdir "%ARCHIVE_DIR%" >nul 2>&1
)

if not exist "%LOG_DIR%" (
    echo ERROR: Cannot create maintenance log directory.
    exit /b 16
)


REM ============================================================
REM 3. PowerShell check
REM ============================================================

where powershell.exe >nul 2>&1

if errorlevel 1 (
    echo ERROR: powershell.exe not found.
    exit /b 14
)


REM ============================================================
REM 4. Generate execution timestamp
REM ============================================================

set "RUN_TS="

for /f %%A in (
    'powershell.exe -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"'
) do (
    set "RUN_TS=%%A"
)

if not defined RUN_TS (
    echo ERROR: Could not generate timestamp.
    exit /b 14
)

set "SCRIPT_LOG=%LOG_DIR%\tomcat9_maintenance_%RUN_TS%.log"

set "RUN_ARCHIVE_DIR=%ARCHIVE_DIR%\%RUN_TS%"
set "TOMCAT_ARCHIVE_DIR=%RUN_ARCHIVE_DIR%\tomcat"
set "HISURF_ARCHIVE_DIR=%RUN_ARCHIVE_DIR%\hisurf3"


REM ============================================================
REM 5. Log write check
REM ============================================================

set "WRITE_TEST=%LOG_DIR%\.__write_test_%RUN_TS%.tmp"

echo test>"%WRITE_TEST%" 2>nul

if not exist "%WRITE_TEST%" (
    echo ERROR: Cannot write to maintenance log directory.
    exit /b 16
)

del /F /Q "%WRITE_TEST%" >nul 2>&1


REM ============================================================
REM 6. Multiple execution protection
REM ============================================================

mkdir "%LOCK_DIR%" >nul 2>&1

if errorlevel 1 (
    call :LOG "ERROR: Another maintenance process is already running."
    exit /b 50
)

set "LOCK_CREATED=1"


call :LOG "============================================================"
call :LOG "Tomcat9 maintenance START"
call :LOG "Run ID       : %RUN_TS%"
call :LOG "Service      : %SERVICE_NAME%"
call :LOG "Tomcat Base  : %TOMCAT_BASE%"
call :LOG "Hi-Surf3 Log : %HISURF3_LOG_DIR%"
call :LOG "============================================================"


REM ============================================================
REM 7. PRECHECK
REM ============================================================

call :LOG "Starting PRECHECK."


sc query "%SERVICE_NAME%" >nul 2>&1

if errorlevel 1 (
    call :LOG "ERROR: Service does not exist: %SERVICE_NAME%"
    set "EXIT_CODE=10"
    goto FINALIZE
)


if not exist "%TOMCAT_BASE%\" (
    call :LOG "ERROR: TOMCAT_BASE does not exist: %TOMCAT_BASE%"
    set "EXIT_CODE=11"
    goto FINALIZE
)


if not exist "%TOMCAT_BASE%\logs\" (
    call :LOG "ERROR: Tomcat log directory does not exist."
    set "EXIT_CODE=12"
    goto FINALIZE
)


if not exist "%HISURF3_LOG_DIR%\" (
    call :LOG "ERROR: Hi-Surf3 log directory does not exist."
    set "EXIT_CODE=13"
    goto FINALIZE
)


where robocopy.exe >nul 2>&1

if errorlevel 1 (
    call :LOG "ERROR: robocopy.exe not found."
    set "EXIT_CODE=15"
    goto FINALIZE
)


call :LOG "PRECHECK completed successfully."


REM ============================================================
REM 8. Tomcat STOP
REM ============================================================

call :LOG "Checking current Tomcat service state."

call :CHECK_STOPPED

if not errorlevel 1 (
    call :LOG "%SERVICE_NAME% is already completely stopped."
    goto TOMCAT_STOPPED
)


call :LOG "Sending STOP request to %SERVICE_NAME%."

sc stop "%SERVICE_NAME%" >> "%SCRIPT_LOG%" 2>&1


REM ============================================================
REM 9. Wait for complete STOP
REM ============================================================

set "COUNT=0"

:WAIT_STOP

call :CHECK_STOPPED

if not errorlevel 1 (
    goto TOMCAT_STOPPED
)

set /a COUNT+=1

if !COUNT! GEQ %STOP_MAX_RETRY% (
    call :LOG "ERROR: Tomcat did not stop completely within timeout."
    set "EXIT_CODE=20"
    goto FINALIZE
)

call :LOG "Waiting for complete stop... (!COUNT!/%STOP_MAX_RETRY%)"

timeout /t %CHECK_INTERVAL% /nobreak >nul

goto WAIT_STOP


:TOMCAT_STOPPED

call :LOG "%SERVICE_NAME% completely stopped. STATE=STOPPED / PID=0"


REM ============================================================
REM 10. Create archive directories
REM ============================================================

mkdir "%TOMCAT_ARCHIVE_DIR%" >nul 2>&1
mkdir "%HISURF_ARCHIVE_DIR%" >nul 2>&1

if not exist "%TOMCAT_ARCHIVE_DIR%\" (
    call :LOG "ERROR: Could not create Tomcat archive directory."
    set "EXIT_CODE=21"
    goto START_RECOVERY
)

if not exist "%HISURF_ARCHIVE_DIR%\" (
    call :LOG "ERROR: Could not create Hi-Surf3 archive directory."
    set "EXIT_CODE=22"
    goto START_RECOVERY
)


REM ============================================================
REM 11. Archive Tomcat logs
REM ============================================================

call :LOG "Archiving Tomcat logs."

robocopy "%TOMCAT_BASE%\logs" "%TOMCAT_ARCHIVE_DIR%" ^
    /E /COPY:DAT /DCOPY:T /R:1 /W:1 /NP ^
    >> "%SCRIPT_LOG%" 2>&1

set "ROBOCOPY_RC=!ERRORLEVEL!"

if !ROBOCOPY_RC! GEQ 8 (
    call :LOG "ERROR: Tomcat log archive failed. robocopy RC=!ROBOCOPY_RC!"
    set "EXIT_CODE=21"
    goto START_RECOVERY
)

call :LOG "Tomcat logs archived successfully."


REM ============================================================
REM 12. Delete original Tomcat log contents
REM ============================================================

call :DELETE_DIRECTORY_CONTENTS "%TOMCAT_BASE%\logs"

if errorlevel 1 (
    call :LOG "ERROR: Some Tomcat log files could not be deleted."
    set "EXIT_CODE=21"
    goto START_RECOVERY
)

call :LOG "Original Tomcat log contents deleted."


REM ============================================================
REM 13. Archive Hi-Surf3 logs
REM ============================================================

call :LOG "Archiving Hi-Surf3 logs."

robocopy "%HISURF3_LOG_DIR%" "%HISURF_ARCHIVE_DIR%" ^
    /E /COPY:DAT /DCOPY:T /R:1 /W:1 /NP ^
    >> "%SCRIPT_LOG%" 2>&1

set "ROBOCOPY_RC=!ERRORLEVEL!"

if !ROBOCOPY_RC! GEQ 8 (
    call :LOG "ERROR: Hi-Surf3 log archive failed. robocopy RC=!ROBOCOPY_RC!"
    set "EXIT_CODE=22"
    goto START_RECOVERY
)

call :LOG "Hi-Surf3 logs archived successfully."


REM ============================================================
REM 14. Delete original Hi-Surf3 log contents
REM ============================================================

call :DELETE_DIRECTORY_CONTENTS "%HISURF3_LOG_DIR%"

if errorlevel 1 (
    call :LOG "ERROR: Some Hi-Surf3 log files could not be deleted."
    set "EXIT_CODE=22"
    goto START_RECOVERY
)

call :LOG "Original Hi-Surf3 log contents deleted."


REM ============================================================
REM 15. Tomcat START
REM ============================================================

:START_RECOVERY

call :LOG "Sending START request to %SERVICE_NAME%."

sc start "%SERVICE_NAME%" >> "%SCRIPT_LOG%" 2>&1

set "START_RC=!ERRORLEVEL!"

if not "!START_RC!"=="0" (

    call :CHECK_RUNNING

    if errorlevel 1 (
        call :LOG "ERROR: Tomcat START request failed. RC=!START_RC!"

        if "!EXIT_CODE!"=="0" (
            set "EXIT_CODE=30"
        )

        goto FINALIZE
    )
)


REM ============================================================
REM 16. Wait for RUNNING
REM ============================================================

set "COUNT=0"

:WAIT_START

call :CHECK_RUNNING

if not errorlevel 1 (
    goto TOMCAT_RUNNING
)

set /a COUNT+=1

if !COUNT! GEQ %START_MAX_RETRY% (
    call :LOG "ERROR: Tomcat did not become RUNNING within timeout."

    if "!EXIT_CODE!"=="0" (
        set "EXIT_CODE=31"
    )

    goto FINALIZE
)

call :LOG "Waiting for Tomcat startup... (!COUNT!/%START_MAX_RETRY%)"

timeout /t %CHECK_INTERVAL% /nobreak >nul

goto WAIT_START


:TOMCAT_RUNNING

call :LOG "%SERVICE_NAME% is RUNNING."


REM ============================================================
REM 17. Delete old maintenance logs
REM ============================================================

call :LOG "Deleting maintenance logs older than %RETENTION_DAYS% days."

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
"$limit=(Get-Date).AddDays(-%RETENTION_DAYS%);" ^
"Get-ChildItem -LiteralPath '%LOG_DIR%' -Filter 'tomcat9_maintenance_*.log' -File -ErrorAction SilentlyContinue |" ^
"Where-Object { $_.LastWriteTime -lt $limit -and $_.FullName -ne '%SCRIPT_LOG%' } |" ^
"Remove-Item -Force -ErrorAction SilentlyContinue;" ^
>> "%SCRIPT_LOG%" 2>&1


REM ============================================================
REM 18. Delete old archive directories
REM ============================================================

call :LOG "Deleting archives older than %RETENTION_DAYS% days."

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
"$limit=(Get-Date).AddDays(-%RETENTION_DAYS%);" ^
"Get-ChildItem -LiteralPath '%ARCHIVE_DIR%' -Directory -ErrorAction SilentlyContinue |" ^
"Where-Object { $_.LastWriteTime -lt $limit } |" ^
"Remove-Item -Recurse -Force -ErrorAction SilentlyContinue;" ^
>> "%SCRIPT_LOG%" 2>&1


REM ============================================================
REM 19. Normal completion
REM ============================================================

if "%EXIT_CODE%"=="0" (
    call :LOG "============================================================"
    call :LOG "Tomcat9 maintenance completed SUCCESSFULLY."
    call :LOG "============================================================"
)


REM ============================================================
REM 20. Finalize
REM ============================================================

:FINALIZE

if not "%EXIT_CODE%"=="0" (
    call :LOG "============================================================"
    call :LOG "Tomcat9 maintenance FAILED."
    call :LOG "Exit Code: %EXIT_CODE%"
    call :LOG "============================================================"
)


if "%LOCK_CREATED%"=="1" (
    rmdir "%LOCK_DIR%" >nul 2>&1
)

exit /b %EXIT_CODE%


REM ============================================================
REM Check complete STOP
REM ============================================================

:CHECK_STOPPED

set "SERVICE_PID="

sc queryex "%SERVICE_NAME%" ^
    | findstr /R /C:"STATE *: *1 *STOPPED" >nul

if errorlevel 1 (
    exit /b 1
)

for /f "tokens=3" %%A in (
    'sc queryex "%SERVICE_NAME%" ^| findstr /R /C:"PID *:"'
) do (
    set "SERVICE_PID=%%A"
)

if not defined SERVICE_PID (
    exit /b 1
)

if not "!SERVICE_PID!"=="0" (
    exit /b 1
)

exit /b 0


REM ============================================================
REM Check RUNNING
REM ============================================================

:CHECK_RUNNING

sc query "%SERVICE_NAME%" ^
    | findstr /R /C:"STATE *: *4 *RUNNING" >nul

if errorlevel 1 (
    exit /b 1
)

exit /b 0


REM ============================================================
REM Delete directory contents
REM ============================================================

:DELETE_DIRECTORY_CONTENTS

set "TARGET_DIR=%~1"

del /F /Q /A "%TARGET_DIR%\*" >nul 2>&1

for /D %%D in ("%TARGET_DIR%\*") do (
    rd /S /Q "%%~fD" >nul 2>&1
)

dir /A /B "%TARGET_DIR%" 2>nul | findstr "." >nul

if not errorlevel 1 (
    exit /b 1
)

exit /b 0


REM ============================================================
REM Logging
REM ============================================================

:LOG

echo [%date% %time%] %~1
echo [%date% %time%] %~1 >> "%SCRIPT_LOG%"

exit /b 0
```

```bat
@echo off
setlocal EnableDelayedExpansion

REM ============================================================
REM Tomcat9 Restart + Log Cleanup + HTTP Health Check
REM ============================================================


REM ============================================================
REM Settings
REM ============================================================

REM Tomcat9 サービス名
set "SERVICE_NAME=Tomcat9"

REM Tomcat9 インストール先
set "TOMCAT_BASE=C:\apache-tomcat-9"

REM ハイサーフ3 ログフォルダ
REM ★ 実際の環境に合わせて変更してください
set "HISURF3_LOG_DIR=C:\Hi-Surf3\logs"

REM メンテナンスBAT自身のログ
REM Tomcat9 logs配下には置かない
set "MAINTENANCE_DIR=C:\tomcat-maintenance"
set "SCRIPT_LOG=%MAINTENANCE_DIR%\tomcat9_restart.log"

REM HTTPヘルスチェックURL
REM ★ 実際のアプリURLに変更してください
set "HEALTH_URL=http://127.0.0.1:8080/myapp/health"

REM Tomcat停止・起動確認
REM 5秒 × 60回 = 最大300秒
set "MAX_RETRY=60"

REM HTTP疎通確認
REM 5秒 × 24回 = 最大120秒
set "HEALTH_MAX_RETRY=24"


REM ============================================================
REM メンテナンスログフォルダ作成
REM ============================================================

if not exist "%MAINTENANCE_DIR%" (
    mkdir "%MAINTENANCE_DIR%"
)

call :LOG "========================================"
call :LOG "Tomcat9 maintenance start"
call :LOG "========================================"


REM ============================================================
REM 1. Tomcat9 停止
REM ============================================================

call :LOG "Stopping %SERVICE_NAME%..."

REM すでにSTOPPEDなら停止処理をスキップ
sc query "%SERVICE_NAME%" | findstr /R /C:"STATE.*STOPPED" >nul

if not errorlevel 1 (
    call :LOG "%SERVICE_NAME% is already stopped."
    goto CHECK_STOPPED
)

net stop "%SERVICE_NAME%" >> "%SCRIPT_LOG%" 2>&1

call :LOG "Stop command issued."


REM ============================================================
REM 2. Tomcat9 完全停止確認
REM    ・STATE = STOPPED
REM    ・PID = 0
REM ============================================================

:CHECK_STOPPED

set "COUNT=0"

:WAIT_STOP

REM ------------------------------------------------------------
REM サービス状態確認
REM ------------------------------------------------------------

sc query "%SERVICE_NAME%" | findstr /R /C:"STATE.*STOPPED" >nul

if errorlevel 1 (
    goto STILL_STOPPING
)


REM ------------------------------------------------------------
REM PID確認
REM ------------------------------------------------------------

set "SERVICE_PID="

for /f "tokens=3" %%A in ('sc queryex "%SERVICE_NAME%" ^| findstr /C:"PID"') do (
    set "SERVICE_PID=%%A"
)

if not defined SERVICE_PID (
    call :LOG "WARNING: Could not get service PID."
    goto STILL_STOPPING
)

if not "!SERVICE_PID!"=="0" (
    call :LOG "%SERVICE_NAME% is STOPPED but PID is still !SERVICE_PID!."
    goto STILL_STOPPING
)

goto STOP_OK


:STILL_STOPPING

set /a COUNT+=1

if !COUNT! GEQ %MAX_RETRY% (
    call :LOG "ERROR: %SERVICE_NAME% did not stop completely."
    goto ERROR_END
)

call :LOG "Waiting for %SERVICE_NAME% to stop... (!COUNT!/%MAX_RETRY%)"

timeout /t 5 /nobreak >nul

goto WAIT_STOP


:STOP_OK

call :LOG "%SERVICE_NAME% stopped completely. STATE=STOPPED PID=0"


REM ============================================================
REM 3. Tomcat9 ログ削除
REM ============================================================

call :LOG "Deleting Tomcat9 logs..."

if exist "%TOMCAT_BASE%\logs" (

    del /F /Q "%TOMCAT_BASE%\logs\*" >> "%SCRIPT_LOG%" 2>&1

    if errorlevel 1 (
        call :LOG "WARNING: Some Tomcat9 log files could not be deleted."
    ) else (
        call :LOG "Tomcat9 logs deleted successfully."
    )

) else (

    call :LOG "WARNING: Tomcat9 logs directory does not exist: %TOMCAT_BASE%\logs"

)


REM ============================================================
REM 4. ハイサーフ3 ログ削除
REM ============================================================

call :LOG "Deleting Hi-Surf3 logs..."

if exist "%HISURF3_LOG_DIR%" (

    del /F /Q "%HISURF3_LOG_DIR%\*" >> "%SCRIPT_LOG%" 2>&1

    if errorlevel 1 (
        call :LOG "WARNING: Some Hi-Surf3 log files could not be deleted."
    ) else (
        call :LOG "Hi-Surf3 logs deleted successfully."
    )

) else (

    call :LOG "WARNING: Hi-Surf3 logs directory does not exist: %HISURF3_LOG_DIR%"

)


REM ============================================================
REM 5. Tomcat9 起動
REM ============================================================

call :LOG "Starting %SERVICE_NAME%..."

net start "%SERVICE_NAME%" >> "%SCRIPT_LOG%" 2>&1

if errorlevel 1 (
    call :LOG "WARNING: net start returned an error. Checking service state..."
)


REM ============================================================
REM 6. Tomcat9 RUNNING確認
REM ============================================================

set "COUNT=0"

:WAIT_START

sc query "%SERVICE_NAME%" | findstr /R /C:"STATE.*RUNNING" >nul

if not errorlevel 1 (
    goto START_OK
)

set /a COUNT+=1

if !COUNT! GEQ %MAX_RETRY% (
    call :LOG "ERROR: %SERVICE_NAME% did not become RUNNING."
    goto ERROR_END
)

call :LOG "Waiting for %SERVICE_NAME% to start... (!COUNT!/%MAX_RETRY%)"

timeout /t 5 /nobreak >nul

goto WAIT_START


:START_OK

call :LOG "%SERVICE_NAME% is RUNNING."


REM ============================================================
REM 7. HTTP 疎通確認
REM ============================================================

call :LOG "Starting HTTP health check."
call :LOG "Health URL: %HEALTH_URL%"

set "COUNT=0"

:WAIT_HTTP

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
    "try { $r = Invoke-WebRequest -Uri '%HEALTH_URL%' -UseBasicParsing -TimeoutSec 10; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"

if not errorlevel 1 (
    goto HTTP_OK
)

set /a COUNT+=1

if !COUNT! GEQ %HEALTH_MAX_RETRY% (
    call :LOG "ERROR: HTTP health check failed."
    call :LOG "URL: %HEALTH_URL%"
    goto ERROR_END
)

call :LOG "Waiting for HTTP 200... (!COUNT!/%HEALTH_MAX_RETRY%)"

timeout /t 5 /nobreak >nul

goto WAIT_HTTP


:HTTP_OK

call :LOG "HTTP health check successful. HTTP 200 received."


REM ============================================================
REM 8. 正常終了
REM ============================================================

call :LOG "========================================"
call :LOG "Tomcat9 maintenance completed successfully."
call :LOG "========================================"

exit /b 0


REM ============================================================
REM 異常終了
REM ============================================================

:ERROR_END

call :LOG "========================================"
call :LOG "Tomcat9 maintenance FAILED."
call :LOG "========================================"

exit /b 1


REM ============================================================
REM ログ出力
REM ============================================================

:LOG

echo [%date% %time%] %~1
echo [%date% %time%] %~1 >> "%SCRIPT_LOG%"

exit /b
```













## UTF-8 → Shift-JIS 変換BAT

## 処理内容

このBATは、`input` フォルダ内のファイルを読み込み、  
UTF-8 から Shift-JIS に変換して `output` フォルダへ出力します。

出力ファイル名は、入力ファイル名と同じです。

変換後、元ファイルは以下のフォルダへ移動します。

```text
backup/yyyyMMdd/
```

`input` フォルダ自体は削除しません。  
処理後、`input` フォルダの中は空になります。

---

## フォルダ構成

```text
convert_tool/
├─ convert.bat
├─ convert.ps1
├─ template/
│  └─ blank_sjis.txt
├─ input/
│  └─ 変換したいファイル.csv
├─ output/
└─ backup/
```

---

## convert.bat

```bat
@echo off
setlocal

cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0convert.ps1"

pause
endlocal
```

---

## convert.ps1

```powershell
$ErrorActionPreference = "Stop"

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$inputDir  = Join-Path $baseDir "input"
$outputDir = Join-Path $baseDir "output"
$backupRootDir = Join-Path $baseDir "backup"
$templateFile = Join-Path $baseDir "template\blank_sjis.txt"

$today = Get-Date -Format "yyyyMMdd"
$backupDir = Join-Path $backupRootDir $today

# Shift-JIS
$sjis = [System.Text.Encoding]::GetEncoding(932)

if (!(Test-Path $inputDir)) {
    Write-Host "input フォルダが存在しません。"
    exit 1
}

if (!(Test-Path $templateFile)) {
    Write-Host "テンプレートファイルが存在しません: $templateFile"
    exit 1
}

New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$files = Get-ChildItem -Path $inputDir -File

if ($files.Count -eq 0) {
    Write-Host "input フォルダにファイルがありません。"
    exit 0
}

foreach ($file in $files) {

    $outputFile = Join-Path $outputDir $file.Name

    # テンプレートをコピーして出力ファイルを作成
    Copy-Item -Path $templateFile -Destination $outputFile -Force

    # UTF-8として読み込み
    $text = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)

    # BOMがある場合は削除
    $text = $text.TrimStart([char]0xFEFF)

    # Shift-JISで書き込み
    [System.IO.File]::WriteAllText($outputFile, $text, $sjis)

    # backup/yyyyMMdd に元ファイルを移動
    $backupFile = Join-Path $backupDir $file.Name

    if (Test-Path $backupFile) {
        $timestamp = Get-Date -Format "HHmmssfff"
        $name = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
        $ext  = [System.IO.Path]::GetExtension($file.Name)
        $backupFile = Join-Path $backupDir "${name}_${timestamp}${ext}"
    }

    Move-Item -Path $file.FullName -Destination $backupFile

    Write-Host "変換完了: $($file.Name)"
}

Write-Host "すべての処理が完了しました。"
Write-Host "出力先: $outputDir"
Write-Host "退避先: $backupDir"
Write-Host "input フォルダは残しています。"
```

---

## template/blank_sjis.txt

空ファイルでOKです。

ただし、Shift-JISの空ファイルとして保存しておく想定です。

---

## 使い方

1. `input` フォルダに変換したいファイルを置く
2. `convert.bat` をダブルクリックする
3. `output` フォルダに同じファイル名で変換後ファイルが出力される
4. 元ファイルは `backup/yyyyMMdd` に移動される
5. `input` フォルダ自体は残る
6. 処理後、`input` フォルダの中は空になる

---

## 処理後のイメージ

```text
convert_tool/
├─ input/
│  └─ 空
├─ output/
│  └─ 変換後ファイル.csv
└─ backup/
   └─ 20260525/
      └─ 元ファイル.csv
```

---

## 注意点

- 出力ファイル名は入力ファイル名と同じです
- BOMは削除されます
- 出力文字コードは Shift-JIS です
- 日本語ヘッダー行もそのまま変換されます
- `input` フォルダ自体は削除されません
- `input` フォルダ内のファイルは `backup/yyyyMMdd` に移動されます
- 同名ファイルが backup にある場合は、時刻付きで退避します









# UTF-8 → Shift-JIS 変換BAT  
# ヘッダー行削除版

## 処理内容

このBATは、`input` フォルダ内のファイルを読み込み、  
**1行目のヘッダー行を削除**したうえで、UTF-8 から Shift-JIS に変換します。

変換後のファイルは `output` フォルダへ出力します。

出力ファイル名は、入力ファイル名と同じです。

変換後、元ファイルは以下のフォルダへ移動します。

```text
backup/yyyyMMdd/
```

`input` フォルダ自体は削除しません。  
処理後、`input` フォルダの中は空になります。

---

## フォルダ構成

```text
convert_tool/
├─ convert_header_delete.bat
├─ convert_header_delete.ps1
├─ template/
│  └─ blank_sjis.txt
├─ input/
│  └─ 変換したいファイル.csv
├─ output/
└─ backup/
```

---

## convert_header_delete.bat

```bat
@echo off
setlocal

cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0convert_header_delete.ps1"

pause
endlocal
```

---

## convert_header_delete.ps1

```powershell
$ErrorActionPreference = "Stop"

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$inputDir  = Join-Path $baseDir "input"
$outputDir = Join-Path $baseDir "output"
$backupRootDir = Join-Path $baseDir "backup"
$templateFile = Join-Path $baseDir "template\blank_sjis.txt"

$today = Get-Date -Format "yyyyMMdd"
$backupDir = Join-Path $backupRootDir $today

# Shift-JIS
$sjis = [System.Text.Encoding]::GetEncoding(932)

if (!(Test-Path $inputDir)) {
    Write-Host "input フォルダが存在しません。"
    exit 1
}

if (!(Test-Path $templateFile)) {
    Write-Host "テンプレートファイルが存在しません: $templateFile"
    exit 1
}

New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$files = Get-ChildItem -Path $inputDir -File

if ($files.Count -eq 0) {
    Write-Host "input フォルダにファイルがありません。"
    exit 0
}

foreach ($file in $files) {

    $outputFile = Join-Path $outputDir $file.Name

    # テンプレートをコピーして出力ファイルを作成
    Copy-Item -Path $templateFile -Destination $outputFile -Force

    # UTF-8として全行読み込み
    $lines = [System.IO.File]::ReadAllLines($file.FullName, [System.Text.Encoding]::UTF8)

    if ($lines.Count -eq 0) {
        Write-Host "空ファイルのためスキップ: $($file.Name)"
        continue
    }

    # 1行目のBOMを削除
    $lines[0] = $lines[0].TrimStart([char]0xFEFF)

    # 1行目のヘッダー行を削除
    $bodyLines = $lines | Select-Object -Skip 1

    # Shift-JISで書き込み
    [System.IO.File]::WriteAllLines($outputFile, $bodyLines, $sjis)

    # backup/yyyyMMdd に元ファイルを移動
    $backupFile = Join-Path $backupDir $file.Name

    if (Test-Path $backupFile) {
        $timestamp = Get-Date -Format "HHmmssfff"
        $name = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
        $ext  = [System.IO.Path]::GetExtension($file.Name)
        $backupFile = Join-Path $backupDir "${name}_${timestamp}${ext}"
    }

    Move-Item -Path $file.FullName -Destination $backupFile

    Write-Host "変換完了: $($file.Name)"
}

Write-Host "すべての処理が完了しました。"
Write-Host "出力先: $outputDir"
Write-Host "退避先: $backupDir"
Write-Host "input フォルダは残しています。"
```

---

## template/blank_sjis.txt

空ファイルでOKです。

ただし、Shift-JISの空ファイルとして保存しておく想定です。

---

## 使い方

1. `input` フォルダに変換したいファイルを置く
2. `convert_header_delete.bat` をダブルクリックする
3. 1行目のヘッダー行が削除される
4. UTF-8 から Shift-JIS に変換される
5. `output` フォルダに同じファイル名で出力される
6. 元ファイルは `backup/yyyyMMdd` に移動される
7. `input` フォルダ自体は残る
8. 処理後、`input` フォルダの中は空になる

---

## 処理後のイメージ

```text
convert_tool/
├─ input/
│  └─ 空
├─ output/
│  └─ 変換後ファイル.csv
└─ backup/
   └─ 20260525/
      └─ 元ファイル.csv
```

---

## 注意点

- 1行目のヘッダー行は削除されます
- 2行目以降だけが出力されます
- 出力ファイル名は入力ファイル名と同じです
- BOMは削除されます
- 出力文字コードは Shift-JIS です
- 日本語を含むヘッダー行でも削除されます
- `input` フォルダ自体は削除されません
- `input` フォルダ内のファイルは `backup/yyyyMMdd` に移動されます
- 同名ファイルが backup にある場合は、時刻付きで退避します




# CSV文字コード変換BAT

## 目的

`input` フォルダに置いたCSVファイルを、以下の条件で変換する。

- UTF-8 のCSVを読み込む
- BOMや先頭の見えない文字を削除する
- 必要に応じてヘッダー行を削除する
- Shift-JIS のCSVとして出力する
- 出力ファイル名は入力ファイル名と同じにする
- 処理後、元ファイルを `backup/yyyyMMdd` に移動する
- `input` フォルダ自体は削除しない

---

## フォルダ構成

```text
project/
├─ convert.bat
├─ input/
│  └─ sample.csv
├─ output/
│  └─ sample.csv
└─ backup/
   └─ 20260526/
      └─ sample.csv
```

---

## 処理の流れ

```text
input フォルダにCSVを置く
↓
convert.bat を実行
↓
UTF-8としてCSVを読み込む
↓
BOM・見えない先頭文字を削除
↓
必要に応じてヘッダー行を削除
↓
Shift-JISで output に出力
↓
元CSVを backup/yyyyMMdd に移動
↓
input フォルダは残す
```

---

## convert.bat

```bat
@echo off
setlocal
set "SELF=%~f0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; Invoke-Expression ((Get-Content -LiteralPath $env:SELF | Select-Object -Skip 5) -join [Environment]::NewLine)"
exit /b %ERRORLEVEL%

# ===== PowerShell part =====

$ErrorActionPreference = "Stop"

# =========================
# 設定
# =========================

# ヘッダー行を削除する場合は $true に変更
$RemoveHeader = $false

# =========================
# フォルダ設定
# =========================

$BaseDir    = Split-Path -Parent $env:SELF
$InputDir   = Join-Path $BaseDir "input"
$OutputDir  = Join-Path $BaseDir "output"
$BackupRoot = Join-Path $BaseDir "backup"
$Today      = Get-Date -Format "yyyyMMdd"
$BackupDir  = Join-Path $BackupRoot $Today

New-Item -ItemType Directory -Force -Path $InputDir   | Out-Null
New-Item -ItemType Directory -Force -Path $OutputDir  | Out-Null
New-Item -ItemType Directory -Force -Path $BackupDir  | Out-Null

# Shift-JIS
$SjisEncoding = [System.Text.Encoding]::GetEncoding(
    932,
    [System.Text.EncoderFallback]::ExceptionFallback,
    [System.Text.DecoderFallback]::ExceptionFallback
)

# UTF-8
$Utf8Encoding = [System.Text.Encoding]::UTF8

$Files = Get-ChildItem -LiteralPath $InputDir -Filter "*.csv" -File

if ($Files.Count -eq 0) {
    Write-Host "input フォルダに CSV ファイルがありません。"
    pause
    exit 0
}

$SuccessCount = 0
$ErrorCount = 0

foreach ($File in $Files) {

    Write-Host "処理中: $($File.Name)"

    try {
        $InputFile  = $File.FullName
        $OutputFile = Join-Path $OutputDir $File.Name

        # UTF-8として読み込み
        $Content = [System.IO.File]::ReadAllText($InputFile, $Utf8Encoding)

        # 先頭のBOM・ゼロ幅スペース・見えない制御文字を削除
        $Content = $Content -replace "^[\uFEFF\u200B\u200C\u200D\u2060\u0000-\u0008\u000B\u000C\u000E-\u001F]+", ""

        # ヘッダー行削除
        if ($RemoveHeader) {
            $Lines = [regex]::Split($Content, "`r`n|`n|`r")

            if ($Lines.Count -gt 1) {
                $Content = ($Lines | Select-Object -Skip 1) -join "`r`n"
            } else {
                $Content = ""
            }
        }

        # Shift-JISで出力
        [System.IO.File]::WriteAllText($OutputFile, $Content, $SjisEncoding)

        # backup/yyyyMMdd に元ファイルを移動
        $BackupFile = Join-Path $BackupDir $File.Name

        if (Test-Path -LiteralPath $BackupFile) {
            $NameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($File.Name)
            $Ext = [System.IO.Path]::GetExtension($File.Name)
            $Time = Get-Date -Format "HHmmssfff"
            $BackupFile = Join-Path $BackupDir "${NameWithoutExt}_${Time}${Ext}"
        }

        Move-Item -LiteralPath $InputFile -Destination $BackupFile

        Write-Host "完了: $($File.Name)"
        $SuccessCount++

    } catch {
        Write-Host "エラー: $($File.Name)"
        Write-Host $_.Exception.Message
        $ErrorCount++
    }
}

Write-Host ""
Write-Host "=============================="
Write-Host "処理結果"
Write-Host "成功: $SuccessCount 件"
Write-Host "失敗: $ErrorCount 件"
Write-Host "=============================="
Write-Host ""

pause
```

---

## ヘッダー行を削除したい場合

`convert.bat` 内の以下を変更する。

### 変更前

```powershell
$RemoveHeader = $false
```

### 変更後

```powershell
$RemoveHeader = $true
```

これで、CSVの1行目を削除してからShift-JISで出力する。

---

## 削除対象の見えない文字

このBATでは、CSV先頭にある以下の文字を削除する。

| 対象 | 内容 |
|---|---|
| `U+FEFF` | UTF-8 BOM |
| `U+200B` | ゼロ幅スペース |
| `U+200C` | ゼロ幅非接合子 |
| `U+200D` | ゼロ幅接合子 |
| `U+2060` | Word Joiner |
| `U+0000` など | 一部の制御文字 |

---

## BATファイルの保存形式

`convert.bat` は以下の形式で保存する。

```text
文字コード：Shift-JIS
BOM：なし
改行コード：CRLF
```

サクラエディタの場合は以下を推奨。

```text
名前を付けて保存
↓
文字コード：SJIS
↓
BOMなし
↓
改行コード：CRLF
```

---

## 注意点

### inputフォルダは削除しない

処理後、`input` フォルダ内のCSVファイルは削除ではなく、`backup/yyyyMMdd` に移動する。

```text
input/sample.csv
↓
backup/20260526/sample.csv
```

そのため、`input` フォルダ自体は残る。

---

## 出力結果

例として、以下のファイルがある場合。

```text
input/sample.csv
```

BAT実行後は以下になる。

```text
output/sample.csv
backup/20260526/sample.csv
```

`output/sample.csv` は Shift-JIS に変換されたファイル。  
`backup/20260526/sample.csv` は元の入力ファイル。

---

## BOMとは

BOMとは、ファイルの先頭に付く見えない目印のようなもの。

UTF-8のBOM付きCSVでは、先頭に見えない文字が入るため、システムによってはCSV取込エラーになることがある。

見た目は以下のように見えても、

```csv
name,age
tanaka,20
```

実際には内部的に以下のようになっている場合がある。

```text
[BOM]name,age
tanaka,20
```

この場合、システム側では `name` ではなく、BOM付きの `name` として扱われる可能性がある。

---

## バイナリ差分の確認方法

見た目が同じCSVでも、内部的に違う場合がある。

確認する場合は、Windowsのコマンドプロンプトで以下を実行する。

```bat
fc /b ok.csv ng.csv
```

差分がない場合は、以下のように表示される。

```text
FC: 相違点は検出されませんでした
```

差分がある場合は、バイト単位で違いが表示される。

---

## まとめ

このBATでできることは以下。

```text
UTF-8 CSVを読み込む
BOMを削除する
見えない先頭文字を削除する
必要ならヘッダー行を削除する
Shift-JISで出力する
元ファイルを日付別backupに移動する
inputフォルダは残す
```
