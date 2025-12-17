resource "aws_security_group" get_leagues_lambda_sg {
  name        = "player-insight-get-leagues-lambda-sg"
  description = "Security group for Get Leagues Lambda"
  vpc_id      = data.aws_vpc.default.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "get_leagues_lambda_to_rds" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.get_leagues_lambda_sg.id
  security_group_id        = aws_security_group.player_insight_sg.id
  description              = "Allow Get Leagues Lambda to access RDS"
}

resource "aws_iam_role" "get_leagues_lambda_role" {
  name = "player-insight-get-leagues-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = "sts:AssumeRole"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "get_leagues_lambda_logs" {
  role       = aws_iam_role.get_leagues_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "get_leagues_lambda_secrets" {
  name = "player-insight-get-leagues-secrets-access"
  role = aws_iam_role.get_leagues_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue"
      ]
      Resource = data.aws_secretsmanager_secret.player_insight_secret.arn

    }]
  })
}

resource "aws_cloudwatch_log_group" "get_leagues_lambda" {
  name              = "/aws/lambda/player-insight-get-leagues"
  retention_in_days = 7
}

resource "aws_lambda_function" "get_leagues_lambda" {
  function_name = "player-insight-get-leagues"
  role          = aws_iam_role.get_leagues_lambda_role.arn

  package_type = "Image"
  image_uri    = "${aws_ecr_repository.get_leagues.repository_url}:latest"

  timeout     = 900
  memory_size = 512

  depends_on = [
    aws_cloudwatch_log_group.get_leagues_lambda,
    aws_iam_role_policy_attachment.get_leagues_lambda_logs,
    aws_iam_role_policy.get_leagues_lambda_secrets
  ]
}
