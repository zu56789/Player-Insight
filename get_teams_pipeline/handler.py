import logging
from extract import get_league_teams
from transform import transform_team_data
from load import get_rds_connection, insert_team_data, get_fbref_url_for_league, get_league_names

# Configure logging
logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_pipeline():
    """Run the ETL pipeline to get, transform, and load team data."""
    logger.info("Starting the team data pipeline")

    # Load league names from the database
    conn = get_rds_connection()
    league_names = get_league_names(conn)
    logger.info("Retrieved %d leagues from the database", len(league_names))
    teams_processed = 0
    teams_inserted = 0
    for league_name in league_names:
        try:
            fbref_url = get_fbref_url_for_league(conn, league_name)
            logger.info("Processing teams for league: %s", league_name)

            # Extract
            raw_team_data = get_league_teams(fbref_url)
            logger.info("Extracted %d teams for league: %s",
                        len(raw_team_data), league_name)

            # Transform and Load
            for team in raw_team_data:
                transformed_team = transform_team_data(team)
                inserted = insert_team_data(conn, transformed_team)
                if not inserted:
                    logger.warning(
                        "Failed to insert team: %s", transformed_team["team_name"])
                    continue
                else:
                    teams_inserted += 1
                    logger.info("Inserted team: %s",
                                transformed_team["team_name"])
            teams_processed += len(raw_team_data)
            logger.info("Completed processing for league: %s", league_name)

        except Exception as e:
            logger.error("Failed to process league %s: %s", league_name, e)


if __name__ == "__main__":
    run_pipeline()
