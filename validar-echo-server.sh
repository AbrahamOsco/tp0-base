name_image="netcat:v1"
docker build -f ./netcat/Dockerfile -t "$name_image" . 
# Capturamos toda la salida al hacer up del container, obtendremos hasta el resultado de ejecutar el script adentro del container 
up_output=$(docker compose -f ./netcat/docker-compose-netcat.yaml up )
echo "$up_output"
docker compose -f ./netcat/docker-compose-netcat.yaml stop
docker compose -f ./netcat/docker-compose-netcat.yaml down
echo "$up_output" | grep -oP 'action: test_echo_server \| result: (success|fail)'
