$uiFiles = Get-ChildItem "ui/*.ui"

foreach ($item in $uiFiles)
{
    Write-Output $item.fullName
    $dest = $item.fullName.Substring(0, $item.fullName.length - 3) + "_ui.py"
    Write-Output $dest
}