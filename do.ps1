param (
    [string]$command,
    [string]$agentName
)

switch ($command) {
    "a" {
        if (-not $agentName) {
            Write-Host "Fout: Geef een agent-naam op voor het 'a' commando."
            Write-Host "Gebruik: .\do.ps1 a <agent-naam>"
        } else {
            Write-Host "Agent wordt aangemaakt: $agentName..."
            python .\scripts\create-agent.py $agentName
        }
    }
    "f" {
        Write-Host "Genesis wordt opgehaald..."
        python .\scripts\fetch-genesis.py
    }
    default {
        Write-Host "Ongeldig commando. Gebruik 'a' of 'f'."
        Write-Host "Voorbeeld:"
        Write-Host "  .\do.ps1 a <agent-naam>  # Maakt een nieuwe agent aan"
        Write-Host "  .\do.ps1 f              # Haalt genesis op"
    }
}
