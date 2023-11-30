# Project Overview

Our project is an in-depth analysis of the cannabis industry, focusing primarily on sentiment analysis and the distribution of dispensaries across various regions. Utilizing Python, specifically libraries like Pandas and Plotly, we've conducted a multi-faceted examination of the burgeoning cannabis market.

## Data Sources and Preparation

The project leverages several key data sources:

- **Tweet Sentiment Analysis**: We've collected and analyzed tweets related to cannabis to gauge public sentiment. Using advanced NLP techniques, we categorized these sentiments as positive, negative, or neutral.
- **Dispensary Data**: We compiled a comprehensive dataset of cannabis dispensaries, focusing on their geographic distribution, growth over time, and other vital metrics.

We ensured data integrity through meticulous cleaning and preprocessing, setting the stage for accurate and meaningful analysis.

## Sentiment Analysis

### Understanding Public Perception

- **Methodology**: Using a BERT model, we analyzed tweets for sentiment, a critical step in understanding public perception.
- **Findings**: The sentiment distribution was visualized using Plotly's bar charts, revealing intriguing trends in public opinion about cannabis.

### Time Series Analysis

- **Trends Over Time**: We examined how sentiments evolved, employing Plotly's `px.line` for temporal analysis. This time series analysis illuminated shifts in public opinion, correlating them with major industry events or legislative changes.

## Geographical Analysis

### Dispensary Distribution

- **Overview**: The spatial distribution of dispensaries is crucial for understanding market saturation and potential growth areas.
- **Visualization**: Using Plotly's choropleth maps, we portrayed dispensary density across different regions. This geographical analysis helps in identifying areas with market potential and those that are already saturated.

### County-Level Analysis

- **Focus**: We delved into county-level data, offering a more granular view of dispensary distribution.
- **Insights**: This analysis highlighted disparities in dispensary accessibility, which could have significant implications for market strategies and policy-making.

## Market Trends and License Issuance

- **Growth Over Time**: Analyzing the yearly trend in license issuance provided insights into the market's growth trajectory.
- **Visualization Technique**: Employing Plotly's `px.bar`, we created a bar chart to depict these trends, offering a clear visual representation of the industry's expansion.

## Integrating Plotly and Markdown

To enhance the comprehensibility and impact of our findings, we integrated Plotly visualizations directly within our Markdown documentation. This approach ensures that our narrative is supported by interactive, data-driven visuals, making the insights more engaging and accessible.

## Challenges and Solutions

Throughout the project, we encountered various challenges, including:

- **Data Volume and Variety**: Handling large datasets from diverse sources required efficient data management strategies.
- **Sentiment Analysis Accuracy**: Ensuring the accuracy of sentiment analysis in NLP is inherently challenging, given the nuances of human language.
- **Geographical Data Representation**: Effectively visualizing spatial data demanded careful selection of mapping techniques and color scales.

We addressed these challenges through a combination of technical proficiency, innovative problem-solving, and robust data analysis techniques.

## Conclusion and Future Directions

Our project sheds light on the complex dynamics of the cannabis industry. The integration of sentiment analysis with geographical data provides a holistic view of the market. Future work could include deeper dives into demographic data, predictive modeling for market trends, and exploring the impact of legal changes on public sentiment and market growth.
