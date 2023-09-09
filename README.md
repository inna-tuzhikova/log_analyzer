# Log Analyzer
 Homework #1 (OTUS. Python Developer. Professional)

No deps project to cook html reports on webservice request time based on nginx 
logs

## Run script
`cd /path/to/repo`

`python3.10 log_analyzer/log_analyzer.py`

Config file `config.json` can be specified in `./data/config.json` (default 
path).

Extra `--config` config.json can be specified in script params

## Run tests
`cd /path/to/repo`

`python3.10 -m unittest discover tests/ -v`
