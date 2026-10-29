$root = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
Set-Location $root

$python = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    throw "Python venv not found at: $python"
}

& $python -u -B -c "from src.advisor import Advisor; a = Advisor('.'); print('Player data freshness:'); [print(x) for x in a.data_freshness_report()]"
& $python -u -B -c "from src.advisor import Advisor; a = Advisor('.'); print('Account:', a.summarize().account); print('Recommendations:'); [print(x) for x in a.recommend_best_next_upgrade()]"
