#!/usr/bin/env python3
"""
Test script to verify dashboard chart data is correct
"""

from app import create_app
from models import db, Parent, Child, Session
import sys

def test_dashboard_chart():
    app = create_app()
    with app.app_context():
        # Get a parent
        parent = Parent.query.first()
        if not parent:
            print("❌ No parent found in database")
            return False
        
        print(f"✅ Testing with parent: {parent.name}")
        
        # Get children
        children = Child.query.filter_by(parent_id=parent.id).all()
        print(f"✅ Found {len(children)} children")
        
        if not children:
            print("⚠️  No children found - chart will show zeros")
            return True
        
        child_ids = [c.id for c in children]
        
        # Get sessions
        sessions = Session.query.filter(
            Session.child_id.in_(child_ids),
            Session.avg_accuracy != None,
            Session.result_status == 'Completed'
        ).order_by(Session.start_time.desc()).all()
        
        print(f"✅ Found {len(sessions)} completed sessions")
        
        # Test chart data generation
        if sessions:
            last_7 = sessions[:7]
            last_7.reverse()
            
            chart_data = [round(s.avg_accuracy, 1) if s.avg_accuracy else 0 for s in last_7]
            
            while len(chart_data) < 7:
                chart_data.insert(0, 0)
            
            print(f"✅ Chart data: {chart_data}")
            
            # Validate data
            if len(chart_data) != 7:
                print(f"❌ Chart data should have 7 points, has {len(chart_data)}")
                return False
            
            for val in chart_data:
                if not isinstance(val, (int, float)):
                    print(f"❌ Invalid value in chart data: {val} (type: {type(val)})")
                    return False
                if val < 0 or val > 100:
                    print(f"❌ Value out of range: {val}")
                    return False
            
            print("✅ All chart data values are valid!")
        else:
            chart_data = [0, 0, 0, 0, 0, 0, 0]
            print(f"✅ No sessions - using default chart data: {chart_data}")
        
        return True

if __name__ == '__main__':
    try:
        success = test_dashboard_chart()
        if success:
            print("\n✅ Dashboard chart test PASSED!")
            sys.exit(0)
        else:
            print("\n❌ Dashboard chart test FAILED!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
