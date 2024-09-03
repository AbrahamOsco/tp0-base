# TP0: Docker + Comunicaciones + Concurrencia
## Parte 2: Repaso de Comunicaciones

### Ejercicio N°6:
Modificar los clientes para que envíen varias apuestas a la vez (modalidad conocida como procesamiento por _chunks_ o _batchs_). La información de cada agencia será simulada por la ingesta de su archivo numerado correspondiente, provisto por la cátedra dentro de `.data/datasets.zip`.
Los _batchs_ permiten que el cliente registre varias apuestas en una misma consulta, acortando tiempos de transmisión y procesamiento.

En el servidor, si todas las apuestas del *batch* fueron procesadas correctamente, imprimir por log: `action: apuesta_recibida | result: success | cantidad: ${CANTIDAD_DE_APUESTAS}`. En caso de detectar un error con alguna de las apuestas, debe responder con un código de error a elección e imprimir: `action: apuesta_recibida | result: fail | cantidad: ${CANTIDAD_DE_APUESTAS}`.

La cantidad máxima de apuestas dentro de cada _batch_ debe ser configurable desde config.yaml. Respetar la clave `batch: maxAmount`, pero modificar el valor por defecto de modo tal que los paquetes no excedan los 8kB. 

El servidor, por otro lado, deberá responder con éxito solamente si todas las apuestas del _batch_ fueron procesadas correctamente.


### Solucion : 
1. Se creo la clase agencyReader para desacoplar la logica de la lectura del csv del client.
2. Se garantiza la liberacion de recursos al recibir una SIGTERM en el caso de cliente o server.  
3. Se cambia el amount a 10, el loop a 100 para enviar varios BatchDTO, el period a 1s para poder enviar mas seguido y no dormir tanto 😴.
4. Se calcula el peso de cada BatchDTO y se compara con la CTE **MAX_BATCH_SIZE** (8192) si es mayor no se envia el BatchDTO (podemos verlo con un amount = 800 ).

### Protocolo: 
Protocolo mas basico explicado desde cero en el EJ5.
En este ejercicio se agrega un nuevo DTO: **BatchDTO** basicamente esta compuesto por: 
1. operation_type (u8): 1 byte
2. Una lista de BetDTO: para su serializacion se envia 2 bytes | (Para el tamanio de la lista) y luego se envia cada BetDTO. 
3. El protocolo para como enviar cada BetDTO esta en el ej5. Aca se reutiliza los metodos como **send_bet_dto**, **recv_bet_dto** de Client protocol y server protocol respectivamente. 

El server recibe el BatchDTO y envia un **AckDTO** como confirmacion del mensaje:
1. operation_type (u8): 1 byte 
2. response (u8): 1 byte | Es 0 (ACK_SUCCESS_BATCH) si recibio bien el BatchDto elserver, 
    si hubo alguna apuesta con error (**👉 Se considera error los number mayor a 9998**) tiene valor 1 (ACK_ERROR_IN_BET_BATCH).
3. current_status (string): 2 bytes + bytes del string.


Si hubo algun error o no el server loggea el resultado final de revisar el BatchDTO:
1. Si hubo error el server manda un ACK con el response 1 (ACK_ERROR_IN_BET_BATCH) y el mensaje del error. 
2. Si no hubo error el server manda un ACK con el response en 0 (ACK_SUCCESS_BATCH) y el mensaje exitoso.

El cliente recibe el AckDTO y muestra el mensaje ya sea de error o no.

### Ejemplo: 
1. Para ejecutar el programa usamos: 
```
    make docker-compose-up
    make docker-compose-logs
``` 

1. Podemos ver el archivo que escribe el server usando otra terminal y escribiendo los comandos uno por uno: 
```
    docker exec -it server sh
    ls
    cat bets.csv
```
Con un amount = 10 y loop = 100 entonces podemos obtener los 1000 primeras apuestas y guardarlas en el bets.csv del server.
<img src= './img/ej6_part1.png'>
Observamos como que el bets.csv del server tiene las ultimas 10 apuestas de las 1000 primeras de la agency-1.csv idem con las demas
agency, (considerando que no hubo apuestas con errores)

Tambien se obtienen las apuestas con errores y se printean los logs correspondientes:
En el server:
```
    docker logs server
```
<img src= './img/ej6_part2.png'>

En el cliente (caso de la agencia3 que tenia un number = 998):
``` 
    docker logs client3
```
<img src= './img/ej6_part3.png'>

Garantizando la liberacion de recursos podemos ejecutar en medio de la ejecucion: 

```
    docker kill --signal=SIGTERM server
    docker kill --signal=SIGTERM client1
    docker kill --signal=SIGTERM client2
    docker kill --signal=SIGTERM client3
    docker kill --signal=SIGTERM client4
    docker kill --signal=SIGTERM client5
``` 
Observamos que se cierran el socket del cliente y el csv, del lado del server se cierra el socket aceptador(listener).
<img src= './img/ej6_part4.png'>
