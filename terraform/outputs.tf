output "db_endpoint" {
  value = aws_db_instance.player_insight_db.endpoint
}

output "secret_arn" {
  value = aws_secretsmanager_secret.player_insight_secret.arn
}

output "get_leagues_ecr_repository_url" {
  value = aws_ecr_repository.get_leagues_repository.repository_url
}

output "get_teams_ecr_repository_url" {
  value = aws_ecr_repository.get_teams_repository.repository_url
}