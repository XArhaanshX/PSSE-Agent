$env:PYTHONPATH = "C:\Users\arhaa\OneDrive\poc1\psse-agentic-ai;C:\Program Files\PTI\PSSE36\36.0\PSSPY311;" + $env:PYTHONPATH
$env:PATH = "C:\Program Files\PTI\PSSE36\36.0\PSSBIN;" + $env:PATH

& "C:\Users\arhaa\AppData\Local\Programs\Python\Python311\python.exe" scripts/test_sld_hypotheses.py
