# cups-accounting

inspired by accsnmp
## Instalacion

### Requerimientos a nivel SO

apt-get install libcups2-dev libsnmp-dev snmp
apt-get install python3 python3-pip virtualenv

### Virtual Environment

virtualenv --python=$(which python3) venv
source venv/bin/activate
pip install pycups easysnmp

## Configuracion

### CUPS

https://www.papercut.com/kb/Main/UnknownAndWithheldUserInCUPS

## TODO

- [x] Funcionamiento Básico (etapas de la impresión y autenticación)
- [x] Agregar Alertas (jinja y google-smtp?)
- [ ] Separar Alertas y agregar contexto (class MailEngine o algo así?)
- [ ] Documentar Instalación
- [ ] Documentar Configuración
- [ ] Agregar DB Backend (sqlalchemy?)
