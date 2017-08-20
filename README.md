# cups-accounting

inspired by accsnmp

## Instalacion

### Requerimientos a nivel SO

```bash
sudo apt-get install python3 python3-pip virtualenv  # Para ejecutar los scripts
sudo apt-get install libcups2-dev  # Lo requiere pycups
sudo apt-get install libsnmp-dev  # Lo requiere easysnmp
sudo apt-get install snmp  # Para evitar unos warnings por la ausencia de MIBs
sudo apt-get install git  # Para clonar este repositorio
```

### Código y Virtual Environment

```bash
git clone https://github.com/dvinazza/cups-accounting.git
cd cups-accounting
virtualenv --python=$(which python3) venv
source venv/bin/activate
pip install pycups easysnmp
pip install sqlalchemy  # db backend
```

## Configuracion

### CUPS

El script necesita acceder a los detalles de los jobs en el CUPS

https://www.papercut.com/kb/Main/UnknownAndWithheldUserInCUPS

## TODO

- [x] Funcionamiento Básico (etapas de la impresión y autenticación)
- [x] Agregar Alertas (jinja y google-smtp?)
- [ ] Alertas: Separar en un objeto aparte y agregar contexto (class MailEngine o algo así?)
- [ ] Alertas: Briefing del job en cuestión
- [x] Alertas: Dominio libre en los aliases
- [ ] Homogeneizar/Simplificar la representación de cada objeto en __repr__
- [x] Documentación: Instalación
- [ ] Documentación: Configuración
- [ ] Documentación: Como extender a otra impresora
- [ ] Configuración: Documentar
- [x] Configuración: Utilizar YAML en lugar de un script de python
- [x] Configuración: Separar la config del Manager de la impresora (mismo manager puede admin varias impr)
- [x] Ejecución: Parametrizar impresora
- [x] db: Agregar DB Backend (sqlalchemy)
- [x] db: Registrar el nombre de la impresora en la Impresion?
- [ ] db: Utilizar polymorf para no tener que mapear a mano las propiedades de cups.job a db.job?
- [ ] db: Armar un front-end con las estadisticas por grupo/usuario
- [ ] db: Tabla separada con las maquinas para no escribir una y otra vez el source ip
