# TP0: Docker + Comunicaciones + Concurrencia
## Parte 1: Introducción a Docker
### Ejercicio N°3:
Crear un script de bash `validar-echo-server.sh` que permita verificar el correcto funcionamiento del servidor utilizando el comando `netcat` para interactuar con el mismo. Dado que el servidor es un EchoServer, se debe enviar un mensaje al servidor y esperar recibir el mismo mensaje enviado.

En caso de que la validación sea exitosa imprimir: `action: test_echo_server | result: success`, de lo contrario imprimir:`action: test_echo_server | result: fail`.

El script deberá ubicarse en la raíz del proyecto. Netcat no debe ser instalado en la máquina _host_ y no se puede exponer puertos del servidor para realizar la comunicación (hint: `docker network`). `

### Solucion: 
Para ejecutar el script seguimos los sgts pasos: 
```
    1. chmod +x validar-echo-server.sh
    2. ./validar-echo-server.sh
``` 

### Ejemplo: 
Para verificar el comportamiento correcto del echo server: 
1. Levantamos el server usando: ```make docker-compose-up```  
2. Abrimos el log para visualizar el output: ``` make docker-compose-logs ``` 
3. Ejecutamos el script anteriormente mencionado ```./validar-echo-server.sh```   
4. Observar como el server nos retorna el mismo mensaje enviado "hello world" y obtenmos un **sucess**
5. Finalmene hacemos un stop y un down: 
``` docker compose -f ./netcat/docker-compose-netcat.yaml stop
    docker compose -f ./netcat/docker-compose-netcat.yaml down
```   
<img src ="./img/ej3_part_1.png">
