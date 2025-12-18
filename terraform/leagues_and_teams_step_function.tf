# IAM Role for Step Function Execution
resource "aws_iam_role" "step_function_role" {
  name = "player-insight-leagues-and-teams-step-function-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy to allow Step Function to invoke Lambda
resource "aws_iam_role_policy" "step_function_lambda_policy" {
  name = "player-insight-leagues-and-teams-step-function-lambda-policy"
  role = aws_iam_role.step_function_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = [
          aws_lambda_function.get_leagues_lambda.arn,
          aws_lambda_function.get_teams_lambda.arn
        ]
      }
    ]
  })
}

# Step Function Definition

resource "aws_sfn_state_machine" "leagues_and_teams_state_machine" {
  name     = "player-insight-leagues-and-teams-state-machine"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode({
    Comment = "State machine to get leagues and teams"
    StartAt = "GetLeagues"
    States = {
      GetLeagues = {
        Type       = "Task"
        Resource   = aws_lambda_function.get_leagues_lambda.arn
        Next       = "GetTeams"
        Retry      = [{
          ErrorEquals = ["States.ALL"]
          IntervalSeconds = 2
          MaxAttempts = 3
          BackoffRate = 2.0
        }]
        Catch      = [{
          ErrorEquals = ["States.ALL"]
          ResultPath  = "$.error-info"
          Next        = "FailState"
        }]
      }
      GetTeams = {
        Type       = "Task"
        Resource   = aws_lambda_function.get_teams_lambda.arn
        End        = true
        Retry      = [{
          ErrorEquals = ["States.ALL"]
          IntervalSeconds = 2
          MaxAttempts = 3
          BackoffRate = 2.0
        }]
        Catch      = [{
          ErrorEquals = ["States.ALL"]
          ResultPath  = "$.error-info"
          Next        = "FailState"
        }]
      }
      FailState = {
        Type       = "Fail"
        Cause      = "Error occurred in Lambda execution"
        Error      = "LambdaFunctionError"
      }
    }
  })

}

# EventBridge Rule to trigger Step Function every 6 months
resource "aws_cloudwatch_event_rule" "leagues_and_teams_schedule" {
  name                = "player-insight-leagues-and-teams-schedule"
  description         = "Trigger leagues and teams pipeline every 6 months"
  schedule_expression = "rate(180 days)"
}

# IAM Role for EventBridge to invoke Step Function
resource "aws_iam_role" "eventbridge_step_function_role" {
  name = "player-insight-eventbridge-step-function-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy to allow EventBridge to start Step Function execution
resource "aws_iam_role_policy" "eventbridge_step_function_policy" {
  name = "player-insight-eventbridge-step-function-policy"
  role = aws_iam_role.eventbridge_step_function_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "states:StartExecution"
        ]
        Resource = aws_sfn_state_machine.leagues_and_teams_state_machine.arn
      }
    ]
  })
}

# EventBridge Target to connect the rule to the Step Function
resource "aws_cloudwatch_event_target" "step_function_target" {
  rule     = aws_cloudwatch_event_rule.leagues_and_teams_schedule.name
  arn      = aws_sfn_state_machine.leagues_and_teams_state_machine.arn
  role_arn = aws_iam_role.eventbridge_step_function_role.arn
}
