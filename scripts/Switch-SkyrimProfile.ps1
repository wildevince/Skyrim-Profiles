<#
.SYNOPSIS
    Bascule entre profils Skyrim SE (Keizaal / Solo) en synchronisant tout le dossier My Games.

.PARAMETER Profile
    Nom du profil à activer (clé dans MyConfig.json > versions).

.PARAMETER Status
    Affiche l'état des profils sans basculer.
#>

[CmdletBinding(DefaultParameterSetName = 'Switch')]
param(
    [Parameter(Mandatory = $true, ParameterSetName = 'Switch')]
    [string]$Profile,

    [Parameter(Mandatory = $true, ParameterSetName = 'Status')]
    [switch]$Status
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$modulePath  = Join-Path $PSScriptRoot "ProfileSwitcher.psm1"

Import-Module $modulePath -Force

if ($Status) {
    Get-SkyrimProfileStatus -ProjectRoot $ProjectRoot | Format-List
    Get-SkyrimProfileStatus -ProjectRoot $ProjectRoot |
        Select-Object -ExpandProperty Profiles |
        Format-Table Name, IsActive, FileCount, Path -AutoSize
    return
}

Switch-SkyrimProfile -Profile $Profile -ProjectRoot $ProjectRoot
