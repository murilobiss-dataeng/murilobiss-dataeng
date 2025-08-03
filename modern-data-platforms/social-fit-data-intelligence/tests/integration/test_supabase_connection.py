#!/usr/bin/env python3
"""
Test script to verify Supabase connection and configuration.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test Supabase connection and configuration."""
    print("🔍 Testing Supabase Connection...")
    print("=" * 50)
    
    # Check environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_anon_key = os.getenv('SUPABASE_ANON_KEY')
    supabase_service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    print(f"SUPABASE_URL: {'✅ Set' if supabase_url else '❌ Not set'}")
    if supabase_url:
        print(f"  Value: {supabase_url}")
        if not supabase_url.startswith('https://'):
            print("  ⚠️  Warning: URL should start with 'https://'")
    
    print(f"SUPABASE_ANON_KEY: {'✅ Set' if supabase_anon_key else '❌ Not set'}")
    if supabase_anon_key:
        print(f"  Starts with: {supabase_anon_key[:20]}...")
        if not supabase_anon_key.startswith('eyJ'):
            print("  ⚠️  Warning: Key should start with 'eyJ'")
    
    print(f"SUPABASE_SERVICE_ROLE_KEY: {'✅ Set' if supabase_service_key else '❌ Not set'}")
    if supabase_service_key:
        print(f"  Starts with: {supabase_service_key[:20]}...")
        if not supabase_service_key.startswith('eyJ'):
            print("  ⚠️  Warning: Key should start with 'eyJ'")
    
    print("\n" + "=" * 50)
    
    # Try to create client
    if not supabase_url or not supabase_anon_key:
        print("❌ Cannot create Supabase client: Missing required credentials")
        return False
    
    try:
        print("🔄 Creating Supabase client...")
        supabase: Client = create_client(supabase_url, supabase_anon_key)
        print("✅ Supabase client created successfully")
        
        # Test connection by trying to access tables in social_fit schema
        print("🔄 Testing connection to 'social_fit.students' table...")
        
        # Try to access the students table using schema-qualified name
        # Note: Supabase client may need special handling for schema-qualified names
        try:
            # First try with schema-qualified name
            result = supabase.table('social_fit.students').select('*').limit(1).execute()
            print("✅ Connection successful! Table 'social_fit.students' access works.")
        except Exception as schema_error:
            print(f"⚠️  Schema-qualified access failed: {schema_error}")
            print("🔄 Trying alternative approach...")
            
            # Try to set the search path or use a different approach
            try:
                # Try without schema (assuming search_path is set)
                result = supabase.table('students').select('*').limit(1).execute()
                print("✅ Connection successful! Table 'students' access works (using search_path).")
            except Exception as direct_error:
                print(f"❌ Direct table access also failed: {direct_error}")
                raise direct_error
        
        # Test other tables
        print("🔄 Testing 'social_fit.instagram_posts' table...")
        try:
            result = supabase.table('social_fit.instagram_posts').select('*').limit(1).execute()
            print("✅ Table 'social_fit.instagram_posts' access works.")
        except:
            result = supabase.table('instagram_posts').select('*').limit(1).execute()
            print("✅ Table 'instagram_posts' access works.")
        
        print("🔄 Testing 'social_fit.analytics' table...")
        try:
            result = supabase.table('social_fit.analytics').select('*').limit(1).execute()
            print("✅ Table 'social_fit.analytics' access works.")
        except:
            result = supabase.table('analytics').select('*').limit(1).execute()
            print("✅ Table 'analytics' access works.")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Provide specific guidance based on error
        if "nodename nor servname provided" in str(e):
            print("\n💡 This error usually means:")
            print("   - SUPABASE_URL is malformed")
            print("   - URL contains invalid characters")
            print("   - Network/DNS issues")
        elif "401" in str(e):
            print("\n💡 This error usually means:")
            print("   - SUPABASE_ANON_KEY is invalid")
            print("   - Key has expired or been revoked")
        elif "relation" in str(e) and "does not exist" in str(e):
            print("\n💡 This error means the tables don't exist yet.")
            print("   Please execute the SQL in 'create_tables.sql' in your Supabase dashboard:")
            print("   1. Go to https://supabase.com/dashboard")
            print("   2. Select your project")
            print("   3. Go to 'SQL Editor'")
            print("   4. Copy and paste the content of 'create_tables.sql'")
            print("   5. Click 'Run'")
            print("   This will create the tables in the 'social_fit' schema.")
        
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    if success:
        print("\n🎉 Supabase connection test PASSED!")
        print("✅ All tables are accessible. You can now run the main pipeline!")
    else:
        print("\n💥 Supabase connection test FAILED!")
        print("Please check your .env file and Supabase credentials.") 