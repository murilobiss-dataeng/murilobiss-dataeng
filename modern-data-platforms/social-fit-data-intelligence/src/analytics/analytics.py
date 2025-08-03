import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List
from loguru import logger

from ..models.models import StudentAnalytics, InstagramAnalytics, CrossPlatformAnalytics

class AnalyticsEngine:
    """Analytics engine for Social FIT data analysis."""
    
    def __init__(self):
        """Initialize analytics engine."""
        pass
    
    def analyze_students(self, students_df: pd.DataFrame) -> StudentAnalytics:
        """Analyze student data and generate insights."""
        try:
            # Basic statistics
            total_students = len(students_df)
            active_students = len(students_df[students_df['active_plan'] == True])
            inactive_students = total_students - active_students
            
            # Plan distribution
            plan_distribution = students_df['plan_type'].value_counts().to_dict()
            
            # Neighborhood distribution
            neighborhood_distribution = students_df['neighborhood'].value_counts().to_dict()
            
            # Gender distribution
            gender_distribution = students_df['gender'].value_counts().to_dict()
            
            # Gympass users
            gympass_users = len(students_df[students_df['gympass'] == True])
            
            # Financial metrics
            average_monthly_value = students_df['monthly_value'].mean()
            total_monthly_revenue = students_df[students_df['active_plan'] == True]['monthly_value'].sum()
            
            return StudentAnalytics(
                total_students=total_students,
                active_students=active_students,
                inactive_students=inactive_students,
                plan_distribution=plan_distribution,
                neighborhood_distribution=neighborhood_distribution,
                gender_distribution=gender_distribution,
                gympass_users=gympass_users,
                average_monthly_value=round(average_monthly_value, 2),
                total_monthly_revenue=round(total_monthly_revenue, 2)
            )
            
        except Exception as e:
            logger.error(f"Error analyzing students data: {e}")
            raise
    
    def analyze_instagram(self, instagram_df: pd.DataFrame) -> InstagramAnalytics:
        """Analyze Instagram data and generate insights."""
        try:
            # Basic metrics
            total_posts = len(instagram_df)
            total_likes = instagram_df['likes'].sum()
            total_comments = instagram_df['comments'].sum()
            total_saves = instagram_df['saves'].sum()
            total_reach = instagram_df['reach'].sum()
            total_profile_visits = instagram_df['profile_visits'].sum()
            total_new_followers = instagram_df['new_followers'].sum()
            
            # Engagement rate
            total_engagement = total_likes + total_comments + total_saves
            average_engagement_rate = total_engagement / total_reach if total_reach > 0 else 0
            
            # Hashtag performance
            hashtag_performance = instagram_df.groupby('main_hashtag').agg({
                'likes': 'mean',
                'comments': 'mean',
                'saves': 'mean',
                'reach': 'mean',
                'engagement_rate': 'mean'
            }).round(2).to_dict('index')
            
            # Daily performance
            daily_performance = instagram_df.groupby('post_date').agg({
                'likes': 'sum',
                'comments': 'sum',
                'saves': 'sum',
                'reach': 'sum',
                'new_followers': 'sum'
            }).to_dict('index')
            
            return InstagramAnalytics(
                total_posts=total_posts,
                total_likes=total_likes,
                total_comments=total_comments,
                total_saves=total_saves,
                total_reach=total_reach,
                total_profile_visits=total_profile_visits,
                total_new_followers=total_new_followers,
                average_engagement_rate=round(average_engagement_rate, 4),
                hashtag_performance=hashtag_performance,
                daily_performance=daily_performance
            )
            
        except Exception as e:
            logger.error(f"Error analyzing Instagram data: {e}")
            raise
    
    def cross_platform_analysis(self, students_df: pd.DataFrame, instagram_df: pd.DataFrame) -> CrossPlatformAnalytics:
        """Perform cross-platform analysis between students and Instagram data."""
        try:
            # Correlation analysis
            # Group Instagram data by date and calculate daily metrics
            daily_instagram = instagram_df.groupby('post_date').agg({
                'likes': 'sum',
                'comments': 'sum',
                'saves': 'sum',
                'reach': 'sum',
                'new_followers': 'sum'
            }).reset_index()
            
            # Group students by enrollment date
            daily_enrollments = students_df.groupby('plan_start_date').size().reset_index(name='enrollments')
            
            # Merge data for correlation analysis
            merged_data = pd.merge(daily_instagram, daily_enrollments, 
                                 left_on='post_date', right_on='plan_start_date', how='outer')
            
            # Calculate correlation
            correlation_score = merged_data['new_followers'].corr(merged_data['enrollments'])
            
            # Engagement to enrollment rate
            total_engagement = daily_instagram['likes'].sum() + daily_instagram['comments'].sum() + daily_instagram['saves'].sum()
            total_enrollments = daily_enrollments['enrollments'].sum()
            engagement_to_enrollment_rate = total_enrollments / total_engagement if total_engagement > 0 else 0
            
            # Top performing content types (by hashtag)
            hashtag_performance = instagram_df.groupby('main_hashtag').agg({
                'engagement_rate': 'mean',
                'new_followers': 'sum'
            }).sort_values('engagement_rate', ascending=False)
            
            top_performing_content_types = hashtag_performance.head(5).index.tolist()
            
            # Optimal posting times (by day of week)
            instagram_df['day_of_week'] = pd.to_datetime(instagram_df['post_date']).dt.day_name()
            optimal_posting_times = instagram_df.groupby('day_of_week')['engagement_rate'].mean().to_dict()
            
            # Geographic insights
            neighborhood_enrollments = students_df['neighborhood'].value_counts().to_dict()
            
            # Revenue impact calculation
            # Estimate revenue impact based on engagement correlation
            estimated_revenue_impact = correlation_score * students_df['monthly_value'].sum() * 0.1  # 10% of correlation
            
            return CrossPlatformAnalytics(
                correlation_score=round(correlation_score, 4) if not pd.isna(correlation_score) else 0,
                engagement_to_enrollment_rate=round(engagement_to_enrollment_rate, 6),
                top_performing_content_types=top_performing_content_types,
                optimal_posting_times=optimal_posting_times,
                geographic_insights=neighborhood_enrollments,
                revenue_impact=round(estimated_revenue_impact, 2)
            )
            
        except Exception as e:
            logger.error(f"Error in cross-platform analysis: {e}")
            raise
    
    def generate_actionable_insights(self, students_analytics: StudentAnalytics, 
                                   instagram_analytics: InstagramAnalytics,
                                   cross_platform_analytics: CrossPlatformAnalytics) -> List[Dict[str, Any]]:
        """Generate actionable insights for Social FIT."""
        insights = []
        
        try:
            # Insight 1: Geographic targeting
            top_neighborhoods = sorted(cross_platform_analytics.geographic_insights.items(), 
                                     key=lambda x: x[1], reverse=True)[:3]
            insights.append({
                'type': 'geographic_targeting',
                'title': 'Focus on High-Converting Neighborhoods',
                'description': f'Top neighborhoods for enrollment: {", ".join([n[0] for n in top_neighborhoods])}',
                'action': 'Create targeted content and ads for these areas',
                'impact': 'High'
            })
            
            # Insight 2: Content optimization
            best_hashtag = max(instagram_analytics.hashtag_performance.items(), 
                             key=lambda x: x[1]['engagement_rate'])
            insights.append({
                'type': 'content_optimization',
                'title': 'Optimize Content Strategy',
                'description': f'Best performing hashtag: {best_hashtag[0]} with {best_hashtag[1]["engagement_rate"]:.2%} engagement',
                'action': 'Increase content using this hashtag and similar ones',
                'impact': 'Medium'
            })
            
            # Insight 3: Plan optimization
            most_popular_plan = max(students_analytics.plan_distribution.items(), key=lambda x: x[1])
            insights.append({
                'type': 'plan_optimization',
                'title': 'Plan Type Optimization',
                'description': f'Most popular plan: {most_popular_plan[0]} with {most_popular_plan[1]} enrollments',
                'action': 'Promote this plan more aggressively in social media',
                'impact': 'Medium'
            })
            
            # Insight 4: Engagement timing
            best_day = max(cross_platform_analytics.optimal_posting_times.items(), key=lambda x: x[1])
            insights.append({
                'type': 'timing_optimization',
                'title': 'Optimal Posting Schedule',
                'description': f'Best day for engagement: {best_day[0]} with {best_day[1]:.2%} engagement rate',
                'action': 'Schedule important posts for this day',
                'impact': 'Medium'
            })
            
            # Insight 5: Revenue opportunity
            if cross_platform_analytics.correlation_score > 0.3:
                insights.append({
                    'type': 'revenue_opportunity',
                    'title': 'Strong Social Media Impact',
                    'description': f'High correlation ({cross_platform_analytics.correlation_score:.2%}) between social engagement and enrollments',
                    'action': 'Increase social media investment and content frequency',
                    'impact': 'High'
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return [] 