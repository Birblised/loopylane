# Builds a page by inlining the logo, its pen path, Leaflet's CSS and the photos into a template.
# Run from anywhere:  powershell -File src\build.ps1                 (template.html -> ../index.html)
#                     powershell -File src\build.ps1 -Version <name>  (<name>\template.html -> ../<name>/index.html, for trying out a variant)
param([string]$Version = '')
$s = $PSScriptRoot
$tpl = if ($Version) { "$s\$Version\template.html" } else { "$s\template.html" }
$Out = if ($Version) { Join-Path $s "..\$Version\index.html" } else { Join-Path $s '..\index.html' }
New-Item -ItemType Directory -Force (Split-Path $Out) | Out-Null
$t = [IO.File]::ReadAllText($tpl)
$t = $t.Replace('{{LOGO}}', 'data:image/png;base64,' + [Convert]::ToBase64String([IO.File]::ReadAllBytes("$s\logo.png")))
$t = $t.Replace('{{PEN}}', [IO.File]::ReadAllText("$s\logo-pen-path.svg.txt"))
$t = $t.Replace('{{LEAFLET_CSS}}', [IO.File]::ReadAllText("$s\leaflet-1.9.4.min.css"))
$t = [regex]::Replace($t, '\{\{IMG:([\w/-]+)\}\}', { param($m) 'data:image/jpeg;base64,' + [Convert]::ToBase64String([IO.File]::ReadAllBytes("$s\photos\$($m.Groups[1].Value).jpg")) })
if ($t.Contains('{{')) { throw 'unfilled placeholder' }
[IO.File]::WriteAllText($Out, $t, (New-Object Text.UTF8Encoding $false))
"built {0:N0} KB -> {1}" -f ((Get-Item $Out).Length / 1KB), (Resolve-Path $Out)