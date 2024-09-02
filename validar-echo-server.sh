name_image="netcat:v1"
docker build -f ./netcat/Dockerfile -t "$name_image" . 
docker compose -f ./netcat/docker-compose-netcat.yaml up
docker compose -f ./netcat/docker-compose-netcat.yaml stop
docker compose -f ./netcat/docker-compose-netcat.yaml down

