# KPIs and Experimentation - Spotify Analysis

## Product Choice: Spotify

I chose Spotify because it's a service I've been using for 4 years and I'm a big music fan who cannot live without music. When I first started using music streaming apps, Apple Music and Spotify were the two biggest options. As an Android user, Spotify was my default choice, but I would have chosen it anyway because most of my friends use it, making it easier to connect with my network. Spotify's UI is more pleasing to the eyes and it has better music recommendations than Apple Music. I've discovered so many good songs through their recommendation systems. They also thrill me every time they release the end-of-year music recap. Now I've also discovered YouTube Music and I like it as well since it has a lot of older and international songs. YouTube is also really good while partnering with other services such as phone carrier Google Fi and Spectrum. Spotify so far only has student plan and Hulu promotion. In my opinion, Spotify might face market share loss to YouTube Music in the future. For this reason, I'm going to propose 3 experiments to keep users interested in Spotify and loyal to the platform.

## My User Journey

### Initial Discovery Phase (2019-2020)
- **How I discovered it**: As an Android user, Spotify was the natural choice for music streaming
- **First impression**: Clean UI, excellent music discovery features, and great social integration
- **Key moments**: 
  - Discovering personalized playlists (Discover Weekly, Release Radar)
  - Connecting with friends and seeing what they're listening to
  - First end-of-year music recap experience
- **What made me stay**: Superior recommendation algorithms and social features

### Regular Usage Phase (2020-2022)
- **Daily integration**: Music became part of my daily routine (commute, workouts, work)
- **Engagement growth**:
  - Active playlist curation
  - Following friends and artists
  - Sharing music discoveries
- **Key features discovered**: 
  - Podcast integration
  - Collaborative playlists
  - Cross-device sync
  - Student plan benefits

### Mature Usage Phase (2022-Present)
- **Current usage**: 2-3 hours daily, across multiple devices
- **Advanced features**:
  - AI-powered recommendations
  - Voice commands
  - Integration with smart home devices
- **Social engagement**: 
  - Following artists and friends
  - Participating in Spotify Wrapped campaigns
  - Sharing listening activity on social media
- **Platform loyalty**: High switching costs due to playlist curation and listening history

## Three Proposed Experiments

### Experiment 1: Spotify's Gym Combo vs. Hulu Deal - A Revenue Sign-Up Experiment

**Objective**: Users love combo deals, therefore Spotify is launching some deals to lure perspective users to sign up. Currently, Spotify has a deal with Hulu. However, that is not a good combo. Since people who go to the gym usually listen to beats, Spotify offers a discounted deal for Spotify Premium and Blink monthly membership. The goal is to see if the Blink combo performs better than the Hulu one in terms of sign-up revenue.

**Hypothesis**: The Blink combo will perform better than the Hulu combo in terms of sign-up revenue due to better alignment with user interests and lifestyle.

**Test Design**:
- **Control Group (50%)**: Current Hulu + Spotify Premium combo
- **Treatment Group (50%)**: New Blink Fitness + Spotify Premium combo

**Leading Metrics**:
- Number of users who sign up after launching the Blink combo
- Click-through rate on combo advertisements
- Time spent viewing combo deal pages

**Lagging Metrics**:
- Increase in sign-up sales
- Revenue per user (RPU)
- Customer lifetime value (CLV)
- Retention rate of combo subscribers

**Expected Impact**: 25% increase in sign-up rates and 15% improvement in revenue per user.

### Experiment 2: Friend Podcast Listening and User Engagement Tracking

**Objective**: Personally, I am curious about what podcasts my friends are listening to and I wish there was a podcast viewing feature. I think it could affect podcast listeners' engagement. The goal is to determine whether allowing users to view what podcasts their friends are listening to positively impacts user engagement with podcasts on the platform.

**Hypothesis**: Social discovery of podcasts will increase user engagement and time spent listening to podcasts.

**Test Design**:
- **Control Group (50%)**: Current podcast experience without social features
- **Treatment Group (50%)**: Enhanced podcast experience with friend activity feed

**Leading Metrics**:
- Frequency of users checking the social podcast feature
- Time spent browsing friend podcast activity
- Click-through rate on friend-recommended podcasts

**Lagging Metrics**:
- Percentage of users who continue to use the platform and engage with podcasts
- Total podcast listening time
- Number of podcasts followed
- Podcast completion rates

**Expected Impact**: 30% increase in podcast engagement and 20% more time spent listening to podcasts.

### Experiment 3: Changing Sign-Up Ads to Enhance User Engagement

**Objective**: To determine whether changing the sign-up ad from "Try 3 months free" to "Your friend is listening to this song, wanna hear it" positively impacts user sign-up rates and engagement on the platform.

**Hypothesis**: Social proof and curiosity-driven messaging will be more effective than traditional free trial offers.

**Test Design**:
- **Control Group (50%)**: "Try 3 months free" advertisement
- **Treatment Group (50%)**: "Your friend is listening to this song, wanna hear it" advertisement

**Leading Metrics**:
- Amount of time users spend on Spotify after signing up
- Click-through rate on sign-up advertisements
- Social sharing of the advertisement

**Lagging Metrics**:
- Percentage of users who convert from free to premium subscribers
- User retention rate after sign-up
- Average session length
- Premium conversion rate

**Expected Impact**: 20% increase in sign-up rates and 15% improvement in premium conversion.

## Tableau Visualization

To support the analysis and demonstrate the expected impact of these experiments, I've created a comprehensive Tableau dashboard that visualizes:

### Dashboard Components:
1. **Experiment Overview**: Allocation percentages and expected impacts for each test group
2. **Performance Tracking**: Week-over-week metrics showing leading and lagging indicators
3. **Comparative Analysis**: Side-by-side comparison of control vs treatment groups
4. **Revenue Impact**: Projected revenue per user across different experiments

### Key Visualizations:
- **Time Series Charts**: Showing metric progression over 4 weeks
- **Bar Charts**: Comparing performance across experiment groups
- **Heat Maps**: Highlighting the best performing variants
- **Scatter Plots**: Correlation between leading and lagging metrics

### Tableau Public Link:
[Tableau Dashboard - Spotify Experimentation Analysis](https://public.tableau.com/app/profile/murilo.biss/viz/5-kpis-experimentation/RevenuePerUserbyGroup#1)

*Note: The dashboard uses simulated data based on realistic expectations for each experiment variant.*

## Implementation Considerations

### Technical Requirements
- A/B testing infrastructure
- Real-time data processing capabilities
- User segmentation tools
- Analytics and monitoring systems

### Success Criteria
- Statistical significance (p < 0.05)
- Minimum detectable effect size of 10%
- Test duration of 4-6 weeks
- Sample size of at least 10,000 users per variant

### Risk Mitigation
- Gradual rollout with monitoring
- Fallback mechanisms for failed experiments
- User feedback collection during testing
- Regular review of experiment performance

## Conclusion

These experiments target different aspects of the Spotify experience: revenue optimization through strategic partnerships, social engagement enhancement, and user acquisition through improved messaging. Each experiment is designed to address specific challenges Spotify faces in the competitive music streaming market, particularly against YouTube Music.

The combination of leading and lagging metrics ensures we can quickly identify promising changes while measuring long-term business impact. The Tableau visualization provides a comprehensive view of how these experiments would perform, helping stakeholders understand the potential impact and make data-driven decisions about which experiments to prioritize.

The key insight is that Spotify needs to leverage its social advantages and create more compelling value propositions to maintain its market position against emerging competitors like YouTube Music.
