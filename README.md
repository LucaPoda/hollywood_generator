# hollywood_generator
Generatore di dati casuali per popolare il database dell'assignment di Bouquet

# Configurazione:
Installare il modulo *psycopg2* tramite pip. Digitare il seguente comando nel terminale:

```
pip instal psycopg2
```

Creare un file chiamato 'connetion.ini' nella stessa cartella dello script e inserire il segurente contenuto (modificando i campi con i dati di accesso al proprio database): 

```
[postgresql]
host=000.000.000.000
port=5432
database=DbName
user=postgres
password=my_password
```
