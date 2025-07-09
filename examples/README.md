# Dribl Home Assistant Integration Examples

This directory contains example configurations for using the Dribl Football integration with Home Assistant dashboards.

## Files

### `ladder_tile.yaml`
A comprehensive ladder markdown card that displays:
- Full league standings table
- Team logos and names
- All statistics (P, W, D, L, GF, GA, GD, Pts)
- Recent form indicators with clickable links to match details
- Color-coded positioning (top 3 in green, bottom 3 in red)
- Responsive design with scrolling for long ladders
- **Fixed:** Now uses markdown card format (works reliably)

### `ladder_tile_simple.yaml`
A basic tile configuration:
- Standard Home Assistant tile
- Shows team count and league leader
- Leader name and points in secondary info
- Simple tap action for more details

### `ladder_entity_card.yaml`
Simple entity card showing:
- Basic ladder information
- Team count attribute
- Standard entity card format

### `ladder_entities_basic.yaml`
Basic entities card (no custom components):
- Shows team count
- Standard Home Assistant entities only
- Simple and reliable

### `ladder_markdown_card.yaml`
Markdown card with ladder table:
- Simple table format
- Top 8 teams
- Basic statistics (P, W, D, L, Pts)
- Works with standard Home Assistant

### `ladder_entities_card.yaml`
Advanced entities card (requires custom components):
- Shows top 3 teams
- Points information
- Template entity rows

### `ladder_card_advanced.yaml`
Advanced interactive ladder card:
- ⚠️ **Note:** Complex configuration, may have issues
- Hover effects and animations
- Enhanced visual styling
- Interactive form indicators

### `ladder_card_working.yaml`
Working advanced ladder card:
- **Recommended:** Reliable alternative to advanced card
- Uses only standard Home Assistant features
- Enhanced styling with gradients
- Clickable form indicators
- Sticky header with scrolling

### `dribl_dashboard.yaml`
A complete dashboard example featuring:
- Next game card with team logos and match details
- Recent results with scores and team information
- League ladder with condensed view
- Separate pages for clubs and players
- Responsive grid layout

## Player Cards

### `player_card_simple.yaml`
Basic player entity card:
- Simple entity card format
- Shows player name and basic info
- Most reliable option

### `player_tile_simple.yaml`
Simple player tile:
- Shows player photo as entity picture
- Age, captain, and goalkeeper status
- Secondary info with key details

### `player_card_detailed.yaml`
Comprehensive player profile:
- Player photo and basic information
- Club affiliations
- Complete career statistics table
- Season-by-season breakdown
- Professional layout with styling

### `player_stats_card.yaml`
Statistics-focused player card:
- Career summary with totals
- Visual statistics display
- Season-by-season performance
- Clean, data-focused design

### `player_entities_card.yaml`
Entities-based player information:
- Uses template entity rows (requires custom components)
- Shows all player attributes
- Club information display

### `player_entities_basic.yaml`
Basic entities player card:
- No custom components required
- Standard Home Assistant entities only
- Shows key player attributes

### `player_grid_card.yaml`
Multiple players in grid:
- Shows 4 players in grid layout
- Tile format with key info
- Good for team overview

### `player_dashboard.yaml`
Complete player dashboard:
- Multi-page layout
- Team squad overview
- Individual player profiles
- Navigation between players
- Career statistics and details

## Usage

1. Copy the desired YAML configuration
2. Add it to your Home Assistant dashboard
3. Replace entity names with your actual Dribl sensor entities
4. Customize colors, icons, and layout as needed

## Entity Names

The examples use sample entity names. Replace these with your actual entities:
- `sensor.dribl_next_game` - Next game sensor
- `sensor.dribl_recent_results` - Recent results sensor
- `sensor.dribl_2025_ladder` - League ladder sensor
- `sensor.dribl_university_of_tasmania_football_club` - Club sensor
- `sensor.dribl_john_doe` - Player sensor
- `sensor.dribl_jane_smith` - Player sensor
- `sensor.dribl_mike_wilson` - Player sensor
- `sensor.dribl_sarah_jones` - Player sensor

## Customization

### Colors
Available tile colors: `red`, `pink`, `purple`, `deep-purple`, `indigo`, `blue`, `light-blue`, `cyan`, `teal`, `green`, `light-green`, `lime`, `yellow`, `amber`, `orange`, `deep-orange`, `brown`, `grey`, `blue-grey`

### Icons
Common football-related icons:
- `mdi:soccer` - Football/soccer ball
- `mdi:soccer-field` - Soccer field
- `mdi:shield-star` - Club shield
- `mdi:account-circle` - Player
- `mdi:format-list-numbered` - Ladder/standings
- `mdi:trophy` - Trophy/championship

### Layout Options
Adjust grid size with `layout_options`:
```yaml
layout_options:
  grid_columns: 4  # Width (1-4)
  grid_rows: 3     # Height (1-6)
```

## Features

### Clickable Links
The ladder tile includes clickable recent form indicators that link to match details on the Dribl website using your configured subdomain.

### Responsive Design
All tiles are designed to work on desktop and mobile devices with appropriate scrolling and sizing.

### Real-time Updates
All tiles automatically update when Home Assistant refreshes the sensor data based on your configured update interval.

## Troubleshooting

### Configuration Errors
If you get "Configuration error" messages:
1. **Use the simple configurations first:** Start with `ladder_tile_simple.yaml` or `ladder_entity_card.yaml`
2. **Check YAML syntax:** Ensure proper indentation and no tabs
3. **Verify entity exists:** Make sure `sensor.dribl_2025_ladder` exists in your Home Assistant
4. **Try basic markdown card:** Use `ladder_markdown_card.yaml` as it works with standard HA

### Entity Not Found
If you get "Entity not found" errors:
1. Check that the Dribl integration is properly configured
2. Verify the entity names match your actual sensors
3. Ensure the sensors have data (may take a few minutes after setup)
4. Check Developer Tools > States to see available entities

### Images Not Loading
If team logos don't appear:
1. Check that the Dribl API is returning image URLs
2. Verify your network can access the Dribl CDN
3. Check Home Assistant logs for any image loading errors

### Template Errors
If you see template rendering errors:
1. Ensure the sensor attributes exist
2. Check that the data structure matches the expected format
3. Verify the sensor is returning data (check in Developer Tools > States)
4. Start with simpler cards before using advanced templates

### Recommended Starting Order

**For Ladder Cards:**
1. `ladder_entity_card.yaml` - Simplest, most reliable
2. `ladder_entities_basic.yaml` - Basic entities card
3. `ladder_tile_simple.yaml` - Basic tile with leader info
4. `ladder_markdown_card.yaml` - Simple table format
5. `ladder_tile.yaml` - Full featured ladder table
6. `ladder_card_working.yaml` - Advanced features that work reliably

**For Player Cards:**
1. `player_card_simple.yaml` - Simplest, most reliable
2. `player_entities_basic.yaml` - Basic player attributes
3. `player_tile_simple.yaml` - Tile with photo
4. `player_stats_card.yaml` - Statistics focused
5. `player_card_detailed.yaml` - Comprehensive profile
6. `player_dashboard.yaml` - Complete dashboard