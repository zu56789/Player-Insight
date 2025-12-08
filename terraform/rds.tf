resource "random_password" "rds_password" {
  length           = 20
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

############################################
# DB VPC AND SUBNETS
############################################

# Default VPC
data "aws_vpc" "default" {
  id = "vpc-0b85e609b5afc35b1"
}

# Default subnets
data "aws_subnet" "subnet_a" {
  id = "subnet-07b10dcb47b5ec997"
}

data "aws_subnet" "subnet_b" {
  id = "subnet-020007e1b677bd81d"
}

data "aws_subnet" "subnet_c" {
  id = "subnet-04339d1458304bd3f"
}


############################################
# DB SUBNET GROUP
############################################

resource "aws_db_subnet_group" "player_insight_subnets" {
  name       = "player-insight-db-subnet-group"
  subnet_ids = [
    data.aws_subnet.subnet_a.id,
    data.aws_subnet.subnet_b.id,
    data.aws_subnet.subnet_c.id
  ]

  description = "Subnet group for Player Insight RDS"
}


############################################
# SECURITY GROUP
############################################

resource "aws_security_group" "player_insight_sg" {
  name        = "player-insight-db-sg"
  description = "Security group for Player Insight RDS"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Allow Postgres"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


############################################
# RDS INSTANCE
############################################

resource "aws_db_instance" "player_insight_db" {
  identifier              = "player-insight-db"
  engine                  = "postgres"
  engine_version          = "17.6"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  max_allocated_storage   = 100
  db_name                 = "player_insight_db"
  username                = "player_insight_admin"
  password                = random_password.rds_password.result
  publicly_accessible     = true                
  skip_final_snapshot     = true             
  vpc_security_group_ids  = [aws_security_group.player_insight_sg.id]
  db_subnet_group_name    = aws_db_subnet_group.player_insight_subnets.name
}
