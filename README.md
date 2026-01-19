# Video Game Market Analysis 

Strategic analysis of global video game sales data to advise game studios on optimal genre and platform targeting for their next IP.

##  Problem Statement
**Challenge:** A game studio needs data-driven guidance on which genre and platform to target for maximum market success.

**Solution:** Comprehensive analysis of 16,598 games across 40 years (1980-2020) revealing regional preferences, platform lifecycles, and publisher success patterns.

##  Key Findings

### Regional Genre Preferences
- **Japan:** RPG dominance (350.29M sales, 52% market share)
- **North America:** Action/Sports preference (861.77M + 670.09M sales)
- **Critical Insight:** 2.2x higher RPG preference in Japan vs NA

### Publisher Hit Rates
- **Nintendo:** 2.56M average sales per game (highest efficiency)
- **Quality over quantity** approach yields better results
- Top publishers maintain consistent performance across platforms

### Platform Lifecycle Patterns
- **PS3:** Peak 2011-2012, then decline
- **PS4:** Growth phase 2013+
- **Timing matters:** Launch during platform growth phase for maximum reach

## Strategic Recommendation

### **Action-RPG Hybrid for PS4/Xbox One**
- **Target Markets:** Japan + North America (70%+ combined market coverage)
- **Genre Strategy:** Blend Action (NA preference) with RPG elements (JP preference)
- **Platform Focus:** Current-gen consoles during growth/maturity phase
- **Expected Sales:** 2.0-3.5M units based on hybrid genre performance

##  Project Structure

```
├── analysis.py          # Core data analysis and visualizations
├── dashboard.py         # Interactive Plotly dashboard
├── presentation.md      # Executive presentation slides
├── recommendations.md   # Detailed strategic recommendations
├── *.png               # Generated visualization charts
└── vgsales.csv         # Dataset (excluded from git)
```

##  Technologies Used
- **Python:** pandas, matplotlib, seaborn, plotly
- **Data Visualization:** Interactive charts and static plots
- **Analysis:** Statistical analysis, trend identification, market segmentation

##  Business Impact
- **Risk Mitigation:** Platform lifecycle analysis prevents poor timing decisions
- **Market Optimization:** Regional preference data maximizes target audience reach
- **Quality Benchmarking:** Publisher hit rate analysis guides development standards
- **Revenue Projection:** Data-driven sales forecasting for investment decisions

##  Usage
1. Run `python analysis.py` for comprehensive market analysis
2. Run `python dashboard.py` for interactive visualizations
3. Review `presentation.md` for executive summary
4. Check `recommendations.md` for detailed strategic guidance

**Bottom Line:** Action-RPG hybrid targeting JP+NA markets on current-gen platforms = optimal ROI strategy.