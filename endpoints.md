https://mc-api.dribl.com/api/fixtures?date_range=all&season=OVdzZ6ZdGr&competition=V8dnjVvdwL&league=6lNbBZvENx&club=bam1BJqNwX&date[]=2025-07-09&tenant=7MNGJ1QmAz&timezone=Australia%2FHobart
This endpoint is for the following:

- Date: All Fixtures (options are "default", "all", "single-date" with date=YYYY-MM-DD, or "date_range" with date=2025-05-14&date=2025-07-09)
- Season: 2025 (this is a single option, the season hash_id. If omitted, it defaults to the current season)
- Competition: Southern Championship (options are empty (all), or a specific competition hash_id)
- League: Southern Championship Women
  (options are empty (all), or a specific league hash_id)
- Club: University of Tasmania Football Club (options are empty (all), or a specific club hash_id)
- Round: All rounds
- Ground: All grounds (options are empty (all), or a specific ground hash_id)
- Match Type: All match types (options are empty (all),
  roundrobin
  finals
  knockout)
- Match Status: All match statuses (options are empty (all),
  pending,
  complete,
  forfeit,
  cancelled,
  abandoned,
  washout,
  washout_cancelled,
  washout_reschedule,
  postponed)

https://mc-api.dribl.com/api/list/leagues?disable_paging=true&tenant=7MNGJ1QmAz&competition=eRdkY6RNGX&sort=%2Bname
Returns the leagues;

```json
{
  "data": [
    {
      "type": "leagues",
      "id": "OEN2XvwZdq",
      "value": "OEN2XvwZdq",
      "order": 23801,
      "title": "Championship League Cup",
      "name": "Championship League Cup",
      "ladder_access": "public",
      "result_access": "public",
      "fixture_access": "public",
      "image": null,
      "links": {
        "self": { "href": "https://mc-api.dribl.com/api/leagues/OEN2XvwZdq" }
      }
    },
    {
      "type": "leagues",
      "id": "7MNG1Q2pdA",
      "value": "7MNG1Q2pdA",
      "order": 23804,
      "title": "Championship Reserves League Cup",
      "name": "Championship Reserves League Cup",
      "ladder_access": "public",
      "result_access": "public",
      "fixture_access": "public",
      "image": null,
      "links": {
        "self": { "href": "https://mc-api.dribl.com/api/leagues/7MNG1Q2pdA" }
      }
    },
    {
      "type": "leagues",
      "id": "Bjma5o16mR",
      "value": "Bjma5o16mR",
      "order": 16571,
      "title": "Kappa Southern Championship",
      "name": "Kappa Southern Championship",
      "ladder_access": "public",
      "result_access": "public",
      "fixture_access": "public",
      "image": null,
      "links": {
        "self": { "href": "https://mc-api.dribl.com/api/leagues/Bjma5o16mR" }
      }
    },
    {
      "type": "leagues",
      "id": "A4KLX8EoKq",
      "value": "A4KLX8EoKq",
      "order": 18698,
      "title": "Southern Championship Reserves",
      "name": "Southern Championship Reserves",
      "ladder_access": "public",
      "result_access": "public",
      "fixture_access": "public",
      "image": null,
      "links": {
        "self": { "href": "https://mc-api.dribl.com/api/leagues/A4KLX8EoKq" }
      }
    },
    {
      "type": "leagues",
      "id": "A4KLXDP1Kq",
      "value": "A4KLXDP1Kq",
      "order": 18440,
      "title": "Southern Championship Women",
      "name": "Southern Championship Women",
      "ladder_access": "public",
      "result_access": "public",
      "fixture_access": "public",
      "image": null,
      "links": {
        "self": { "href": "https://mc-api.dribl.com/api/leagues/A4KLXDP1Kq" }
      }
    }
  ]
}
```

https://mc-api.dribl.com/api/list/rounds?date_range=all&season=LBdDbV4Nb7&date[]=2025-05-14&competition=eRdkY6RNGX&tenant=7MNGJ1QmAz&timezone=Australia%2FHobart
Returns the rounds;

```json
[
  { "value": "roundrobin_1", "title": " Round 1", "name": " Round 1" },
  { "value": "roundrobin_2", "title": " Round 2", "name": " Round 2" },
  { "value": "roundrobin_3", "title": " Round 3", "name": " Round 3" },
  { "value": "roundrobin_4", "title": " Round 4", "name": " Round 4" },
  { "value": "roundrobin_5", "title": " Round 5", "name": " Round 5" },
  { "value": "roundrobin_6", "title": " Round 6", "name": " Round 6" },
  { "value": "roundrobin_7", "title": " Round 7", "name": " Round 7" },
  { "value": "roundrobin_8", "title": " Round 8", "name": " Round 8" },
  { "value": "roundrobin_9", "title": " Round 9", "name": " Round 9" },
  { "value": "roundrobin_10", "title": " Round 10", "name": " Round 10" },
  { "value": "roundrobin_11", "title": " Round 11", "name": " Round 11" },
  { "value": "roundrobin_12", "title": " Round 12", "name": " Round 12" },
  { "value": "roundrobin_13", "title": " Round 13", "name": " Round 13" },
  { "value": "roundrobin_14", "title": " Round 14", "name": " Round 14" },
  { "value": "roundrobin_15", "title": " Round 15", "name": " Round 15" },
  { "value": "roundrobin_16", "title": " Round 16", "name": " Round 16" },
  { "value": "roundrobin_17", "title": " Round 17", "name": " Round 17" },
  { "value": "roundrobin_18", "title": " Round 18", "name": " Round 18" },
  { "value": "finals_1", "title": "Finals Round 1", "name": "Finals Round 1" },
  { "value": "finals_2", "title": "Finals Round 2", "name": "Finals Round 2" }
]
```

https://mc-api.dribl.com/api/fixtures?date_range=all&season=LBdDbV4Nb7&date[]=2025-05-14&competition=eRdkY6RNGX&tenant=7MNGJ1QmAz&timezone=Australia%2FHobart
Returns the fixtures;

```json
{
  "data": [
    {
      "type": "fixtures",
      "hash_id": "2KpR9MoPom",
      "attributes": {
        "name": "Metro Football Club All Ages Men 03 Male Southern Championship 1 vs Hobart United Football Club All Ages Men 03 Male Southern Championship 1",
        "date": "2023-03-17T07:00:00.000000Z",
        "round": "R1",
        "full_round": "Round 1",
        "ground_name": "KGV",
        "ground_latitude": -42.8284,
        "ground_longitude": 147.2789,
        "ground_address": null,
        "field_name": "KGV",
        "is_historic_field": false,
        "home_team_name": "Metro Football Club All Ages Men 03 Male Southern Championship 1",
        "home_logo": "https://ocean.dribl.com/f66b1bf8b9594e1faa57f8f6bf084dc6",
        "away_team_name": "Hobart United Football Club All Ages Men 03 Male Southern Championship 1",
        "away_logo": "https://ocean.dribl.com/e2c24b64f75749edbafb6d37417d5518",
        "competition_name": "Southern Championship",
        "league_name": "Southern Championship Reserves",
        "status": "complete",
        "bye_flag": false,
        "is_unstructured": false,
        "league_result_access": "public",
        "home_score": 1,
        "home_score_extra": null,
        "home_score_penalty": null,
        "home_score_half": null,
        "home_score_extra_half": null,
        "away_score": 5,
        "away_score_extra": null,
        "away_score_penalty": null,
        "away_score_half": null,
        "away_score_extra_half": null,
        "allocated_center_referee": true,
        "allocated_assistant_referee_1": true,
        "allocated_assistant_referee_2": true,
        "allocated_fourth_official": false,
        "allocated_game_leader": false,
        "referee_count": 3,
        "enable_referees_allocated": false,
        "match_hash_id": "wNlXOM8xYN",
        "forfeit_team_hash_id": null,
        "home_team_hash_id": "ydo54x7DND",
        "away_team_hash_id": "pN6XoZQbd0"
      }
    }
  ],
  "links": {
    "first": null,
    "last": null,
    "prev": null,
    "next": "https://mc-api.dribl.com/api/fixtures?cursor=eyJzY2hlZHVsZV9ldmVudHMuZGF0ZSI6IjIwMjMtMDQtMDIgMDQ6MzA6MDAiLCJzY2hlZHVsZV9ldmVudHMuaWQiOjE1Nzk4MzIsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0"
  },
  "meta": {
    "path": "https://mc-api.dribl.com/api/fixtures",
    "per_page": 30,
    "next_cursor": "eyJzY2hlZHVsZV9ldmVudHMuZGF0ZSI6IjIwMjMtMDQtMDIgMDQ6MzA6MDAiLCJzY2hlZHVsZV9ldmVudHMuaWQiOjE1Nzk4MzIsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0",
    "prev_cursor": null
  }
}
```

https://mc-api.dribl.com/api/matchcentre-match-members/match/8Nq4gl8z8m/team/ld4OJj2GKW
Returns the match members for a specific match;

```json
[
  {
    "user_hash_id": "jdylOn4PK5",
    "team_hash_id": "ld4OJj2GKW",
    "image": "https://ocean.dribl.com/82bcc0c009d44362b97303f08f6f7d43",
    "first_name": "Jane",
    "last_name": "Doe",
    "role_slug": "player",
    "jersey": "9",
    "available": true,
    "starting": false,
    "borrowed": 1,
    "playing": true,
    "is_captain": false,
    "is_goalkeeper": false,
    "staff_role": null,
    "field_role": null,
    "field_role_slug": null,
    "field_role_group": null,
    "votes": 2,
    "has_subs": false,
    "in_subs": [],
    "out_subs": [],
    "has_goals": true,
    "goals": [
      {
        "minute": "38",
        "own_goal": false,
        "penalty_kick": false,
        "game_section": "ft-first-half"
      },
      {
        "minute": "44",
        "own_goal": false,
        "penalty_kick": false,
        "game_section": "ft-first-half"
      },
      {
        "minute": "48",
        "own_goal": false,
        "penalty_kick": false,
        "game_section": "ft-second-half"
      }
    ],
    "has_cards": false,
    "cards": [],
    "has_ban": false,
    "formation_field_position": null,
    "formation_type": null,
    "formation_team_type": null
  }
]
```

https://mc-api.dribl.com/api/list/clubs?disable_paging=true&tenant=7MNGJ1QmAz
Returns the list of clubs;

```json
[
  {
    "type": "clubs",
    "id": "bam1BJqNwX",
    "attributes": {
      "name": "University of Tasmania Football Club",
      "slug": null,
      "image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7",
      "alt_image": null,
      "phone": null,
      "email": "utas.soccer@gmail.com",
      "email_address": null,
      "url": null,
      "color": null,
      "accent": null,
      "address": {
        "address_line_1": "Olinda Grove Sports Ground",
        "address_line_2": null,
        "city": "Mt. Nelson",
        "state": "TAS",
        "country": "AUS",
        "postcode": "7007"
      },
      "socials": [
        {
          "name": "facebook",
          "value": "facebook.com/TasmanianUniversitySoccerClub"
        }
      ],
      "grounds": null
    },
    "links": {
      "self": {
        "href": "https://mc-api.dribl.com/api/clubs/bam1BJqNwX"
      }
    }
  }
]
```

https://mc-api.dribl.com/api/memberprofile/jdylOn4PK5?tenant=7MNGJ1QmAz&season=OVdzZ6ZdGr
Returns the member profile for a specific player

```json
{
  "data": {
    "type": "members",
    "hash_id": "jdylOn4PK5",
    "attributes": {
      "first_name": "Jane",
      "last_name": "Doe",
      "image": "https://ocean.dribl.com/82bcc0c009d44362b97303f08f6f7d43",
      "player_clubs": [
        {
          "hash_id": "bam1BJqNwX",
          "name": "University of Tasmania Football Club",
          "image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7",
          "team_info": [],
          "color": "#ffffff",
          "accent": "#1caf9a"
        }
      ],
      "coach_clubs": [],
      "club_color": "#ffffff",
      "club_accent": "#1caf9a",
      "age": 27,
      "team_info": [],
      "nationality": "Australian",
      "is_captain": null,
      "is_goalkeeper": null
    }
  }
}
```

https://mc-api.dribl.com/api/memberprofile-careers/member/jdylOn4PK5/tenant/7MNGJ1QmAz?member=jdylOn4PK5&season=OVdzZ6ZdGr
Returns the career stats

```json
{
  "data": [
    {
      "season_name": "Winter 2023",
      "is_current": false,
      "season_hash_id": "LBdDbV4Nb7",
      "club_names": ["University of Tasmania Football Club"],
      "club_images": [
        "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7"
      ],
      "clubs": [
        {
          "name": "University of Tasmania Football Club",
          "image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7"
        }
      ],
      "comp_names": [
        "Southern Social League Social Women's League Division 1",
        "Southern Championship Southern Championship Women",
        "Statewide Cup Women's Statewide Cup",
        "Southern Social League Social Women's League 1 Cup"
      ],
      "leagues": [
        {
          "league_name": "Social Women's League Division 1",
          "comp_name": "Southern Social League"
        },
        {
          "league_name": "Southern Championship Women",
          "comp_name": "Southern Championship"
        },
        {
          "league_name": "Women's Statewide Cup",
          "comp_name": "Statewide Cup"
        },
        {
          "league_name": "Social Women's League 1 Cup",
          "comp_name": "Southern Social League"
        }
      ],
      "played": 24,
      "started": 17,
      "minutes": 1530,
      "goals": 12,
      "yellow_cards": 0,
      "red_cards": 0,
      "td_cards": 0,
      "votes": 0,
      "team_ids": ["PmjBGeykmZ", "RmwWg9p4mE", "JmXJ3lzzKn"],
      "team_names": [
        "University of Tasmania Football Club All Ages Women 03 Female Southern Womens Division 1",
        "University of Tasmania Football Club All Ages Women 02 Female Womens Championship",
        "University of Tasmania Football Club All Ages Women 02 Female Southern Championship Women"
      ]
    },
    {
      "season_name": "Winter 2024",
      "is_current": false,
      "season_hash_id": "kemAnD1NB7",
      "club_names": ["University of Tasmania Football Club"],
      "club_images": [
        "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7"
      ],
      "clubs": [
        {
          "name": "University of Tasmania Football Club",
          "image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7"
        }
      ],
      "comp_names": [
        "Southern Championship Southern Championship Women",
        "Southern Social League Social League 1 Womens",
        "Statewide Cup Women's Statewide Cup"
      ],
      "leagues": [
        {
          "league_name": "Southern Championship Women",
          "comp_name": "Southern Championship"
        },
        {
          "league_name": "Social League 1 Womens",
          "comp_name": "Southern Social League"
        },
        { "league_name": "Women's Statewide Cup", "comp_name": "Statewide Cup" }
      ],
      "played": 20,
      "started": 16,
      "minutes": 1464,
      "goals": 11,
      "yellow_cards": 0,
      "red_cards": 0,
      "td_cards": 0,
      "votes": 0,
      "team_ids": ["am1qlqDXmw", "MNGopLWENA"],
      "team_names": [
        "University of Tasmania Football Club Championship Women Championship Women Female",
        "University of Tasmania Football Club Social League Women League 1 Female"
      ]
    },
    {
      "season_name": "2025",
      "is_current": true,
      "season_hash_id": "OVdzZ6ZdGr",
      "club_names": ["University of Tasmania Football Club"],
      "club_images": [
        "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7"
      ],
      "clubs": [
        {
          "name": "University of Tasmania Football Club",
          "image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7"
        }
      ],
      "comp_names": [
        "Southern Championship Southern Championship Women",
        "Southern Social League Social League 1 Womens",
        "Statewide Cup Women's Statewide Cup"
      ],
      "leagues": [
        {
          "league_name": "Southern Championship Women",
          "comp_name": "Southern Championship"
        },
        {
          "league_name": "Social League 1 Womens",
          "comp_name": "Southern Social League"
        },
        { "league_name": "Women's Statewide Cup", "comp_name": "Statewide Cup" }
      ],
      "played": 21,
      "started": 14,
      "minutes": 1194,
      "goals": 17,
      "yellow_cards": 0,
      "red_cards": 0,
      "td_cards": 0,
      "votes": 0,
      "team_ids": ["ld4OJj2GKW", "pmvzkg7ymv"],
      "team_names": [
        "University of Tasmania Football Club Championship Women Championship Women Female",
        "University of Tasmania Football Club Social League Women League 1 Female"
      ]
    }
  ]
}
```

https://mc-api.dribl.com/api/memberprofile-matches/member/jdylOn4PK5?member=jdylOn4PK5&tenant=7MNGJ1QmAz&date_range=default&m=jdylOn4PK5&season=OVdzZ6ZdGr&competition=V8dnjVvdwL&league=6lNbBZvENx

Returns the match history for a specific player

```json
{
  "data": [
    {
      "type": "members",
      "hash_id": "8NObnrR1bm",
      "attributes": {
        "date": "2025-03-14T08:00:00.000000Z",
        "round": "R1",
        "full_round": "Round 1",
        "away_team_name": "University of Tasmania Football Club Championship Women Championship Women Female",
        "away_logo": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7",
        "away_club_name": "University of Tasmania Football Club",
        "home_team_name": "Taroona Football Club Championship Women Championship Women Female",
        "home_logo": "https://ocean.dribl.com/ad1472e73dd745b28a9eea61c4158929",
        "home_club_name": "Taroona Football Club",
        "comp_name": "Southern Championship",
        "league_name": "Southern Championship Women",
        "side": "away",
        "home_score": 0,
        "away_score": 9,
        "score_type": "FT",
        "goals": 0,
        "td_card_count": 0,
        "yellow_card_count": 0,
        "red_card_count": 0,
        "votes": null,
        "umts_home_team_name": null,
        "umts_away_team_name": null,
        "umts_home_club_name": null,
        "umts_away_club_name": null,
        "umts_home_logo": null,
        "umts_away_logo": null,
        "umts_field_name": null,
        "umts_ground_name": null,
        "available": true,
        "played": true,
        "started": false,
        "is_captain": false,
        "is_goalkeeper": false,
        "minutes": 0,
        "match_hash_id": "am1nvekxZN",
        "home_team_hash_id": "xNxW6XpMmk",
        "away_team_hash_id": "ld4OJj2GKW"
      },
      "counts": [],
      "links": []
    }
  ]
}
```

https://mc-api.dribl.com/api/ladders?date_range=default&season=OVdzZ6ZdGr&competition=V8dnjVvdwL&league=6lNbBZvENx&ladder_type=regular&tenant=7MNGJ1QmAz&require_pools=true
Returns the ladder.

```json
{
  "data": [
    {
      "type": "ladder-entry",
      "id": "emA1BvWgmB",
      "attributes": {
        "team_hash_id": "ld4OJj2GKW",
        "team_name": "University of Tasmania Football Club  Championship Women",
        "season_name": "2025",
        "club_code": "UTC",
        "club_name": "University of Tasmania Football Club",
        "club_logo": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7",
        "points": 36,
        "goals_for": 70,
        "goals_against": 6,
        "goal_difference": 64,
        "played": 12,
        "won": 12,
        "drawn": 0,
        "lost": 0,
        "pen_win": 0,
        "pen_loss": 0,
        "et_win": 0,
        "et_loss": 0,
        "red_cards": 0,
        "yellow_cards": 0,
        "other_cards": 0,
        "temporary_dismissals": 0,
        "seq_no": 8,
        "position": 1,
        "forfeits": 0,
        "points_per_game": "3.00",
        "byes": 0,
        "point_adjustment": 0,
        "pool_name": null,
        "upcoming_matches": [
          {
            "id": "AN06n9xWad",
            "date": "2025-07-13 04:30:00",
            "home_team_hash_id": "RmwwpYZZmE",
            "home_club_name": "Kingborough Lions United Football Club  Championship Women",
            "home_team_name": "Kingborough Lions United Football Club  Championship Women",
            "home_club_image": "https://ocean.dribl.com/4ec1919f22ff4f969f045e40f07a7cb7",
            "match_hash_id": "AN06n9xWad",
            "away_team_hash_id": "ld4OJj2GKW",
            "away_club_name": "University of Tasmania Football Club  Championship Women",
            "away_team_name": "University of Tasmania Football Club  Championship Women",
            "away_club_image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7",
            "round_number": 14,
            "status": "pending",
            "league_result_access": "public",
            "home_score": null,
            "home_score_extra": null,
            "home_score_penalty": null,
            "home_score_half": null,
            "home_score_extra_half": null,
            "away_score": null,
            "away_score_extra": null,
            "away_score_penalty": null,
            "away_score_half": null,
            "away_score_extra_half": null,
            "pub_disp_club_name": "club-name",
            "pub_disp_club_logo": 1,
            "pub_disp_age_group": 0,
            "pub_disp_division": 1,
            "pub_disp_gender": 0,
            "pub_disp_axis": 0,
            "pub_disp_group": 1,
            "bye_flag": false
          }
        ],
        "recent_matches": [
          {
            "id": "8Nq4gl8z8m",
            "date": "2025-07-06 05:30:00",
            "home_team_hash_id": "ld4OJj9DKW",
            "home_club_name": "Glenorchy Knights Football Club  Championship Women",
            "home_team_name": "Glenorchy Knights Football Club  Championship Women",
            "home_club_image": "https://ocean.dribl.com/a21380e1a98142d5bce390ad152267e9",
            "match_hash_id": "8Nq4gl8z8m",
            "away_team_hash_id": "ld4OJj2GKW",
            "away_club_name": "University of Tasmania Football Club  Championship Women",
            "away_team_name": "University of Tasmania Football Club  Championship Women",
            "away_club_image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7",
            "round_number": 13,
            "status": "complete",
            "league_result_access": "public",
            "home_score": 1,
            "home_score_extra": null,
            "home_score_penalty": null,
            "home_score_half": 0,
            "home_score_extra_half": null,
            "away_score": 8,
            "away_score_extra": null,
            "away_score_penalty": null,
            "away_score_half": 4,
            "away_score_extra_half": null,
            "pub_disp_club_name": "club-name",
            "pub_disp_club_logo": 1,
            "pub_disp_age_group": 0,
            "pub_disp_division": 1,
            "pub_disp_gender": 0,
            "pub_disp_axis": 0,
            "pub_disp_group": 1,
            "bye_flag": false
          },
          {
            "id": "zdBvbEp1kd",
            "date": "2025-06-29 04:30:00",
            "home_team_hash_id": "PmrkEvEENo",
            "home_club_name": "New Town White Eagles Soccer Club  Championship Women",
            "home_team_name": "New Town White Eagles Soccer Club  Championship Women",
            "home_club_image": "https://ocean.dribl.com/b50d407efc4b4e3994262a9351455995",
            "match_hash_id": "zdBvbEp1kd",
            "away_team_hash_id": "ld4OJj2GKW",
            "away_club_name": "University of Tasmania Football Club  Championship Women",
            "away_team_name": "University of Tasmania Football Club  Championship Women",
            "away_club_image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7",
            "round_number": 12,
            "status": "complete",
            "league_result_access": "public",
            "home_score": 1,
            "home_score_extra": null,
            "home_score_penalty": null,
            "home_score_half": 1,
            "home_score_extra_half": null,
            "away_score": 2,
            "away_score_extra": null,
            "away_score_penalty": null,
            "away_score_half": 2,
            "away_score_extra_half": null,
            "pub_disp_club_name": "club-name",
            "pub_disp_club_logo": 1,
            "pub_disp_age_group": 0,
            "pub_disp_division": 1,
            "pub_disp_gender": 0,
            "pub_disp_axis": 0,
            "pub_disp_group": 1,
            "bye_flag": false
          },
          {
            "id": "3NPowYVWYm",
            "date": "2025-06-15 04:30:00",
            "home_team_hash_id": "ld4OJj2GKW",
            "home_club_name": "University of Tasmania Football Club  Championship Women",
            "home_team_name": "University of Tasmania Football Club  Championship Women",
            "home_club_image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7",
            "match_hash_id": "3NPowYVWYm",
            "away_team_hash_id": "PmjnAWa5mZ",
            "away_club_name": "Hobart City FC  Championship Women",
            "away_team_name": "Hobart City FC  Championship Women",
            "away_club_image": "https://ocean.dribl.com/4910517ae7ee414c84d06efbd41cc6ca",
            "round_number": 10,
            "status": "complete",
            "league_result_access": "public",
            "home_score": 5,
            "home_score_extra": null,
            "home_score_penalty": null,
            "home_score_half": 3,
            "home_score_extra_half": null,
            "away_score": 0,
            "away_score_extra": null,
            "away_score_penalty": null,
            "away_score_half": 0,
            "away_score_extra_half": null,
            "pub_disp_club_name": "club-name",
            "pub_disp_club_logo": 1,
            "pub_disp_age_group": 0,
            "pub_disp_division": 1,
            "pub_disp_gender": 0,
            "pub_disp_axis": 0,
            "pub_disp_group": 1,
            "bye_flag": false
          },
          {
            "id": "pmvQP9JL5d",
            "date": "2025-06-01 04:30:00",
            "home_team_hash_id": "ld4OJj2GKW",
            "home_club_name": "University of Tasmania Football Club  Championship Women",
            "home_team_name": "University of Tasmania Football Club  Championship Women",
            "home_club_image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7",
            "match_hash_id": "pmvQP9JL5d",
            "away_team_hash_id": "BdD1zrzwmb",
            "away_club_name": "Olympia F.C. Warriors  Championship Women",
            "away_team_name": "Olympia F.C. Warriors  Championship Women",
            "away_club_image": "https://ocean.dribl.com/e6a5b6981a834561a8d150b73fc2d5c3",
            "round_number": 9,
            "status": "complete",
            "league_result_access": "public",
            "home_score": 7,
            "home_score_extra": null,
            "home_score_penalty": null,
            "home_score_half": 7,
            "home_score_extra_half": null,
            "away_score": 0,
            "away_score_extra": null,
            "away_score_penalty": null,
            "away_score_half": 0,
            "away_score_extra_half": null,
            "pub_disp_club_name": "club-name",
            "pub_disp_club_logo": 1,
            "pub_disp_age_group": 0,
            "pub_disp_division": 1,
            "pub_disp_gender": 0,
            "pub_disp_axis": 0,
            "pub_disp_group": 1,
            "bye_flag": false
          },
          {
            "id": "am1nvegeZN",
            "date": "2025-05-25 04:30:00",
            "home_team_hash_id": "ld4OJj2GKW",
            "home_club_name": "University of Tasmania Football Club  Championship Women",
            "home_team_name": "University of Tasmania Football Club  Championship Women",
            "home_club_image": "https://ocean.dribl.com/3e32ea6085b04800ad671187eb8569b7",
            "match_hash_id": "am1nvegeZN",
            "away_team_hash_id": "xNxW6XpMmk",
            "away_club_name": "Taroona Football Club  Championship Women",
            "away_team_name": "Taroona Football Club  Championship Women",
            "away_club_image": "https://ocean.dribl.com/ad1472e73dd745b28a9eea61c4158929",
            "round_number": 8,
            "status": "complete",
            "league_result_access": "public",
            "home_score": 7,
            "home_score_extra": null,
            "home_score_penalty": null,
            "home_score_half": 2,
            "home_score_extra_half": null,
            "away_score": 0,
            "away_score_extra": null,
            "away_score_penalty": null,
            "away_score_half": 0,
            "away_score_extra_half": null,
            "pub_disp_club_name": "club-name",
            "pub_disp_club_logo": 1,
            "pub_disp_age_group": 0,
            "pub_disp_division": 1,
            "pub_disp_gender": 0,
            "pub_disp_axis": 0,
            "pub_disp_group": 1,
            "bye_flag": false
          }
        ]
      },
      "links": {
        "self": {
          "href": "https://mc-api.dribl.com/api/ladders/emA1BvWgmB"
        }
      }
    }
  ],
  "point_adjustments": []
}
```

https://footballtasmania.dribl.com/matchcentre?m=AN06n9xWad
example subdomain.
