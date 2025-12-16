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


def upload_league_data(conn: connection, league_data: dict) -> bool:
    """Upload league data to the PostgreSQL RDS database."""
    check_query = """
        SELECT * FROM league
        WHERE league_name = %s AND league_season = %s;
        """
    with conn.cursor() as cursor:

        cursor.execute(check_query, (
            league_data['league_name'],
            league_data['league_season']
        ))
        existing_league = cursor.fetchone()
        if existing_league:
            return False  # League data already exists

        insert_query = """
        INSERT INTO league (league_name, league_country, league_season, fbref_url)
        VALUES (%s, %s, %s, %s);
        """

        cursor.execute(insert_query, (
            league_data['league_name'],
            league_data['league_country'],
            league_data['league_season'],
            league_data['fbref_url']
        ))
        return True
