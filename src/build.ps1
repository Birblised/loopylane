# Builds ../index.html from template.html by inlining the logo, its pen path, Leaflet's CSS and the photos.
# Run from anywhere:  powershell -File src\build.ps1
param([string]$Out = (Join-Path $PSScriptRoot '..\index.html'))
$s = $PSScriptRoot
$t = [IO.File]::ReadAllText("$s\template.html")
$t = $t.Replace('{{LOGO}}', 'data:image/png;base64,' + [Convert]::ToBase64String([IO.File]::ReadAllBytes("$s\logo.png")))
$t = $t.Replace('{{PEN}}', [IO.File]::ReadAllText("$s\logo-pen-path.svg.txt"))
$t = $t.Replace('{{LEAFLET_CSS}}', [IO.File]::ReadAllText("$s\leaflet-1.9.4.min.css"))
$t = [regex]::Replace($t, '\{\{IMG:([\w/-]+)\}\}', { param($m) 'data:image/jpeg;base64,' + [Convert]::ToBase64String([IO.File]::ReadAllBytes("$s\photos\$($m.Groups[1].Value).jpg")) })
if ($t.Contains('{{')) { throw 'unfilled placeholder' }
[IO.File]::WriteAllText($Out, $t, (New-Object Text.UTF8Encoding $false))
"built {0:N0} KB -> {1}" -f ((Get-Item $Out).Length / 1KB), (Resolve-Path $Out)