import json
from psycopg2 import connect
from psycopg2.extensions import connection
import boto3
from botocore.exceptions import ClientError


def get_secret() -> str:
    """Retrieve database credentials from AWS Secrets Manager."""

    secret_name = "player-insight-db-credentials"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session(profile_name="personal")
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return secret


def get_rds_connection() -> connection:
    """Establish a connection to the PostgreSQL RDS database."""
    secret = get_secret()
    secret_dict = json.loads(secret)

    conn = connect(
        database=secret_dict['DB_NAME'],
        user=secret_dict['DB_USERNAME'],
        password=secret_dict['DB_PASSWORD'],
        host=secret_dict['DB_HOST']
    )
    return conn
