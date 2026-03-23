@echo off
echo Building screen-scraper.exe ...
pip install pyinstaller --quiet
python -m PyInstaller screen-scraper.spec --noconfirm
echo.
echo Done. Output: dist\screen-scraper\
echo Share the dist\screen-scraper\ folder with end users.
pause
