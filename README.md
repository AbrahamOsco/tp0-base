# TP0: Docker + Comunicaciones + Concurrencia
## Parte 3: Repaso de Concurrencia

### Ejercicio N°8:
Modificar el servidor para que permita aceptar conexiones y procesar mensajes en paralelo.
En este ejercicio es importante considerar los mecanismos de sincronización a utilizar para el correcto funcionamiento de la persistencia.

En caso de que el alumno implemente el servidor Python utilizando _multithreading_,  deberán tenerse en cuenta las [limitaciones propias del lenguaje](https://wiki.python.org/moin/GlobalInterpreterLock).

### Solucion : 
### Protocol: 

### Mecanismos de sincronizacion utilizado: 


### Ejemplo: 
1. Para ejecutar el programa usamos: 
```
    make docker-compose-up
    make docker-compose-logs
``` 


2. Garantizando la liberacion de recursos podemos ejecutar en medio de la ejecucion: 

```
    docker kill --signal=SIGTERM server
    docker kill --signal=SIGTERM client1
    docker kill --signal=SIGTERM client2
    docker kill --signal=SIGTERM client3
    docker kill --signal=SIGTERM client4
    docker kill --signal=SIGTERM client5
``` 
Observamos que se cierran el socket del cliente y el archivo csv, del lado del server se cierra el socket aceptador(listener).
