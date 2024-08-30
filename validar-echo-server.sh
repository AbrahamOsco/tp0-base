name_image="netcat:v1"
echo "Buildeando el container netcat obteniendo la imagen: "$name_image""
docker build -f ./netcat/Dockerfile -t "$name_image" . 

echo "Ejecutando el "$name_image""
docker compose -f ./netcat/docker-compose-netcat.yaml up
docker compose -f ./netcat/docker-compose-netcat.yaml stop
docker compose -f ./netcat/docker-compose-netcat.yaml down

