# Dribl Home Assistant Integration

A comprehensive Home Assistant integration for Dribl football management platform that allows you to track clubs, teams, players, and fixtures.

## Features

- **Next Game Sensor**: Shows upcoming fixture details with team logos, venue, and Google Maps link
- **Recent Results Sensor**: Displays recent game results (customizable time period)
- **Club Following**: Track specific clubs and their information
- **Player Following**: Monitor individual player stats and profiles
- **Configuration Flow**: Easy setup through Home Assistant UI

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the "+" button
4. Search for "Dribl Football"
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Download the latest release from GitHub
2. Extract the `dribl` folder to your `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Dribl"
4. Follow the configuration steps:
   - Enter your Tenant ID (default: `7MNGJ1QmAz`)
   - Set your timezone
   - Configure results display hours
   - Set update interval
   - Select clubs to follow
   - Select players to follow (optional)

## Sensors

### Next Game Sensor (`sensor.dribl_next_game`)
- **State**: Date and time of next scheduled game
- **Attributes**:
  - `home_team`: Home team name
  - `away_team`: Away team name
  - `home_logo`: URL to home team logo
  - `away_logo`: URL to away team logo
  - `ground_name`: Venue name
  - `google_maps_link`: Direct link to Google Maps
  - `competition`: Competition name
  - `league`: League name
  - `round`: Round information
  - `status`: Game status

### Recent Results Sensor (`sensor.dribl_recent_results`)
- **State**: Number of recent completed games
- **Attributes**:
  - `results`: List of recent game results with scores, teams, and details
  - `count`: Total number of results

### Club Sensors (`sensor.dribl_[club_name]`)
- **State**: Club name
- **Attributes**:
  - `club_id`: Unique club identifier
  - `name`: Club name
  - `image`: Club logo URL
  - `email`: Contact email
  - `phone`: Contact phone
  - `website`: Club website
  - `address`: Club address information
  - `socials`: Social media links

### Player Sensors (`sensor.dribl_[player_name]`)
- **State**: Player full name
- **Attributes**:
  - `player_id`: Unique player identifier
  - `first_name`: Player first name
  - `last_name`: Player last name
  - `image`: Player photo URL
  - `age`: Player age
  - `nationality`: Player nationality
  - `is_captain`: Whether player is a captain
  - `is_goalkeeper`: Whether player is a goalkeeper
  - `clubs`: List of associated clubs
  - `career_stats`: Career statistics and match history

### Ladder Sensors (`sensor.dribl_[league_name]_ladder`)
- **State**: Number of teams in the ladder
- **Attributes**:
  - `ladder`: Complete ladder standings with all statistics
  - `team_count`: Total number of teams
  - Each team includes:
    - Position, played, won, drawn, lost, byes, forfeits
    - Goals for, goals against, goal difference
    - Points and points per game
    - Recent form (last 5 games with results and links)
    - Up next (next fixture with link)

## Usage Examples

### Automation Example
```yaml
automation:
  - alias: "Notify Next Game"
    trigger:
      - platform: state
        entity_id: sensor.dribl_next_game
    action:
      - service: notify.mobile_app
        data:
          title: "Next Game"
          message: >
            {{ state_attr('sensor.dribl_next_game', 'home_team') }} vs 
            {{ state_attr('sensor.dribl_next_game', 'away_team') }}
            at {{ states('sensor.dribl_next_game') }}
```

### Lovelace Card Example
```yaml
type: entities
title: Next Game
entities:
  - entity: sensor.dribl_next_game
    type: attribute
    attribute: home_team
    name: Home Team
  - entity: sensor.dribl_next_game
    type: attribute
    attribute: away_team
    name: Away Team
  - entity: sensor.dribl_next_game
    type: attribute
    attribute: ground_name
    name: Venue
```

## Dashboard Examples

This integration includes comprehensive dashboard examples in the `examples/` directory:

- **`ladder_tile.yaml`** - Full-featured ladder table with team logos, statistics, and clickable form indicators
- **`ladder_tile_simple.yaml`** - Simple ladder tile for quick setup
- **`ladder_card_advanced.yaml`** - Advanced ladder card with interactive features and hover effects
- **`dribl_dashboard.yaml`** - Complete multi-page dashboard with next game, results, and ladder views

See the [examples README](examples/README.md) for detailed usage instructions and customization options.

## API Information

This integration uses the Dribl API endpoints:
- `/api/fixtures` - Fixture data
- `/api/list/clubs` - Club information
- `/api/list/leagues` - League information
- `/api/list/seasons` - Season information
- `/api/list/competitions` - Competition information
- `/api/list/rounds` - Round information
- `/api/list/grounds` - Ground information
- `/api/memberprofile` - Player profiles
- `/api/memberprofile-careers` - Player career statistics
- `/api/ladders` - League ladder standings

## Support

For issues and feature requests, please use the [GitHub Issues](https://github.com/user/dribl-hass/issues) page.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.