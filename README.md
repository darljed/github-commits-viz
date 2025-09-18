# GitHub Organization Commits Extractor & Visualizer

A Python script that fetches commit data for all members of a GitHub organization and exports it to CSV format, plus an HTML visualization tool that displays the data as a GitHub-style commits heatmap.

## Setup

### Prerequisites
- Python 3.6+
- GitHub Personal Access Token (PAT) with organization read permissions
- Modern web browser for visualization

### Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install requests python-dotenv
```

3. Create a `.env` file in the project root:
```
GH_TOKEN=your_github_token_here
GH_ORG=your_organization_name
```

## Usage

### 1. Generate CSV Data
Run the script to generate CSV output:
```bash
python commits_by_user.py > commits_by_user.csv
```

### 2. Visualize Data
Open `commits_heatmap.html` in your web browser to view the interactive heatmap.

### Output Format
CSV with columns: `username,date,commits`
```csv
username,date,commits
john_doe,2024-01-15,3
jane_smith,2024-01-16,5
```

## Functions Documentation

### `_gql(token, query, variables)`
Executes GraphQL queries against GitHub API.
- **Parameters**: GitHub token, GraphQL query string, query variables
- **Returns**: JSON response from GitHub API

### `_get_org_id(token, org)`
Retrieves the internal ID for a GitHub organization.
- **Parameters**: GitHub token, organization name
- **Returns**: Organization ID string

### `_iter_org_members(token, org)`
Generator that yields all organization members with pagination.
- **Parameters**: GitHub token, organization name  
- **Yields**: Member login names

### `_member_daily_contribs(token, login, org_id, start, end)`
Fetches daily contribution counts for a specific user within date range.
- **Parameters**: GitHub token, username, org ID, start date, end date
- **Returns**: Dictionary of {date: contribution_count}

### `get_org_commits_by_user(org, start, end, token=None)`
Main function that orchestrates data collection for all organization members.
- **Parameters**: Organization name, start date, end date, optional token
- **Returns**: Dictionary of user contributions

## Limitations

### GitHub API Constraints
- **Rate Limits**: 5,000 GraphQL points per hour
- **Time Range**: Only last 12 months of contribution data available
- **Data Granularity**: Daily contribution counts (not individual commits)
- **Scope**: Only contributions to organization repositories

### Script Limitations
- Large organizations may hit rate limits
- No automatic rate limit handling
- Cannot retrieve historical data beyond 12 months

### Visualization Requirements
- Requires `commits_by_user.csv` file in the same directory
- Modern web browser with JavaScript enabled
- Local file access (some browsers may require serving via HTTP for CSV loading)

## Visualization Features

### Interactive Heatmap (`commits_heatmap.html`)
- **GitHub-style heatmap**: Displays commits data with familiar green intensity colors
- **Individual/Combined views**: Toggle between per-user and organization-wide views
- **Dark/Light themes**: Switch between GitHub's dark and light color schemes
- **Month/weekday labels**: Clear time reference labels for easy navigation
- **Download functionality**: Export visualizations as PNG images
- **Hover tooltips**: View exact commit counts and dates

### Usage Instructions
1. Ensure `commits_by_user.csv` is in the same directory as the HTML file
2. Open `commits_heatmap.html` in your web browser
3. Use the toggle buttons to switch between:
   - **Individual Users**: Shows each user's commits separately
   - **Combined View**: Shows organization-wide commits aggregated by date
   - **Theme**: Switch between dark and light themes
4. Click "Download as PNG" to save the current view as an image

### Visualization Details
- **Commit intensity levels**: 0 (no commits), 1-3, 4-6, 7-9, 10+ commits per day
- **Combined view scaling**: Uses higher thresholds (0, 1-5, 6-15, 16-30, 31+ commits)
- **Date range**: Covers September 2024 to August 2025
- **Responsive design**: Works on desktop and mobile browsers

## Recommendations

### For Better Performance
1. **Rate Limiting**: Implement exponential backoff for large organizations
2. **Caching**: Store intermediate results to avoid re-fetching
3. **Parallel Processing**: Use async requests for faster data collection

### For Extended Functionality
1. **Historical Data**: Use GitHub data export or webhook archives for data older than 12 months
2. **Detailed Commits**: Switch to REST API for individual commit details
3. **Repository Filtering**: Add filters for specific repositories or teams

### Alternative Approaches
- **GitHub CLI**: Use `gh api` commands for custom queries
- **GitHub Actions**: Set up automated data collection workflows
- **Third-party Tools**: Consider GitHub analytics platforms for advanced reporting