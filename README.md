# SteamViz - Exploring Game Trends

## Description
SteamViz is a transformative gaming analytics and data visualization tool that enhances game discovery and provides deep insights into market trends. Developed for the DATA 511 Data Visualization course, SteamViz harnesses data from the Steam API to deliver actionable intelligence on game popularity, revenue, player engagement, and hardware compatibility. The project processes large datasets—including timeseries data for over 100 games (with around 90,000 rows each) and an overall game overview comprising 97,000+ games—ensuring robust and comprehensive visual analysis.

Explore the interactive dashboard here: [SteamViz Tableau](https://tinyurl.com/SteamViz)  

## Key Features
- **Game Explorer Dashboard:**  
  Filters and displays games based on detailed PC specifications (CPU, GPU, OS, RAM, and storage). A dynamic ranking system uses calculated fields and parameters to assess compatibility, ensuring that only games that match a user's hardware are shown. A 'Match Filter' employs a FIXED Level of Detail (LOD) expression to tag games as "Match" when they meet the selected criteria.

- **Game-Specific Dashboard:**  
  Provides in-depth analysis for individual games, including detailed descriptions, genre classifications, pricing, lifetime sales, and player sentiment. These dashboards offer analytical charts that reveal engagement trends and revenue distributions, helping users make informed decisions.

- **Gaming Trends Visualization:**  
  Presents dynamic visuals such as treemaps, bar charts, and line graphs to illustrate trends in game popularity, revenue by genre, and median playtime. Interactive elements, including an animated Release Year slider, allow users to explore historical and forecasted data (e.g., downloads and playtime predictions for 2022–2024).

- **User Behavior Analysis:**  
  Delivers insights into download patterns and player preferences (e.g., free vs. paid games) by leveraging scatter plots and horizontal bar charts. These visuals incorporate calculated fields to quantify engagement ratios and highlight key metrics like median playtime per download.

## Technologies Used
- **Data Acquisition & Processing:**  
  - Steam API for collecting detailed game data  
  - Python scripts to automate data extraction, cleaning, parsing (using regular expressions), and categorization  
  - Aggregation of raw timeseries data into monthly averages, stored in Excel for subsequent Tableau integration

- **Data Visualization:**  
  - Tableau for developing interactive dashboards with dynamic filters and parameterized views  
  - Calculated fields and FIXED LOD expressions to create custom rankings and match filters based on user inputs

- **Design & User-Centered Approach:**  
  - Iterative design informed by guerrilla usability testing, leading to refined visual hierarchies, enhanced tooltips, and interactive features
