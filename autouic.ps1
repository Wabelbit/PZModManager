$uiFiles = Get-ChildItem "ui/*.ui"

foreach ($item in $uiFiles)
{
    $src = $item.fullName
    $dest = $item.fullName.Substring(0, $item.fullName.length - 3) + "_ui.py"
    Write-Output "$src -> $dest"
    pyside6-uic.exe "$src" -o "$dest"
}
