param(
    [string]$PythonExe = 'python'
)

function Start-ServiceProc($name, $args) {
    Write-Host "[*] Avvio $name..."
    Start-Process -FilePath $args[0] -ArgumentList ($args[1..($args.Length-1)]) -NoNewWindow
}

Start-ServiceProc 'AZR' @($PythonExe, 'agents/azr_server.py')
Start-ServiceProc 'Ollama' @('ollama','serve')
Start-ServiceProc 'EyeAgent' @($PythonExe, 'modules/vision/eye_agent.py')
Start-ServiceProc 'Josh Bridge' @($PythonExe, 'integrations/bridge_josch.py')
Start-ServiceProc 'n8n' @('n8n','start')
Start-ServiceProc 'SleepTimeCompute' @($PythonExe, 'modules/scheduler/sleep_time_compute.py')
