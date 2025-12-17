docker build --platform linux/amd64 --provenance=false --no-cache -t player-insight-get-leagues-ecr:latest ../

aws ecr get-login-password --region eu-west-2 --profile personal | docker login --username AWS --password-stdin 486560521248.dkr.ecr.eu-west-2.amazonaws.com

docker tag player-insight-get-leagues-ecr:latest 486560521248.dkr.ecr.eu-west-2.amazonaws.com/player-insight-get-leagues-ecr:latest

docker push 486560521248.dkr.ecr.eu-west-2.amazonaws.com/player-insight-get-leagues-ecr:latest