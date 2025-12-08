output "db_endpoint" {
  value = aws_db_instance.player_insight_db.endpoint
}

output "secret_arn" {
  value = aws_secretsmanager_secret.player_insight_secret.arn
}