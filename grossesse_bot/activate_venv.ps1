Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host "Environnement virtuel activé !" -ForegroundColor Green
Write-Host ""
Write-Host "Pour lancer le serveur Django, tapez: python manage.py runserver" -ForegroundColor Yellow
Write-Host "Pour installer des packages, tapez: pip install nom_du_package" -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
