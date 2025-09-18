#!/usr/bin/env python3
import os
import csv
import sys
import datetime as dt
import requests
from dotenv import load_dotenv

load_dotenv()

def _gql(token, query, variables):
    response = requests.post(
        'https://api.github.com/graphql',
        json={'query': query, 'variables': variables},
        headers={'Authorization': f'Bearer {token}'},
        timeout=60
    )
    return response.json()

def _get_org_id(token, org):
    query = """
    query($org: String!) {
        organization(login: $org) {
            id
        }
    }
    """
    result = _gql(token, query, {'org': org})
    return result['data']['organization']['id']

def _iter_org_members(token, org):
    query = """
    query($org: String!, $cursor: String) {
        organization(login: $org) {
            membersWithRole(first: 100, after: $cursor) {
                nodes {
                    login
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    }
    """
    cursor = None
    while True:
        result = _gql(token, query, {'org': org, 'cursor': cursor})
        for member in result['data']['organization']['membersWithRole']['nodes']:
            yield member['login']
        
        page_info = result['data']['organization']['membersWithRole']['pageInfo']
        if not page_info['hasNextPage']:
            break
        cursor = page_info['endCursor']

def _member_daily_contribs(token, login, org_id, start, end):
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!, $orgId: ID!) {
        user(login: $login) {
            contributionsCollection(from: $from, to: $to, organizationID: $orgId) {
                contributionCalendar {
                    weeks {
                        contributionDays {
                            date
                            contributionCount
                        }
                    }
                }
            }
        }
    }
    """
    
    from_dt = dt.datetime.combine(start, dt.time.min).isoformat() + 'Z'
    to_dt = dt.datetime.combine(end, dt.time.max).isoformat() + 'Z'
    
    result = _gql(token, query, {
        'login': login,
        'from': from_dt,
        'to': to_dt,
        'orgId': org_id
    })
    
    contributions = {}
    if result['data']['user'] and result['data']['user']['contributionsCollection']:
        for week in result['data']['user']['contributionsCollection']['contributionCalendar']['weeks']:
            for day in week['contributionDays']:
                if day['contributionCount'] > 0:
                    contributions[day['date']] = day['contributionCount']
    
    return contributions

def get_org_commits_by_user(org, start, end, token=None):
    if not token:
        token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_PAT') or os.getenv('github-pat')
    
    org_id = _get_org_id(token, org)
    result = {}
    
    for member in _iter_org_members(token, org):
        contributions = _member_daily_contribs(token, member, org_id, start, end)
        if contributions:
            result[member] = contributions
    
    return result

def main():
    org = os.getenv('GH_ORG', 'MSTR-Projects')
    start = dt.date(2024, 9, 1)
    end = dt.date(2025, 8, 30)
    
    commits_data = get_org_commits_by_user(org, start, end)
    
    writer = csv.writer(sys.stdout)
    writer.writerow(['username', 'date', 'commits'])
    
    for username, dates in commits_data.items():
        for date, commits in dates.items():
            writer.writerow([username, date, commits])

if __name__ == '__main__':
    main()