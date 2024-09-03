# TP0: Docker + Comunicaciones + Concurrencia
## Parte 2: Repaso de Comunicaciones

### Ejercicio N°5:
Modificar la lógica de negocio tanto de los clientes como del servidor para nuestro nuevo caso de uso.

#### Cliente
Emulará a una _agencia de quiniela_ que participa del proyecto. Existen 5 agencias. Deberán recibir como variables de entorno los campos que representan la apuesta de una persona: nombre, apellido, DNI, nacimiento, numero apostado (en adelante 'número'). Ej.: `NOMBRE=Santiago Lionel`, `APELLIDO=Lorca`, `DOCUMENTO=30904465`, `NACIMIENTO=1999-03-17` y `NUMERO=7574` respectivamente.

Los campos deben enviarse al servidor para dejar registro de la apuesta. Al recibir la confirmación del servidor se debe imprimir por log: `action: apuesta_enviada | result: success | dni: ${DNI} | numero: ${NUMERO}`.

#### Servidor
Emulará a la _central de Lotería Nacional_. Deberá recibir los campos de la cada apuesta desde los clientes y almacenar la información mediante la función `store_bet(...)` para control futuro de ganadores. La función `store_bet(...)` es provista por la cátedra y no podrá ser modificada por el alumno.
Al persistir se debe imprimir por log: `action: apuesta_almacenada | result: success | dni: ${DNI} | numero: ${NUMERO}`.

#### Comunicación:
Se deberá implementar un módulo de comunicación entre el cliente y el servidor donde se maneje el envío y la recepción de los paquetes, el cual se espera que contemple:
* Definición de un protocolo para el envío de los mensajes.
* Serialización de los datos.
* Correcta separación de responsabilidades entre modelo de dominio y capa de comunicación.
* Correcto empleo de sockets, incluyendo manejo de errores y evitando los fenómenos conocidos como [_short read y short write_](https://cs61.seas.harvard.edu/site/2018/FileDescriptors/).


### Solucion : 
1. Como cada cliente (Agencia quinela) envia una unica apuesta (no tiene sentido que se envie 5 veces el mismo numero) cambie el loop amount a 1. 
1. Para la implementacion del protocolo se uso el patron DTO creando los DTO: ackDTO y betDTO.
1. Ademas se creo la clase socketTCP que encapsula el comportamiento para evitar los short read/write y ademas recibe solo bytes y retorna bytes, es el protocolo quien se encarga de serializar ints como (u8) (u16) o strings a bytes para luego enviarlo por el objeto SocketTCP.
1. Se crearon las clases ServerProtocol y ClientProtocol ambos heredan de Protocol, esto para hacer escalable cuando hayan mas tipos de mensaje, 
ademas reduce la probabilidad de problemas en los protocolo debido a la simetria de los send y recv en los metodos **asociados** de la clases hijas hace muy dificil equivocarse, un ejemplo:
1. Si el ClientProtocol tiene un metodo que es send_bet_dto(a_bet_dto) entonces el server tendra su metodo **simetrico** recv_bet_dto(), estos son los **metodos asociados**
1. 👉 Cuando se envia un string se envia en primer lugar 2 bytes (u16) con el tamaño del string en bytes y luego se envia el string (en bytes-codificado a utf8), el que recibe es lo mismo recibe primero los 2 bytes (u16) y con eso ya sabe cuantos bytes esperar para obtener el string.


### Protocolo: 
En primer lugar el cliente envia un **betDTO** compuesto por: 
1. operation_type (u8): 1 byte | sirve para identificar el tipo de operacion cada dto tiene uno. 
2. agency_id (u8): 1 byte | id de la agencia.
3. name (string): 2 bytes (u16:tamanio del string codificado) + bytes del strings |
4. last_name (string): 2 bytes + bytes del string
5. dni (string):  2 bytes + bytes del string.
6. birthday (string): 2 bytes + bytes del string.
7. number: (u16) 2 bytes : numero de la apuesta.   

El server recibe el betDTO y envia un **AckDTO**:
1. operation_type (u8): 1 byte 
2. response (u8): 1 byte | Es 0 (ACK_SUCCESS_BET) si recibio bien el betDTO el server.
3. current_status (string): 2 bytes + bytes del string: | se usa para mandar algun mensaje mas descriptivo de la situacion.

El cliente recibe el ackDTO y termina. Ese es todo el protocolo por ahora en el ejercicio 5. 
El servidor recibe correctamente las apuestas y las escribe en el csv. 

### Ejecuion y ejemplo: 
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
<img src = './img/ej5_1.png'>

