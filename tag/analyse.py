"""
Try Tag Rugby Match Analyzer
Finds the last time a team won N consecutive matches without conceding a single try.
"""

import re
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Tuple, Optional


def fetch_season_data(season_id: int) -> Optional[str]:
    """Fetch the standings/results page for a given season."""
    url = f"https://trytagrugby.spawtz.com/Leagues/Standings?VenueId=0&LeagueId=745&SeasonId={season_id}&DivisionId=0"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching season {season_id}: {e}")
        return None


def parse_results(html: str) -> List[Dict]:
    """Parse match results from the HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    matches = []
    
    # Find all result rows in the results section
    # Looking for pattern like: "Team A | score1 - score2 | Team B"
    result_tables = soup.find_all('table')
    
    for table in result_tables:
        rows = table.find_all('tr')
        current_date = None
        
        for row in rows:
            cells = row.find_all('td')
            
            # Check if this is a date row
            if len(cells) >= 1:
                date_text = cells[0].get_text(strip=True)
                # Match patterns like "Thursday 08 Jan 2026" or "Thursday 08 January 2026"
                if 'day' in date_text.lower() and any(month in date_text for month in 
                    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                    current_date = date_text
                    continue
            
            # Check if this is a match result row (has 5 cells: time, pitch, team1, score, team2)
            if len(cells) == 5:
                time_text = cells[0].get_text(strip=True)
                pitch_text = cells[1].get_text(strip=True)
                team1_text = cells[2].get_text(strip=True)
                score_text = cells[3].get_text(strip=True)
                team2_text = cells[4].get_text(strip=True)
                
                # Parse the score (format: "X - Y")
                score_match = re.search(r'(\d+)\s*-\s*(\d+)', score_text)
                if score_match and current_date:
                    score1 = int(score_match.group(1))
                    score2 = int(score_match.group(2))
                    
                    # Only include completed matches (not "vs" which indicates future matches)
                    if 'vs' not in score_text.lower():
                        matches.append({
                            'date': current_date,
                            'time': time_text,
                            'pitch': pitch_text,
                            'team1': team1_text,
                            'score1': score1,
                            'team2': team2_text,
                            'score2': score2
                        })
    
    return matches


def is_walkover(score1: int, score2: int) -> bool:
    """Check if a match is a walkover (10-0)."""
    return (score1 == 10 and score2 == 0) or (score1 == 0 and score2 == 10)


def analyze_clean_sheet_streaks(matches: List[Dict], season_id: int) -> List[Dict]:
    """
    Analyze matches to find teams with consecutive wins without conceding a try.
    Returns list of streak records.
    """
    # Group matches by team
    team_results = defaultdict(list)
    
    for match in matches:
        # Skip walkovers
        if is_walkover(match['score1'], match['score2']):
            continue
        
        # Add result to team1
        team_results[match['team1']].append({
            'date': match['date'],
            'opponent': match['team2'],
            'scored': match['score1'],
            'conceded': match['score2'],
            'won': match['score1'] > match['score2'],
            'clean_sheet': match['score2'] == 0
        })
        
        # Add result to team2
        team_results[match['team2']].append({
            'date': match['date'],
            'opponent': match['team1'],
            'scored': match['score2'],
            'conceded': match['score1'],
            'won': match['score2'] > match['score1'],
            'clean_sheet': match['score1'] == 0
        })
    
    # Find streaks for each team
    streaks = []
    
    for team, results in team_results.items():
        # Sort by date (reverse to go from most recent to oldest within a season)
        results_sorted = results
        
        current_streak = 0
        streak_matches = []
        
        for result in results_sorted:
            if result['won'] and result['clean_sheet']:
                current_streak += 1
                streak_matches.append(result)
            else:
                # Streak broken, record it if it's meaningful
                if current_streak > 0:
                    streaks.append({
                        'team': team,
                        'season_id': season_id,
                        'streak_length': current_streak,
                        'matches': streak_matches.copy(),
                        'last_match_date': streak_matches[-1]['date'] if streak_matches else None
                    })
                current_streak = 0
                streak_matches = []
        
        # Don't forget the last streak if it exists
        if current_streak > 0:
            streaks.append({
                'team': team,
                'season_id': season_id,
                'streak_length': current_streak,
                'matches': streak_matches.copy(),
                'last_match_date': streak_matches[-1]['date'] if streak_matches else None
            })
    
    return streaks


def get_season_name(html: str) -> str:
    """Extract season name from the page."""
    soup = BeautifulSoup(html, 'html.parser')
    h3 = soup.find('h3')
    if h3:
        text = h3.get_text(strip=True)
        # Extract text before " - Current Standings" or " - Standings"
        match = re.search(r'(.+?)\s*-\s*(Current\s+)?Standings', text)
        if match:
            return match.group(1).strip()
    return "Unknown Season"


def main(min_season: int = 1, max_season: int = 95, min_streak: int = 1):
    """
    Main function to analyze all seasons.
    
    Args:
        min_season: Minimum season ID to analyze
        max_season: Maximum season ID to analyze  
        min_streak: Minimum streak length to report (default: 1)
    """
    print("Try Tag Rugby - Clean Sheet Streak Analyzer")
    print("=" * 60)
    print("Analyzing seasons to find consecutive wins without conceding a try...")
    print("(Ignoring 10-0 walkovers)")
    print(f"Season range: {min_season} to {max_season}")
    print(f"Minimum streak length to report: {min_streak}")
    print()
    
    all_streaks = []
    
    min_season_id = min_season
    max_season_id = max_season
    
    for season_id in range(max_season_id, min_season_id - 1, -1):
        print(f"Fetching Season {season_id}...", end=" ")
        
        html = fetch_season_data(season_id)
        if not html:
            print("Failed to fetch or empty")
            continue
        
        season_name = get_season_name(html)
        matches = parse_results(html)
        
        if not matches:
            print(f"No matches found ({season_name})")
            continue
        
        print(f"Found {len(matches)} matches ({season_name})")
        
        streaks = analyze_clean_sheet_streaks(matches, season_id)
        
        for streak in streaks:
            streak['season_name'] = season_name
            all_streaks.append(streak)
    
    print()
    print("=" * 60)
    print("RESULTS: Teams with consecutive wins without conceding a try")
    print("=" * 60)
    print()
    
    # Filter by minimum streak length
    all_streaks = [s for s in all_streaks if s['streak_length'] >= min_streak]
    
    # Sort by streak length (descending) and then by season (descending)
    all_streaks.sort(key=lambda x: (x['streak_length'], x['season_id']), reverse=True)
    
    if not all_streaks:
        print("No clean sheet streaks found!")
        return
    
    # Group by streak length
    streak_groups = defaultdict(list)
    for streak in all_streaks:
        streak_groups[streak['streak_length']].append(streak)
    
    for n in sorted(streak_groups.keys(), reverse=True):
        print(f"\n{n} CONSECUTIVE WIN{'S' if n != 1 else ''} WITHOUT CONCEDING A TRY:")
        print("-" * 60)
        
        streaks_of_n = streak_groups[n]
        # Sort by season ID descending (most recent first)
        streaks_of_n.sort(key=lambda x: x['season_id'], reverse=True)
        
        for streak in streaks_of_n:
            print(f"\nTeam: {streak['team']}")
            print(f"Season: {streak['season_name']} (ID: {streak['season_id']})")
            print(f"Matches:")
            for i, match in enumerate(streak['matches'], 1):
                print(f"  {i}. {match['date']}: vs {match['opponent']} "
                      f"(Won {match['scored']}-{match['conceded']})")
            
            # Show last match date
            if streak['last_match_date']:
                print(f"Last match: {streak['last_match_date']}")
    
    print()
    print("=" * 60)
    print("SUMMARY:")
    print(f"Total streaks found: {len(all_streaks)}")
    print(f"Longest streak: {max(streak_groups.keys())} consecutive wins")
    print(f"Most recent long streak (4+): ", end="")
    
    long_streaks = [s for s in all_streaks if s['streak_length'] >= 4]
    if long_streaks:
        long_streaks.sort(key=lambda x: x['season_id'], reverse=True)
        recent = long_streaks[0]
        print(f"{recent['team']} - {recent['streak_length']} wins in {recent['season_name']}")
    else:
        print("None found")
    
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    min_season = 1
    max_season = 95
    min_streak = 1
    
    if len(sys.argv) > 1:
        try:
            if '--help' in sys.argv or '-h' in sys.argv:
                print("Usage: python3 try_tag_analyzer.py [min_season] [max_season] [min_streak]")
                print()
                print("Arguments:")
                print("  min_season  : Minimum season ID to analyze (default: 1)")
                print("  max_season  : Maximum season ID to analyze (default: 95)")
                print("  min_streak  : Minimum streak length to report (default: 1)")
                print()
                print("Examples:")
                print("  python3 try_tag_analyzer.py           # Analyze all seasons, show all streaks")
                print("  python3 try_tag_analyzer.py 90 95     # Analyze seasons 90-95")
                print("  python3 try_tag_analyzer.py 1 95 3    # Show only streaks of 3+ wins")
                sys.exit(0)
            
            if len(sys.argv) >= 2:
                min_season = int(sys.argv[1])
            if len(sys.argv) >= 3:
                max_season = int(sys.argv[2])
            if len(sys.argv) >= 4:
                min_streak = int(sys.argv[3])
        except ValueError:
            print("Error: Arguments must be integers")
            sys.exit(1)
    
    main(min_season, max_season, min_streak)
