import logging
from extract import extract_top_five_leagues
from transform import transform_league_data
from load import get_rds_connection, upload_league_data

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Run the ETL pipeline to get, transform, and load league data."""
    logger.info("Starting the league data lambda")
    url = "https://fbref.com/en/"
    logger.info("Starting league data extraction from %s", url)

    # Extract
    raw_league_data = extract_top_five_leagues(url)
    logger.info("Extracted %d leagues", len(raw_league_data))

    # Transform
    logger.info("Starting league data transformation")
    transformed_league_data = []
    for league in raw_league_data:
        try:
            transformed = transform_league_data(league)
            transformed_league_data.append(transformed)
        except ValueError as e:
            logger.warning(
                "Skipping league due to transformation error: %s", e)
    logger.info("Transformed %d leagues", len(transformed_league_data))

    # Load
    logger.info("Starting league data loading into the database")
    conn = get_rds_connection()
    loaded_count = 0
    for league in transformed_league_data:
        try:
            success = upload_league_data(conn, league)
            if success:
                loaded_count += 1
                logger.info("Uploaded league: %s", league['league_name'])
            else:
                logger.info("League already exists, skipped: %s season: %s",
                            league['league_name'], league['league_season'])
        except Exception as e:
            logger.error("Failed to upload league %s: %s",
                         league['league_name'], e)
            raise

    logger.info(
        "Uploading completed. Total new leagues uploaded: %d", loaded_count)
    conn.close()
    return {
        "status": "SUCCESS",
        "leagues_processed": len(transformed_league_data),
        "leagues_inserted": loaded_count
    }
