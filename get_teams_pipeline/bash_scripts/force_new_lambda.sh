aws lambda update-function-code \
  --function-name player-insight-get-teams \
  --region eu-west-2 \
  --profile personal \
  --image-uri 486560521248.dkr.ecr.eu-west-2.amazonaws.com/player-insight-get-teams-ecr:latest