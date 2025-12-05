-- ===========================================
-- DROP TABLES (SAFE ORDER)
-- ===========================================
DROP TABLE IF EXISTS similar_players;
DROP TABLE IF EXISTS gk_player_stats;
DROP TABLE IF EXISTS outfield_player_stats;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS league;

-- ================================
-- League Table
-- ================================
CREATE TABLE league (
    league_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    league_name TEXT NOT NULL,
    league_country TEXT,
    league_season TEXT,
    fbref_url TEXT
);

-- ================================
-- Team Table
-- ================================
CREATE TABLE team (
    team_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    team_name TEXT NOT NULL,
    league_id INTEGER REFERENCES league(league_id),
    fbref_url TEXT
);

-- ================================
-- Player Table
-- ================================
CREATE TABLE player (
    player_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    player_name TEXT NOT NULL,
    player_position TEXT NOT NULL,
    player_nationality TEXT NOT NULL,
    player_dob DATE NOT NULL,
    player_height TEXT NOT NULL,
    player_strong_foot TEXT NOT NULL,
    player_image TEXT,
    team_id INTEGER REFERENCES team(team_id),
    fbref_url TEXT,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- ================================
-- Outfield Player Stats Table
-- ================================
CREATE TABLE outfield_player_stats (
    player_stats_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES player(player_id),
    games_played INTEGER,
    games_started INTEGER,
    minutes_played INTEGER,
    goals INTEGER,
    assists INTEGER,
    xg REAL,
    xa REAL,
    shots INTEGER,
    shots_on_target INTEGER,
    yellow_cards INTEGER,
    red_cards INTEGER,
    touches INTEGER,
    successful_dribbles INTEGER,
    tackles INTEGER,
    interceptions INTEGER,
    passes_attempted INTEGER,
    passes_completed INTEGER,
    pass_completion_pcg REAL,
    season TEXT,
    competition TEXT,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- ================================
-- Goalkeeper Stats Table
-- ================================
CREATE TABLE gk_player_stats (
    gk_stats_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES player(player_id),
    games_played INTEGER,
    games_started INTEGER,
    minutes_played INTEGER,
    saves INTEGER,
    save_pcg REAL,
    goals_conceded INTEGER,
    clean_sheets INTEGER,
    psxg REAL,
    passes_attempted INTEGER,
    passes_completed INTEGER,
    pass_completion_pcg REAL,
    long_ball_attempts INTEGER,
    long_ball_completed INTEGER,
    long_ball_pcg REAL,
    crosses_faced INTEGER,
    crosses_stopped INTEGER,
    crosses_stopped_pcg REAL,
    touches INTEGER,
    yellow_cards INTEGER,
    red_cards INTEGER,
    season TEXT,
    competition TEXT,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- ================================
-- Similar Players Table
-- ================================
CREATE TABLE similar_players (
    player_comparison_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES player(player_id),
    similar_player_id INTEGER NOT NULL REFERENCES player(player_id),
    similarity_score REAL NOT NULL,
    season TEXT,
    competition TEXT,
    computed_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_comparison UNIQUE(player_id, similar_player_id)
);

-- ================================
-- INDEXES
-- ================================

-- League Indexes
CREATE INDEX idx_league_name ON league(league_name);
CREATE INDEX idx_league_season ON league(league_season);

-- Team Indexes
CREATE INDEX idx_team_league_id ON team(league_id);
CREATE INDEX idx_team_name ON team(team_name);

-- Player Indexes
CREATE INDEX idx_player_team_id ON player(team_id);
CREATE INDEX idx_player_name ON player(player_name);
CREATE INDEX idx_player_position ON player(player_position);

-- Outfield Stats Indexes
CREATE INDEX idx_outfield_player_id ON outfield_player_stats(player_id);
CREATE INDEX idx_outfield_season ON outfield_player_stats(season);

-- Goalkeeper Stats Indexes
CREATE INDEX idx_gk_player_id ON gk_player_stats(player_id);
CREATE INDEX idx_gk_season ON gk_player_stats(season);

-- Similar Players Indexes
CREATE INDEX idx_similar_player_id ON similar_players(player_id);
CREATE INDEX idx_similar_similar_player_id ON similar_players(similar_player_id);
CREATE INDEX idx_similarity_score ON similar_players(similarity_score DESC);
