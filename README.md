# TP0: Docker + Comunicaciones + Concurrencia
## Parte 1: Introducción a Docker
### Ejercicio N°3:
Crear un script de bash `validar-echo-server.sh` que permita verificar el correcto funcionamiento del servidor utilizando el comando `netcat` para interactuar con el mismo. Dado que el servidor es un EchoServer, se debe enviar un mensaje al servidor y esperar recibir el mismo mensaje enviado.

En caso de que la validación sea exitosa imprimir: `action: test_echo_server | result: success`, de lo contrario imprimir:`action: test_echo_server | result: fail`.

El script deberá ubicarse en la raíz del proyecto. Netcat no debe ser instalado en la máquina _host_ y no se puede exponer puertos del servidor para realizar la comunicación (hint: `docker network`). `

### Solucion: 
Para ejecutar el script usamos los sgts comandos: 
```
    chmod +x validar-echo-server.sh
    ./validar-echo-server.sh
``` 

### Ejemplo: 
Para verificar el comportamiento correcto del echo server: 
1. Levantamos el server usando: ```make docker-compose-up```  
2. Abrimos el log para visualizar el output: ``` make docker-compose-logs ``` 
3. Ejecutamos el script anteriormente mencionado ```./validar-echo-server.sh```   
4. Se creara un container con el netcat instalado, se conectara al servidor y enviara el ensaje **hello world**.
5. El server nos retorna el "hello world" y al comparar lo enviado y recibido obtendremos un **sucess**
5. Finalmene hacemos los stop y los down: 
``` 
    docker compose -f ./netcat/docker-compose-netcat.yaml stop
    docker compose -f ./netcat/docker-compose-netcat.yaml down
    make docker-compose-down
```   
<img src ="./img/ej3_part_1.png">
