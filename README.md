# TP0: Docker + Comunicaciones + Concurrencia

### Ejercicio N°4:
Modificar servidor y cliente para que ambos sistemas terminen de forma _graceful_ al recibir la signal SIGTERM. Terminar la aplicación de forma _graceful_ implica que todos los _file descriptors_ (entre los que se encuentran archivos, sockets, threads y procesos) deben cerrarse correctamente antes que el thread de la aplicación principal muera. Loguear mensajes en el cierre de cada recurso (hint: Verificar que hace el flag `-t` utilizado en el comando `docker compose down`).
### Solucion: 
Para ejecutar el ejercicio: 
```
    make docker-compose-up
    make docker-compose-logs
    docker kill --signal=SIGTERM client1
    docker kill --signal=SIGTERM server
```
De esta manera enviaremos la signal SIGTERM tanto al client con id 1, como al server. 

### Explicacion de la implementacion: 
Para resolver el ejercicio se dividio la logica en dos:
1. En el lado del server: se uso la librera signal de python y al detectar la señal setea en true el booleano **was_killed** en true y ademas cerramos el socket aceptador(listener), lo que provocaria una excepcion al trata de hacer un accept lo handelamos y retornamos None y asi continuamos hasta terminal normalmente el programa.

2. Client: Se uso la libreria basicas de os/signal, signal, syscall de go. Luego se crea un canal que almacen signals como SIGTERM y se lanza una gorrutina (un thread mas ligero) para no quedarse bloqueado en la operacion de <- (un pop o recv), el manejo es setear en true el booleano, cuando es seteado en true se espera a que termine "la iteracion del loop en curso" (cerrando bien el socket y se verifica su cierre) y la sgt iteracion se cortara el loop para terminar el programa controlada.


### Ejemplo: 
1. Ejecutando los comandos anterior vemos que tanto el client como el servidor:
<img src='./img/ej4_part_1.png'>

2. Si hacemso un **make docker-compose-up** y luego un **make docker-compose-logs** y luego un **make docker-compose-down***  obtenemos tambien que libera los recursos:
<img src='./img/ej4_part_2.png'>


2. Si mandamos la signal primero al server, el cliente y el server liberan los recursos de forma correcta: 
<img src='./img/ej4_part_3.png'>



