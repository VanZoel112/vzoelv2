#!/usr/bin/env python3
"""
Logger System Test - Comprehensive Testing
Test semua komponen logger system dengan config integration
Created by: Vzoel Fox's
"""

import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test imports
def test_imports():
    """Test all logger imports"""
    print("🔍 Testing logger imports...")
    
    try:
        from logger import (
            VzoelLogger, UserActivityLogger,
            vzoel_logger, user_logger,
            log_info, log_warning, log_error, log_success,
            get_user_report, get_daily_report,
            get_logging_system_status, health_check
        )
        print("✅ All logger imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config_loading():
    """Test config loading"""
    print("\n🔍 Testing config loading...")
    
    try:
        from logger import vzoel_logger
        
        if len(vzoel_logger.config) > 0:
            print("✅ Config loaded successfully")
            print(f"   - Project: {vzoel_logger.config.get('project_info', {}).get('project_name', 'Unknown')}")
            print(f"   - Version: {vzoel_logger.config.get('project_info', {}).get('version', 'Unknown')}")
            return True
        else:
            print("⚠️ Config is empty")
            return False
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        return False

def test_premium_assets():
    """Test premium assets integration"""
    print("\n🔍 Testing premium assets...")
    
    try:
        from logger import vzoel_logger
        
        if vzoel_logger.assets:
            print("✅ Premium assets loaded")
            test_emoji = vzoel_logger.get_premium_emoji("centang")
            print(f"   - Test emoji 'centang': {test_emoji}")
            return True
        else:
            print("⚠️ Premium assets not available (fallback mode)")
            return True  # Still OK, fallback should work
    except Exception as e:
        print(f"❌ Premium assets test failed: {e}")
        return False

def test_basic_logging():
    """Test basic logging functionality"""
    print("\n🔍 Testing basic logging...")
    
    try:
        from logger import log_info, log_warning, log_error, log_success
        
        # Test different log levels
        log_info("Test info message", {"test": "data"})
        log_warning("Test warning message")
        log_error("Test error message", send_to_telegram=False)  # Don't spam Telegram
        log_success("Test success message")
        
        print("✅ Basic logging functions work")
        return True
    except Exception as e:
        print(f"❌ Basic logging failed: {e}")
        return False

def test_user_logger():
    """Test user activity logger"""
    print("\n🔍 Testing user activity logger...")
    
    try:
        from logger import user_logger
        
        # Create mock user and chat objects
        class MockUser:
            def __init__(self):
                self.id = 12345
                self.first_name = "Test"
                self.last_name = "User"
                self.username = "testuser"
                self.is_bot = False
        
        class MockChat:
            def __init__(self):
                self.id = -12345
                self.title = "Test Group"
                self.type = "group"
        
        mock_user = MockUser()
        mock_chat = MockChat()
        
        # Test logging user activity
        user_logger.log_user_activity(mock_user, mock_chat, "/test", success=True)
        
        # Test getting user stats
        stats = user_logger.get_user_stats(12345)
        
        if stats:
            print("✅ User activity logging works")
            print(f"   - User tracked: {stats['user_info']['first_name']}")
            print(f"   - Total commands: {stats['total_commands']}")
            return True
        else:
            print("⚠️ User stats empty")
            return False
    except Exception as e:
        print(f"❌ User logger failed: {e}")
        return False

def test_system_status():
    """Test system status functions"""
    print("\n🔍 Testing system status...")
    
    try:
        from logger import get_logging_system_status, health_check
        
        # Test system status
        status = get_logging_system_status()
        print("✅ System status retrieved")
        print(f"   - Version: {status['version']}")
        print(f"   - Config loaded: {status['config_loaded']}")
        print(f"   - Premium assets: {status['premium_assets']}")
        
        # Test health check
        health = health_check()
        print(f"   - Overall health: {health['overall_health']}")
        print(f"   - Issues found: {len(health['issues'])}")
        
        return True
    except Exception as e:
        print(f"❌ System status test failed: {e}")
        return False

def test_report_generation():
    """Test report generation"""
    print("\n🔍 Testing report generation...")
    
    try:
        from logger import get_user_report, get_daily_report, vzoel_logger
        
        # Test user report (should handle non-existent user gracefully)
        user_report = get_user_report(99999)  # Non-existent user
        print("✅ User report generation works (handled non-existent user)")
        
        # Test daily report
        daily_report = get_daily_report()
        print("✅ Daily report generation works")
        
        # Test system report
        system_report_task = vzoel_logger.create_log_report()
        print("✅ System report generation works")
        
        return True
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return False

def test_data_persistence():
    """Test data persistence"""
    print("\n🔍 Testing data persistence...")
    
    try:
        from logger import user_logger
        
        # Check if data directories exist
        data_dir = user_logger.data_dir
        activity_file = user_logger.activity_file
        
        print(f"   - Data directory: {data_dir}")
        print(f"   - Activity file exists: {os.path.exists(activity_file)}")
        
        # Test save functionality
        user_logger.save_user_activities()
        user_logger.save_daily_stats()
        
        print("✅ Data persistence works")
        return True
    except Exception as e:
        print(f"❌ Data persistence failed: {e}")
        return False

def test_error_handling():
    """Test error handling and fallbacks"""
    print("\n🔍 Testing error handling...")
    
    try:
        from logger import vzoel_logger, emergency_log, VzoelLogger
        
        # Test emergency logging
        emergency_log("Test emergency message", {"test": "emergency"})
        
        # Test with invalid data
        invalid_config = VzoelLogger("non_existent_config.json")
        print("✅ Error handling works (graceful fallbacks)")
        
        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 Starting Vzoel Logger System Comprehensive Test")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Config Loading", test_config_loading), 
        ("Premium Assets", test_premium_assets),
        ("Basic Logging", test_basic_logging),
        ("User Logger", test_user_logger),
        ("System Status", test_system_status),
        ("Report Generation", test_report_generation),
        ("Data Persistence", test_data_persistence),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success Rate: {(passed / (passed + failed) * 100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Logger system is ready for production.")
    else:
        print(f"\n⚠️ {failed} tests failed. Please check the issues above.")
    
    # Generate test report
    test_report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": len(tests),
        "passed": passed,
        "failed": failed,
        "success_rate": round(passed / (passed + failed) * 100, 1),
        "status": "PASSED" if failed == 0 else "FAILED"
    }
    
    # Save test results
    try:
        with open("test_results.json", "w") as f:
            json.dump(test_report, f, indent=2)
        print(f"\n📄 Test results saved to test_results.json")
    except Exception as e:
        print(f"\n⚠️ Could not save test results: {e}")
    
    return failed == 0

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)