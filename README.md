# cups-accounting

inspired by accsnmp
## Instalacion

### Requerimientos a nivel SO

apt-get install libcups2-dev libsnmp-dev
apt-get install python3 python3-pip virtualenv

### Virtual Environment

virtualenv --python=$(which python3) venv
source venv/bin/activate
pip install pycups easysnmp


## Configuracion

https://www.papercut.com/kb/Main/UnknownAndWithheldUserInCUPS

## TODO

- [ ] Funcionamiento Básico
- [ ] Documentar Instalación
- [ ] Documentar Configuración
- [ ] Agregar DB Backend (sqlalchemy?)
- [ ] Agregar Alertas (jinja y google-smtp?)
