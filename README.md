# ERVIL (ITSM - ITIL Practices)


## Virtual Env
```
pip install virtualenv --user
python -m venv .venv
source .venv/Scripts/activate
## para desenvolvimento
pip install -r requirements.txt
## para testes
pip install -r requirements_tests.txt
## desativando ambiente virtual
deactivate
```

## Build docker image
```
cd app
docker build -t ervil:0.0.1 .
```
