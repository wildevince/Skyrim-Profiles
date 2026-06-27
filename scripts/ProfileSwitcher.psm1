# Module de bascule entre profils Skyrim SE (My Games).

function Get-SkyrimProfileConfig {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot
    )

    $configFile = Join-Path $ProjectRoot "MyConfig.json"
    if (-not (Test-Path -LiteralPath $configFile)) {
        throw "Fichier de configuration introuvable : $configFile"
    }

    $raw = Get-Content -LiteralPath $configFile -Raw -Encoding UTF8
    return [PSCustomObject]@{
        Config     = ($raw | ConvertFrom-Json)
        ConfigFile = $configFile
        ProjectRoot = $ProjectRoot
    }
}

function Save-SkyrimProfileConfig {
    param(
        [Parameter(Mandatory = $true)]
        $Config,
        [Parameter(Mandatory = $true)]
        [string]$ConfigFile
    )

    $json = $Config | ConvertTo-Json -Depth 5
    Set-Content -LiteralPath $ConfigFile -Value $json -Encoding UTF8
}

function Resolve-SkyrimProfilePath {
    param(
        $Config,
        [string]$ProfileName
    )

    $relativeOrAbsolute = $Config.versions.$ProfileName
    if ([string]::IsNullOrWhiteSpace($relativeOrAbsolute)) {
        throw "Profil inconnu : $ProfileName"
    }

    if ([System.IO.Path]::IsPathRooted($relativeOrAbsolute)) {
        return $relativeOrAbsolute
    }

    return Join-Path $Config.profilesRoot $relativeOrAbsolute
}

function Sync-SkyrimDirectory {
    param(
        [string]$Source,
        [string]$Destination,
        [switch]$Mirror
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        New-Item -ItemType Directory -Path $Source -Force | Out-Null
    }

    if (-not (Test-Path -LiteralPath $Destination)) {
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    }

    $robocopyArgs = @(
        $Source,
        $Destination,
        "/E", "/COPY:DAT", "/R:2", "/W:2",
        "/NFL", "/NDL", "/NJH", "/NJS", "/NC", "/NS"
    )

    if ($Mirror) {
        $robocopyArgs += "/MIR"
    }

    & robocopy @robocopyArgs | Out-Null

    if ($LASTEXITCODE -ge 8) {
        throw "Echec de la synchronisation $Source -> $Destination (robocopy code $LASTEXITCODE)"
    }
}

function Get-SkyrimProfileStatus {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot
    )

    $ctx = Get-SkyrimProfileConfig -ProjectRoot $ProjectRoot
    $config = $ctx.Config
    $profiles = @($config.versions.PSObject.Properties.Name)

    $details = foreach ($name in $profiles) {
        $path = Resolve-SkyrimProfilePath -Config $config -ProfileName $name
        $fileCount = 0
        if (Test-Path -LiteralPath $path) {
            $fileCount = (Get-ChildItem -LiteralPath $path -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object).Count
        }

        [PSCustomObject]@{
            Name      = $name
            Path      = $path
            FileCount = $fileCount
            IsActive  = ($name -eq $config.active_version)
        }
    }

    return [PSCustomObject]@{
        ActiveProfile = $config.active_version
        LastSwitch    = $config.last_switch
        LastBackup    = $config.last_backup
        TargetRoot    = $config.targetRoot
        Profiles      = $details
    }
}

function Initialize-SkyrimProfiles {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InitialProfile,
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot
    )

    $ctx = Get-SkyrimProfileConfig -ProjectRoot $ProjectRoot
    $config = $ctx.Config
    $configFile = $ctx.ConfigFile

    $availableProfiles = @($config.versions.PSObject.Properties.Name)
    if ($InitialProfile -notin $availableProfiles) {
        throw "Profil initial inconnu : $InitialProfile. Disponibles : $($availableProfiles -join ', ')"
    }

    $profilesRoot = $config.profilesRoot
    $targetRoot   = $config.targetRoot
    $backupRoot   = Join-Path $profilesRoot $config.backupRoot

    if (-not (Test-Path -LiteralPath $profilesRoot)) {
        throw "Dossier des profils introuvable : $profilesRoot"
    }

    if (-not (Test-Path -LiteralPath $targetRoot)) {
        New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
    }

    if (-not (Test-Path -LiteralPath $backupRoot)) {
        New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
    }

    foreach ($name in $availableProfiles) {
        $profilePath = Resolve-SkyrimProfilePath -Config $config -ProfileName $name
        if (-not (Test-Path -LiteralPath $profilePath)) {
            New-Item -ItemType Directory -Path $profilePath -Force | Out-Null
        }
    }

    $initialPath = Resolve-SkyrimProfilePath -Config $config -ProfileName $InitialProfile
    Write-Host "Capture initiale depuis My Games vers $InitialProfile..."
    Sync-SkyrimDirectory -Source $targetRoot -Destination $initialPath -Mirror

    $config.active_version = $InitialProfile
    $config.last_switch    = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    Save-SkyrimProfileConfig -Config $config -ConfigFile $configFile

    return [PSCustomObject]@{
        Success       = $true
        InitialProfile = $InitialProfile
        ProfilePath   = $initialPath
        TargetRoot    = $targetRoot
    }
}

function Switch-SkyrimProfile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Profile,
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot,
        [switch]$Quiet
    )

    $ErrorActionPreference = "Stop"
    $messages = [System.Collections.Generic.List[string]]::new()

    function Write-Step {
        param([string]$Text)
        $messages.Add($Text) | Out-Null
        if (-not $Quiet) {
            Write-Host $Text
        }
    }

    $ctx = Get-SkyrimProfileConfig -ProjectRoot $ProjectRoot
    $config = $ctx.Config
    $configFile = $ctx.ConfigFile

    $availableProfiles = @($config.versions.PSObject.Properties.Name)
    if ($Profile -notin $availableProfiles) {
        throw "Profil inconnu : $Profile. Disponibles : $($availableProfiles -join ', ')"
    }

    $profilesRoot = $config.profilesRoot
    $targetRoot   = $config.targetRoot
    $backupRoot   = Join-Path $profilesRoot $config.backupRoot
    $sourceRoot   = Resolve-SkyrimProfilePath -Config $config -ProfileName $Profile

    if (-not (Test-Path -LiteralPath $profilesRoot)) {
        throw "Dossier des profils introuvable : $profilesRoot"
    }

    if (-not (Test-Path -LiteralPath $sourceRoot)) {
        New-Item -ItemType Directory -Path $sourceRoot -Force | Out-Null
        Write-Step "Dossier profil cree : $sourceRoot"
    }

    if (-not (Test-Path -LiteralPath $targetRoot)) {
        New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
    }

    if (-not (Test-Path -LiteralPath $backupRoot)) {
        New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
    }

    $activeProfile = $config.active_version

    if (-not [string]::IsNullOrWhiteSpace($activeProfile) -and $activeProfile -ne $Profile) {
        $activeProfilePath = Resolve-SkyrimProfilePath -Config $config -ProfileName $activeProfile
        if (-not (Test-Path -LiteralPath $activeProfilePath)) {
            New-Item -ItemType Directory -Path $activeProfilePath -Force | Out-Null
        }

        Write-Step "Sauvegarde du profil actif ($activeProfile) depuis My Games..."
        Sync-SkyrimDirectory -Source $targetRoot -Destination $activeProfilePath -Mirror
    }

    $timestamp  = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $thisBackup = Join-Path $backupRoot $timestamp
    New-Item -ItemType Directory -Path $thisBackup -Force | Out-Null

    Write-Step "Backup de My Games vers : $thisBackup"
    Sync-SkyrimDirectory -Source $targetRoot -Destination $thisBackup

    Write-Step "Deploiement du profil $Profile vers My Games..."
    Sync-SkyrimDirectory -Source $sourceRoot -Destination $targetRoot -Mirror

    $config.active_version = $Profile
    $config.last_switch    = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $config.last_backup    = $thisBackup
    Save-SkyrimProfileConfig -Config $config -ConfigFile $configFile

    if (-not $Quiet) {
        Write-Host ""
        Write-Host "Profil actif   : $Profile"
        Write-Host "Source         : $sourceRoot"
        Write-Host "Cible          : $targetRoot"
        Write-Host "Backup         : $thisBackup"
        Write-Host "Config         : $configFile"
    }

    return [PSCustomObject]@{
        Success  = $true
        Profile  = $Profile
        Source   = $sourceRoot
        Target   = $targetRoot
        Backup   = $thisBackup
        Messages = $messages.ToArray()
    }
}

Export-ModuleMember -Function @(
    'Get-SkyrimProfileConfig',
    'Get-SkyrimProfileStatus',
    'Initialize-SkyrimProfiles',
    'Switch-SkyrimProfile'
)
