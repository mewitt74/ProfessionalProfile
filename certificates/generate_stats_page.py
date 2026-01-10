import json

# Load optimized data
with open('certificates/stats_optimized.json') as f:
    data = json.load(f)

# Generate timeline HTML
timeline_html = ""
for entry in data['timeline']:
    width = int((entry['count'] / data['max_count']) * 100)
    plural = 's' if entry['count'] != 1 else ''
    timeline_html += f'''            <div class="timeline-bar">
                <div class="timeline-date">{entry["display"]}</div>
                <div class="timeline-visual" style="width: {width}%;">
                    <span class="timeline-count">{entry["count"]} app{plural}</span>
                </div>
            </div>
'''

# Generate positions HTML
positions_html = ""
for category, positions in data['positions_by_category'].items():
    if positions:
        positions_html += f'''            <div class="category-section">
                <h3 class="category-title">{category} <span class="count-badge">({len(positions)})</span></h3>
                <div class="titles-grid">
'''
        for pos in positions:
            positions_html += f'                    <div class="title-chip">{pos}</div>\n'
        positions_html += '''                </div>
            </div>

'''

# Generate companies HTML
companies_html = ""
for industry, companies in data['companies_by_industry'].items():
    if companies:
        companies_html += f'''            <div class="industry-section">
                <h3 class="industry-title"><span class="industry-icon">●</span>{industry} <span class="count-badge">({len(companies)})</span></h3>
                <div class="companies-grid">
'''
        for comp in companies:
            companies_html += f'                    <div class="company-chip">{comp}</div>\n'
        companies_html += '''                </div>
            </div>

'''

# Create complete HTML
html = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Search Statistics | Melissa Witte-Spencer</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .stats-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}

        .stats-header h1 {{
            margin: 0 0 12px 0;
            font-size: 32px;
        }}

        .stats-header p {{
            margin: 0;
            font-size: 16px;
            opacity: 0.95;
        }}

        .stats-content {{
            padding: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .key-metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }}

        .metric-card {{
            background: var(--bg-white);
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            border: 2px solid var(--border);
            box-shadow: var(--shadow-sm);
            transition: var(--transition);
        }}

        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-md);
        }}

        .metric-value {{
            font-size: 48px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }}

        .metric-label {{
            font-size: 14px;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }}

        .section-title {{
            font-size: 26px;
            font-weight: 700;
            color: var(--text);
            margin: 50px 0 24px 0;
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 12px;
            border-bottom: 3px solid var(--primary);
        }}

        /* Timeline - Left to Right */
        .timeline-chart {{
            background: var(--bg-white);
            padding: 30px;
            border-radius: 12px;
            border: 2px solid var(--border);
            margin-bottom: 50px;
            overflow-x: auto;
        }}

        .timeline-bar {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 20px;
        }}

        .timeline-date {{
            font-weight: 600;
            color: var(--text);
            font-size: 13px;
            min-width: 80px;
        }}

        .timeline-visual {{
            height: 40px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            padding: 0 16px;
            color: white;
            font-weight: 600;
            font-size: 14px;
            box-shadow: var(--shadow-sm);
            transition: var(--transition);
        }}

        .timeline-visual:hover {{
            transform: scale(1.02);
            box-shadow: var(--shadow-md);
        }}

        .timeline-count {{
            white-space: nowrap;
        }}

        /* Position Titles - Categorized */
        .category-section {{
            margin-bottom: 40px;
        }}

        .category-title {{
            font-size: 18px;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .count-badge {{
            background: var(--primary);
            color: white;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
        }}

        .titles-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 12px;
        }}

        .title-chip {{
            background: var(--bg-light);
            padding: 14px 16px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            color: var(--text);
            border: 1px solid var(--border);
            transition: var(--transition);
            line-height: 1.4;
        }}

        .title-chip:hover {{
            background: linear-gradient(135deg, rgba(33, 128, 195, 0.1) 0%, rgba(50, 184, 198, 0.1) 100%);
            border-color: var(--primary);
            transform: translateX(4px);
        }}

        /* Companies - Grouped by Industry */
        .industry-section {{
            margin-bottom: 40px;
        }}

        .industry-title {{
            font-size: 18px;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .industry-icon {{
            color: var(--accent);
            font-size: 12px;
        }}

        .companies-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 12px;
        }}

        .company-chip {{
            background: var(--bg-light);
            padding: 12px 16px;
            border-radius: 8px;
            text-align: center;
            font-size: 13px;
            font-weight: 500;
            color: var(--text);
            border: 1px solid var(--border);
            transition: var(--transition);
        }}

        .company-chip:hover {{
            background: linear-gradient(135deg, rgba(33, 128, 195, 0.15) 0%, rgba(50, 184, 198, 0.15) 100%);
            border-color: var(--accent);
            transform: translateY(-2px);
            box-shadow: var(--shadow-sm);
        }}

        @media (max-width: 768px) {{
            .titles-grid, .companies-grid {{
                grid-template-columns: 1fr;
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
        <h1>Job Search Activity Dashboard</h1>
        <p>Strategic targeting across high-growth technology companies | GRC Leadership Roles</p>
    </div>

    <div class="stats-content" id="main">
        <!-- Key Metrics -->
        <div class="key-metrics">
            <div class="metric-card">
                <div class="metric-value">113</div>
                <div class="metric-label">Total Applications</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">113</div>
                <div class="metric-label">Companies Targeted</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">110</div>
                <div class="metric-label">Unique Titles</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">46</div>
                <div class="metric-label">Days Active</div>
            </div>
        </div>

        <!-- Application Timeline -->
        <h2 class="section-title">📈 Application Activity Timeline</h2>
        <div class="timeline-chart">
{timeline_html}        </div>

        <!-- Position Titles by Category -->
        <h2 class="section-title">💼 Role Alignment & Strategic Targeting</h2>
{positions_html}
        <!-- Companies by Industry -->
        <h2 class="section-title">🏢 Target Companies by Industry Sector</h2>
{companies_html}
    </div>

    <footer>
        <p>&copy; 2026 Melissa Witte-Spencer. All rights reserved. | Last Updated: January 10, 2026</p>
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

print("✅ Generated optimized stats.html successfully")
