echo "Buildeando netcat obteniendo la imagen: netcat:v1"
docker build -f ./netcat/Dockerfile -t netcat:v1 . 

echo "Ejecutando el netcat:v1"
docker compose -f ./netcat/docker-compose-netcat.yaml up


