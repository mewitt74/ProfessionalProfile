import json
import openpyxl
from datetime import datetime
from collections import defaultdict

# Load the workbook to recalculate
wb = openpyxl.load_workbook('certificates/Resume Submissions.xlsx')

# Get timeline and aggregate by month
ws_timeline = wb['Sheet1']
monthly_data = defaultdict(int)
for row in ws_timeline.iter_rows(min_row=4, values_only=True):
    if row[0] and isinstance(row[0], datetime) and row[1]:
        month_key = row[0].strftime('%b %Y')
        monthly_data[month_key] += int(row[1])

# Sort by date
sorted_months = sorted(monthly_data.items(), key=lambda x: datetime.strptime(x[0], '%b %Y'))
max_count = max([count for _, count in sorted_months]) if sorted_months else 1

# Get positions and companies
ws_data = wb['Sheet2']

# More specific role groupings based on similarity
positions_by_role = {
    'Director Level': [],
    'Technical Program Manager': [],
    'Compliance Program Manager': [],
    'Senior Manager & Principal': [],
    'GRC Manager': [],
    'Security & Risk Manager': [],
    'AI & Governance Specialist': [],
    'Compliance Analyst & Specialist': [],
    'Lead & Head Roles': [],
    'Other Roles': []
}

companies_by_industry = {
    'Cloud & Infrastructure': [],
    'Enterprise Software & SaaS': [],
    'FinTech & Financial Services': [],
    'Security & Compliance': [],
    'Healthcare & Life Sciences': [],
    'E-commerce & Consumer Tech': [],
    'Consulting & Services': [],
    'Emerging Technology': []
}

# Industry mapping
industry_map = {
    'Amazon': 'Cloud & Infrastructure', 'Amazon Prime Air': 'Cloud & Infrastructure', 'Google': 'Cloud & Infrastructure',
    'Microsoft': 'Cloud & Infrastructure', 'CoreWeave': 'Cloud & Infrastructure', 'NVIDIA': 'Cloud & Infrastructure',
    'Oracle': 'Cloud & Infrastructure', 'F5': 'Cloud & Infrastructure',
    'Atlassian': 'Enterprise Software & SaaS', 'Docusign': 'Enterprise Software & SaaS', 'Asana': 'Enterprise Software & SaaS',
    'Hubspot': 'Enterprise Software & SaaS', 'Twilio': 'Enterprise Software & SaaS', 'Avalara': 'Enterprise Software & SaaS',
    'Teradata': 'Enterprise Software & SaaS', 'VeevaSystems': 'Enterprise Software & SaaS', 'insightsoftware': 'Enterprise Software & SaaS',
    'Ncontracts': 'Enterprise Software & SaaS', 'Figma': 'Enterprise Software & SaaS', 'GrafanaLabs': 'Enterprise Software & SaaS',
    'Amplitude': 'Enterprise Software & SaaS', 'Confluent': 'Enterprise Software & SaaS', 'Vercel': 'Enterprise Software & SaaS',
    'FloQast': 'Enterprise Software & SaaS', '6sense(Growth-stageB2BSaaS)': 'Enterprise Software & SaaS', 'Airtable': 'Enterprise Software & SaaS',
    'interface.ai': 'Enterprise Software & SaaS', 'MediaAlpha': 'Enterprise Software & SaaS', 'phData': 'Enterprise Software & SaaS',
    'Kyriba': 'Enterprise Software & SaaS', 'VitalhubCorp': 'Enterprise Software & SaaS',
    'Affirm': 'FinTech & Financial Services', 'Block': 'FinTech & Financial Services', 'Stripe': 'FinTech & Financial Services',
    'Coinbase': 'FinTech & Financial Services', 'Circle': 'FinTech & Financial Services', 'Paxos': 'FinTech & Financial Services',
    'Ripple': 'FinTech & Financial Services', 'AnchorageDigital': 'FinTech & Financial Services', 'GreenDot': 'FinTech & Financial Services',
    'Upstart': 'FinTech & Financial Services', 'Wrapbook': 'FinTech & Financial Services', 'BILL': 'FinTech & Financial Services',
    'BECU': 'FinTech & Financial Services', 'Allstate': 'FinTech & Financial Services', 'Symetra': 'FinTech & Financial Services',
    'CIBC': 'FinTech & Financial Services', 'Blackstone Talent Group': 'FinTech & Financial Services',
    'Evergreen Home Loans': 'FinTech & Financial Services', 'MeridianLink': 'FinTech & Financial Services', 'Experian': 'FinTech & Financial Services',
    'CrowdStrike': 'Security & Compliance', 'Zscaler': 'Security & Compliance', 'Vanta': 'Security & Compliance',
    'SecureCodeWarrior': 'Security & Compliance', 'Zenity': 'Security & Compliance', 'Entrust': 'Security & Compliance',
    'Virtru': 'Security & Compliance', 'Forta': 'Security & Compliance',
    'Milliman(IntelliScriptDivision)': 'Healthcare & Life Sciences', 'IncludedHealth': 'Healthcare & Life Sciences',
    'Baylor Scott & White Health': 'Healthcare & Life Sciences', 'CardinalHealth': 'Healthcare & Life Sciences',
    'BeiGene(BeOne)': 'Healthcare & Life Sciences', 'GlobalCommercialJazzPharma': 'Healthcare & Life Sciences',
    'SwordHealth': 'Healthcare & Life Sciences', 'HealthInTech': 'Healthcare & Life Sciences', 'Aledade': 'Healthcare & Life Sciences',
    'UnileverPrestige': 'Healthcare & Life Sciences', 'PrecisionMedicineGroup': 'Healthcare & Life Sciences',
    'BALTGroup(Balt)': 'Healthcare & Life Sciences', 'Radformation': 'Healthcare & Life Sciences',
    'AirBnB': 'E-commerce & Consumer Tech', 'DoorDash': 'E-commerce & Consumer Tech', 'Zillow': 'E-commerce & Consumer Tech',
    'Expedia Group': 'E-commerce & Consumer Tech', 'SnapChat': 'E-commerce & Consumer Tech', 'Meta': 'E-commerce & Consumer Tech',
    'Nordstrom': 'E-commerce & Consumer Tech', 'Angi': 'E-commerce & Consumer Tech', 'RealPage': 'E-commerce & Consumer Tech',
    'Deloitte': 'Consulting & Services', 'KPMGUS': 'Consulting & Services', 'KornFerry': 'Consulting & Services',
    'WilsonSonsini': 'Consulting & Services', 'HorizontalTalent': 'Consulting & Services', 'CypressHCM': 'Consulting & Services',
    'DecisionPointCorporation': 'Consulting & Services', 'Signify Technology': 'Consulting & Services',
    'IBSS': 'Consulting & Services', 'Polestar Analytics': 'Consulting & Services',
    'D-WaveQuantum': 'Emerging Technology', 'Groq': 'Emerging Technology', 'Perplexity': 'Emerging Technology',
    'Waymo': 'Emerging Technology', 'WingAviation': 'Emerging Technology', 'Phaidra': 'Emerging Technology',
    'Zania': 'Emerging Technology', 'Mozilla': 'Emerging Technology', 'Popl': 'Emerging Technology'
}

unique_companies = set()
unique_positions = set()

for row in ws_data.iter_rows(min_row=4, values_only=True):
    if row[1] and row[2]:
        company = str(row[1]).strip()
        position = str(row[2]).strip()
        pos_lower = position.lower()
        
        unique_companies.add(company)
        unique_positions.add(position)
        
        # More specific categorization
        if any(x in pos_lower for x in ['director of', 'director,', 'director risk', 'director security', 'associate director']):
            positions_by_role['Director Level'].append(position)
        elif 'technical program manager' in pos_lower or 'technical pm' in pos_lower or ('program manager' in pos_lower and 'technical' in pos_lower):
            positions_by_role['Technical Program Manager'].append(position)
        elif any(x in pos_lower for x in ['compliance program', 'pci compliance program', 'program manager, compliance']):
            positions_by_role['Compliance Program Manager'].append(position)
        elif any(x in pos_lower for x in ['senior manager', 'senior director', 'principal', 'sr. manager', 'sr manager']):
            positions_by_role['Senior Manager & Principal'].append(position)
        elif 'grc manager' in pos_lower or 'governance, risk & compliance manager' in pos_lower or 'manager, grc' in pos_lower:
            positions_by_role['GRC Manager'].append(position)
        elif any(x in pos_lower for x in ['security', 'risk manager', 'risk & compliance', 'cybersecurity']) and 'manager' in pos_lower:
            positions_by_role['Security & Risk Manager'].append(position)
        elif any(x in pos_lower for x in ['ai ', 'governance lead', 'governance specialist', 'privacy']):
            positions_by_role['AI & Governance Specialist'].append(position)
        elif any(x in pos_lower for x in ['compliance analyst', 'compliance specialist', 'grc analyst', 'compliance advisor']):
            positions_by_role['Compliance Analyst & Specialist'].append(position)
        elif any(x in pos_lower for x in ['lead', 'head of']):
            positions_by_role['Lead & Head Roles'].append(position)
        else:
            positions_by_role['Other Roles'].append(position)
        
        # Categorize company
        if company in industry_map:
            companies_by_industry[industry_map[company]].append(company)
        else:
            companies_by_industry['Emerging Technology'].append(company)

# Remove duplicates and sort
for role in positions_by_role:
    positions_by_role[role] = sorted(set(positions_by_role[role]))

for ind in companies_by_industry:
    companies_by_industry[ind] = sorted(set(companies_by_industry[ind]))

wb.close()

# Get total submissions from Sheet1 (daily counts)
wb2 = openpyxl.load_workbook('certificates/Resume Submissions.xlsx')
ws_timeline_calc = wb2['Sheet1']
total_submissions = 0
for row in ws_timeline_calc.iter_rows(min_row=4, values_only=True):
    if row[0] and isinstance(row[0], datetime) and row[1]:
        total_submissions += int(row[1])
wb2.close()

# Calculate totals for cards
total_companies = len(unique_companies)
total_title_groups = len([role for role, positions in positions_by_role.items() if positions])

# Generate role data for charts
role_data = []
for role, positions in positions_by_role.items():
    if positions:
        role_data.append({
            'category': role,
            'count': len(positions),
            'positions': positions
        })
role_data.sort(key=lambda x: x['count'], reverse=True)

# Generate company data for heat map
industry_data = []
for industry, companies in companies_by_industry.items():
    if companies:
        industry_data.append({
            'industry': industry,
            'count': len(companies),
            'companies': companies
        })
industry_data.sort(key=lambda x: x['count'], reverse=True)

# Create complete HTML
html = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Search Analytics | Melissa Witte-Spencer</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        * {{
            box-sizing: border-box;
        }}

        .stats-header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 20px 30px;
            border-bottom: 2px solid var(--primary);
        }}

        .stats-header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 600;
            letter-spacing: -0.5px;
        }}

        .stats-content {{
            padding: 20px;
            max-width: 1600px;
            margin: 0 auto;
            background: var(--bg-light);
        }}

        /* Dashboard Grid Layout */
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 16px;
        }}

        .metric-card {{
            background: var(--bg-white);
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid var(--primary);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .metric-value {{
            font-size: 36px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            margin-bottom: 4px;
        }}

        .metric-label {{
            font-size: 11px;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
        }}

        /* Two Column Layout for Main Content */
        .content-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 16px;
        }}

        .panel {{
            background: var(--bg-white);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}

        .panel-header {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .panel-subtitle {{
            font-size: 11px;
            color: var(--text-light);
            font-weight: 500;
        }}

        /* Compact Timeline */
        .timeline-compact {{
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
        }}

        .timeline-item {{
            flex: 1;
            background: var(--bg-light);
            padding: 12px;
            border-radius: 6px;
            text-align: center;
        }}

        .timeline-month {{
            font-size: 11px;
            font-weight: 600;
            color: var(--text-light);
            margin-bottom: 6px;
            text-transform: uppercase;
        }}

        .timeline-number {{
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .timeline-number {{
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        /* Compact Role Bars */
        .role-bar {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
            font-size: 13px;
        }}

        .role-name {{
            min-width: 180px;
            font-weight: 600;
            color: var(--text);
        }}

        .role-viz {{
            flex: 1;
            height: 24px;
            background: var(--bg-light);
            border-radius: 4px;
            position: relative;
            overflow: hidden;
        }}

        .role-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 8px;
            color: white;
            font-size: 11px;
            font-weight: 700;
            min-width: 40px;
        }}

        /* Compact Heat Grid */
        .heat-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }}

        .heat-item {{
            padding: 12px;
            border-radius: 6px;
            border: 1px solid var(--border);
            cursor: pointer;
            transition: all 0.2s;
        }}

        .heat-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        .heat-very-high {{ background: linear-gradient(135deg, rgba(33,128,195,0.25), rgba(50,184,198,0.25)); border-left: 4px solid var(--primary); }}
        .heat-high {{ background: linear-gradient(135deg, rgba(33,128,195,0.18), rgba(50,184,198,0.18)); border-left: 4px solid var(--primary); }}
        .heat-medium {{ background: linear-gradient(135deg, rgba(33,128,195,0.12), rgba(50,184,198,0.12)); border-left: 3px solid var(--accent); }}
        .heat-low {{ background: linear-gradient(135deg, rgba(33,128,195,0.08), rgba(50,184,198,0.08)); border-left: 3px solid var(--accent); }}
        .heat-very-low {{ background: linear-gradient(135deg, rgba(33,128,195,0.04), rgba(50,184,198,0.04)); border-left: 2px solid var(--border); }}

        .heat-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .heat-industry {{
            font-size: 13px;
            font-weight: 600;
            color: var(--text);
        }}

        .heat-number {{
            font-size: 22px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .heat-companies {{
            font-size: 10px;
            color: var(--text-light);
            margin-top: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* Full Width Bottom Panel */
        .full-panel {{
            background: var(--bg-white);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}

        .summary-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            margin-top: 12px;
        }}

        .summary-item {{
            text-align: center;
            padding: 12px;
            background: var(--bg-light);
            border-radius: 6px;
        }}

        .summary-value {{
            font-size: 20px;
            font-weight: 700;
            color: var(--primary);
        }}

        .summary-label {{
            font-size: 10px;
            color: var(--text-light);
            text-transform: uppercase;
            margin-top: 4px;
        }}

        @media (max-width: 1024px) {{
            .dashboard-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .content-grid {{
                grid-template-columns: 1fr;
            }}

            .heat-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (max-width: 768px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr 1fr;
            }}
            
            .timeline-compact {{
                flex-direction: column;
            }}

            .role-name {{
                min-width: 120px;
                font-size: 12px;
            }}
        }}
    </style>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
    
    <!-- Dark Mode Toggle -->
    <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">
        <span class="theme-toggle-icon" id="themeIcon">🌙</span>
        <span id="themeLabel">Dark</span>
    </button>

    <header role="banner">
        <div class="header-content">
            <div>
                <div class="logo"><a href="index.html">Melissa Witte-Spencer</a></div>
                <div class="logo-subtitle">Job Search Analytics & Strategic Targeting</div>
            </div>
        </div>
    </header>

    <!-- Hamburger Navigation -->
    <div class="floating-nav">
        <button class="hamburger-btn" onclick="toggleNavMenu()" aria-label="Navigation Menu" aria-expanded="false">
            <span></span>
            <span></span>
            <span></span>
        </button>
        <div class="nav-menu" id="navMenu" role="navigation">
            <button onclick="navigateTo('index.html')">🏠 Home</button>
            <button onclick="navigateTo('star-stories.html')">⭐ STAR Stories</button>
            <button onclick="navigateTo('iso-matrix.html')">📊 ISO Matrix</button>
            <button onclick="navigateTo('stats.html')" class="active">📈 Stats</button>
        </div>
    </div>

    <div class="stats-header">
        <h1>📊 Executive Job Search Dashboard | GRC Leadership Targeting</h1>
    </div>

    <div class="stats-content" id="main">
        <!-- Key Metrics Row -->
        <div class="dashboard-grid">
            <div class="metric-card">
                <div class="metric-value">{total_submissions}</div>
                <div class="metric-label">Applications</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{total_companies}</div>
                <div class="metric-label">Companies</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{total_title_groups}</div>
                <div class="metric-label">Categories</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">46</div>
                <div class="metric-label">Days Active</div>
            </div>
        </div>

        <!-- Timeline Compact -->
        <div class="panel">
            <div class="panel-header">
                Monthly Activity
                <span class="panel-subtitle">Application volume trend</span>
            </div>
            <div class="timeline-compact">
'''

for month, count in sorted_months:
    html += f'''                <div class="timeline-item">
                    <div class="timeline-month">{month}</div>
                    <div class="timeline-number">{count}</div>
                </div>
'''

html += '''            </div>
        </div>

        <!-- Two Column Grid -->
        <div class="content-grid">
            <!-- Left: Role Distribution -->
            <div class="panel">
                <div class="panel-header">
                    Role Category Distribution
                    <span class="panel-subtitle">{total_submissions} total positions</span>
                </div>
'''

for item in role_data[:10]:  # Top 10
    role = item['category']
    count = item['count']
    width = int((count / max([r['count'] for r in role_data])) * 100)
    
    html += f'''                <div class="role-bar">
                    <div class="role-name">{role}</div>
                    <div class="role-viz">
                        <div class="role-fill" style="width: {width}%;">{count}</div>
                    </div>
                </div>
'''

html += '''            </div>

            <!-- Right: Industry Heat Map -->
            <div class="panel">
                <div class="panel-header">
                    Industry Coverage Map
                    <span class="panel-subtitle">{total_companies} companies across 8 sectors</span>
                </div>
                <div class="heat-grid">
'''

for item in industry_data:
    industry = item['industry']
    count = item['count']
    companies = item['companies']
    
    # Determine intensity
    if count >= 20:
        intensity_class = 'heat-very-high'
    elif count >= 15:
        intensity_class = 'heat-high'
    elif count >= 10:
        intensity_class = 'heat-medium'
    elif count >= 5:
        intensity_class = 'heat-low'
    else:
        intensity_class = 'heat-very-low'
    
    html += f'''                    <div class="heat-item {intensity_class}" title="{', '.join(companies[:5])}...">
                        <div class="heat-row">
                            <div class="heat-industry">{industry}</div>
                            <div class="heat-number">{count}</div>
                        </div>
                        <div class="heat-companies">{count} companies targeted</div>
                    </div>
'''

html += f'''                </div>
            </div>
        </div>

        <!-- Bottom Summary Panel -->
        <div class="full-panel">
            <div class="panel-header">Strategic Focus Summary</div>
            <div class="summary-stats">
                <div class="summary-item">
                    <div class="summary-value">{int((total_submissions/46)*7)}</div>
                    <div class="summary-label">Weekly Avg</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{int((total_companies/total_submissions)*100)}%</div>
                    <div class="summary-label">Company Coverage</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{industry_data[0]['industry'].split()[0]}</div>
                    <div class="summary-label">Top Industry</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{role_data[0]['category'].split()[0]}</div>
                    <div class="summary-label">Top Category</div>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 Melissa Witte-Spencer | Strategic GRC Leadership</p>
    </footer>

    <script>
        function toggleTheme() {{
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            html.setAttribute('data-theme', newTheme);
            
            const icon = document.getElementById('themeIcon');
            const label = document.getElementById('themeLabel');
            if (newTheme === 'dark') {{
                icon.textContent = '☀️';
                label.textContent = 'Light';
            }} else {{
                icon.textContent = '🌙';
                label.textContent = 'Dark';
            }}
            
            localStorage.setItem('theme', newTheme);
        }}

        function toggleNavMenu() {{
            const menu = document.getElementById('navMenu');
            const hamburger = document.querySelector('.hamburger-btn');
            menu.classList.toggle('active');
            hamburger.classList.toggle('active');
        }}

        function navigateTo(page) {{
            const menu = document.getElementById('navMenu');
            menu.classList.remove('active');
            document.querySelector('.hamburger-btn').classList.remove('active');
            setTimeout(() => {{
                window.location.href = page;
            }}, 100);
        }}

        // Apply saved theme on load
        document.addEventListener('DOMContentLoaded', () => {{
            const savedTheme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', savedTheme);
            const icon = document.getElementById('themeIcon');
            const label = document.getElementById('themeLabel');
            if (savedTheme === 'dark') {{
                icon.textContent = '☀️';
                label.textContent = 'Light';
            }}
        }});
    </script>
</body>
</html>
'''

# Write the file
with open('stats.html', 'w') as f:
    f.write(html)

print(f"✅ Generated optimized stats.html")
print(f"   Total Submissions: {total_submissions}")
print(f"   Companies: {total_companies}")
print(f"   Title Categories: {total_title_groups}")
print(f"   Months: {len(sorted_months)}")
