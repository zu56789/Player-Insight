import logging
from extract import get_league_teams
from transform import transform_team_data
from load import get_rds_connection, insert_team_data, get_fbref_url_for_league, get_league_names

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Run the ETL pipeline to get, transform, and load team data."""
    logger.info("Starting the team data pipeline")

    # Load league names from the database
    conn = get_rds_connection()
    league_names = get_league_names(conn)
    logger.info("Retrieved %d leagues from the database", len(league_names))
    teams_processed = 0
    teams_inserted = 0
    leagues_processed = 0

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
                try:
                    transformed_team = transform_team_data(team)
                    insert_team_data(conn, transformed_team)
                    teams_inserted += 1
                    logger.info("Inserted team: %s",
                                transformed_team["team_name"])
                except Exception as e:
                    error_msg = str(e)
                    if "duplicate key" in error_msg or "unique constraint" in error_msg:
                        logger.info("Team already exists: %s",
                                    team.get("team_name", "Unknown"))
                    else:
                        logger.warning("Failed to insert team %s: %s",
                                       team.get("team_name", "Unknown"), e)
                    continue

            teams_processed += len(raw_team_data)
            leagues_processed += 1
            logger.info("Completed processing for league: %s", league_name)

        except Exception as e:
            logger.error("Failed to process league %s: %s", league_name, e)
            conn.rollback()
            continue

    conn.close()
    logger.info("Pipeline completed: %d leagues processed, %d teams processed, %d teams inserted",
                leagues_processed, teams_processed, teams_inserted)

    return {
        "status": "SUCCESS",
        "leagues_processed": leagues_processed,
        "teams_processed": teams_processed,
        "teams_inserted": teams_inserted
    }


if __name__ == "__main__":
    result = lambda_handler(None, None)
    print(result)
