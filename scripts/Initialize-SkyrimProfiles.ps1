<#
.SYNOPSIS
    Premiere installation : cree les dossiers profils et capture le contenu actuel de My Games.

.PARAMETER InitialProfile
    Nom du profil correspondant au contenu actuel de targetRoot (ex. Solo, Keizaal).
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$InitialProfile
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$modulePath  = Join-Path $PSScriptRoot "ProfileSwitcher.psm1"

Import-Module $modulePath -Force
Initialize-SkyrimProfiles -InitialProfile $InitialProfile -ProjectRoot $ProjectRoot
