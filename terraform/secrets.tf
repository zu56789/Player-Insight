resource "aws_secretsmanager_secret" "player_insight_secret" {
  name        = "player-insight-db-credentials"
  description = "Credentials for Player Insight PostgreSQL RDS"
}

resource "aws_secretsmanager_secret_version" "player_insight_secret_value" {
  secret_id = aws_secretsmanager_secret.player_insight_secret.id

  secret_string = jsonencode({
    DB_HOST     = aws_db_instance.player_insight_db.address
    DB_NAME     = aws_db_instance.player_insight_db.db_name
    DB_USERNAME = aws_db_instance.player_insight_db.username
    DB_PASSWORD = random_password.rds_password.result
  })
}
