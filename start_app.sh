
#!/bin/sh

sudo docker compose --profile kafka-server up --build -d
sleep 10
sudo docker compose --profile main-app-service up  --build -d
