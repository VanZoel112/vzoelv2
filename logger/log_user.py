"""
User Activity Logger - Premium User Tracking System
Track user interactions dengan premium formatting dan statistics
Created by: Vzoel Fox's
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from collections import defaultdict
from pyrogram import Client
from pyrogram.types import Message, User, Chat

try:
    from utils.assets import VzoelAssets, bold, italic, emoji
except ImportError:
    def bold(text): return f"**{text}**"
    def italic(text): return f"_{text}_"
    def emoji(key): return ""

class UserActivityLogger:
    """
    Premium user activity tracking dengan comprehensive statistics
    """
    
    def __init__(self, config_path: str = "vzoel/config.json", data_dir: str = "user_data"):
        self.config_path = config_path
        self.data_dir = data_dir
        self.config = self.load_config()
        
        # Create data directory
        os.makedirs(self.data_dir, exist_ok=True)
        
        # User activity storage
        self.activity_file = os.path.join(self.data_dir, "user_activity.json")
        self.daily_stats_file = os.path.join(self.data_dir, "daily_stats.json")
        
        # Load existing data
        self.user_activities = self.load_user_activities()
        self.daily_stats = self.load_daily_stats()
        
        # Premium assets
        self.assets = None
        try:
            self.assets = VzoelAssets()
        except:
            pass
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration dari vzoel/config.json"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Failed to load config: {e}")
            return {}
    
    def load_user_activities(self) -> Dict[str, Any]:
        """Load user activities dari file"""
        try:
            if os.path.exists(self.activity_file):
                with open(self.activity_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Failed to load user activities: {e}")
            return {}
    
    def load_daily_stats(self) -> Dict[str, Any]:
        """Load daily statistics dari file"""
        try:
            if os.path.exists(self.daily_stats_file):
                with open(self.daily_stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Failed to load daily stats: {e}")
            return {}
    
    def save_user_activities(self):
        """Save user activities ke file"""
        try:
            with open(self.activity_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_activities, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save user activities: {e}")
    
    def save_daily_stats(self):
        """Save daily statistics ke file"""
        try:
            with open(self.daily_stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.daily_stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save daily stats: {e}")
    
    def get_premium_emoji(self, emoji_key: str) -> str:
        """Get premium emoji atau fallback"""
        if self.assets:
            return self.assets.get_emoji(emoji_key)
        return emoji(emoji_key) if 'emoji' in globals() else ""
    
    def log_user_activity(self, user: User, chat: Chat, command: str, success: bool = True):
        """Log user activity dengan comprehensive data"""
        
        user_id = str(user.id)
        chat_id = str(chat.id)
        timestamp = datetime.now().isoformat()
        date_key = datetime.now().strftime('%Y-%m-%d')
        
        # Initialize user data jika belum ada
        if user_id not in self.user_activities:
            self.user_activities[user_id] = {
                "user_info": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "is_bot": user.is_bot,
                    "first_seen": timestamp
                },
                "statistics": {
                    "total_commands": 0,
                    "successful_commands": 0,
                    "failed_commands": 0,
                    "last_activity": timestamp,
                    "commands_used": {},
                    "chat_interactions": {},
                    "daily_activity": {}
                },
                "activity_history": []
            }
        
        user_data = self.user_activities[user_id]
        
        # Update user info (jika ada perubahan)
        user_data["user_info"].update({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        })
        
        # Update statistics
        stats = user_data["statistics"]
        stats["total_commands"] += 1
        stats["last_activity"] = timestamp
        
        if success:
            stats["successful_commands"] += 1
        else:
            stats["failed_commands"] += 1
        
        # Command tracking
        if command not in stats["commands_used"]:
            stats["commands_used"][command] = {"count": 0, "success": 0, "failed": 0}
        
        stats["commands_used"][command]["count"] += 1
        if success:
            stats["commands_used"][command]["success"] += 1
        else:
            stats["commands_used"][command]["failed"] += 1
        
        # Chat interaction tracking
        if chat_id not in stats["chat_interactions"]:
            stats["chat_interactions"][chat_id] = {
                "chat_info": {
                    "id": chat.id,
                    "title": getattr(chat, 'title', None),
                    "type": chat.type.value if hasattr(chat.type, 'value') else str(chat.type),
                    "username": getattr(chat, 'username', None)
                },
                "interaction_count": 0,
                "last_interaction": timestamp
            }
        
        stats["chat_interactions"][chat_id]["interaction_count"] += 1
        stats["chat_interactions"][chat_id]["last_interaction"] = timestamp
        
        # Daily activity tracking
        if date_key not in stats["daily_activity"]:
            stats["daily_activity"][date_key] = {"commands": 0, "success": 0, "failed": 0}
        
        stats["daily_activity"][date_key]["commands"] += 1
        if success:
            stats["daily_activity"][date_key]["success"] += 1
        else:
            stats["daily_activity"][date_key]["failed"] += 1
        
        # Add to activity history (keep last 100 activities)
        activity_record = {
            "timestamp": timestamp,
            "command": command,
            "chat_id": chat.id,
            "chat_type": chat.type.value if hasattr(chat.type, 'value') else str(chat.type),
            "success": success
        }
        
        user_data["activity_history"].append(activity_record)
        
        # Keep only last 100 activities
        if len(user_data["activity_history"]) > 100:
            user_data["activity_history"] = user_data["activity_history"][-100:]
        
        # Update daily statistics
        self.update_daily_stats(date_key, command, success)
        
        # Save data
        self.save_user_activities()
        self.save_daily_stats()
    
    def update_daily_stats(self, date_key: str, command: str, success: bool):
        """Update daily statistics"""
        
        if date_key not in self.daily_stats:
            self.daily_stats[date_key] = {
                "total_commands": 0,
                "successful_commands": 0,
                "failed_commands": 0,
                "unique_users": set(),
                "commands_breakdown": {},
                "active_users": []
            }
        
        day_stats = self.daily_stats[date_key]
        day_stats["total_commands"] += 1
        
        if success:
            day_stats["successful_commands"] += 1
        else:
            day_stats["failed_commands"] += 1
        
        # Command breakdown
        if command not in day_stats["commands_breakdown"]:
            day_stats["commands_breakdown"][command] = {"count": 0, "success": 0, "failed": 0}
        
        day_stats["commands_breakdown"][command]["count"] += 1
        if success:
            day_stats["commands_breakdown"][command]["success"] += 1
        else:
            day_stats["commands_breakdown"][command]["failed"] += 1
        
        # Convert set to list untuk JSON serialization
        if isinstance(day_stats["unique_users"], set):
            day_stats["unique_users"] = list(day_stats["unique_users"])
    
    def get_user_stats(self, user_id: Union[int, str]) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        
        user_id = str(user_id)
        if user_id not in self.user_activities:
            return {}
        
        user_data = self.user_activities[user_id]
        stats = user_data["statistics"]
        
        # Calculate success rate
        total = stats["total_commands"]
        success_rate = (stats["successful_commands"] / total * 100) if total > 0 else 0
        
        # Most used commands
        most_used = sorted(
            stats["commands_used"].items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:5]
        
        # Recent activity (last 7 days)
        recent_days = []
        for i in range(7):
            date_key = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            if date_key in stats["daily_activity"]:
                recent_days.append({
                    "date": date_key,
                    "commands": stats["daily_activity"][date_key]["commands"]
                })
        
        return {
            "user_info": user_data["user_info"],
            "total_commands": total,
            "success_rate": round(success_rate, 2),
            "successful_commands": stats["successful_commands"],
            "failed_commands": stats["failed_commands"],
            "most_used_commands": most_used,
            "chat_count": len(stats["chat_interactions"]),
            "recent_activity": recent_days,
            "last_activity": stats["last_activity"],
            "first_seen": user_data["user_info"]["first_seen"]
        }
    
    def create_user_report(self, user_id: Union[int, str]) -> str:
        """Create formatted user activity report"""
        
        stats = self.get_user_stats(user_id)
        if not stats:
            return f"{self.get_premium_emoji('merah')} User tidak ditemukan dalam database"
        
        user_info = stats["user_info"]
        name = user_info.get("first_name", "Unknown")
        if user_info.get("last_name"):
            name += f" {user_info['last_name']}"
        
        username = user_info.get("username")
        username_display = f"@{username}" if username else "No username"
        
        # Format dates
        first_seen = datetime.fromisoformat(stats["first_seen"]).strftime('%Y-%m-%d')
        last_activity = datetime.fromisoformat(stats["last_activity"]).strftime('%Y-%m-%d %H:%M')
        
        report_lines = [
            f"{self.get_premium_emoji('utama')} {bold('USER ACTIVITY REPORT')}",
            "",
            f"{self.get_premium_emoji('centang')} {bold('User Information:')}",
            f"• Name: {bold(name)}",
            f"• Username: {bold(username_display)}",
            f"• User ID: {bold(str(user_info['id']))}",
            f"• First Seen: {bold(first_seen)}",
            f"• Last Activity: {bold(last_activity)}",
            "",
            f"{self.get_premium_emoji('loading')} {bold('Command Statistics:')}",
            f"• Total Commands: {bold(str(stats['total_commands']))}",
            f"• Successful: {bold(str(stats['successful_commands']))}",
            f"• Failed: {bold(str(stats['failed_commands']))}",
            f"• Success Rate: {bold(str(stats['success_rate']) + '%')}",
            f"• Chat Interactions: {bold(str(stats['chat_count']))}",
            ""
        ]
        
        # Most used commands
        if stats["most_used_commands"]:
            report_lines.append(f"{self.get_premium_emoji('aktif')} {bold('Most Used Commands:')}")
            for i, (cmd, cmd_stats) in enumerate(stats["most_used_commands"], 1):
                report_lines.append(f"  {i}. {bold(cmd)} - {cmd_stats['count']} times")
            report_lines.append("")
        
        # Recent activity
        if stats["recent_activity"]:
            report_lines.append(f"{self.get_premium_emoji('loading')} {bold('Recent Activity (Last 7 Days):')}")
            for day_data in stats["recent_activity"][:5]:  # Show last 5 days
                date_formatted = datetime.strptime(day_data["date"], '%Y-%m-%d').strftime('%m-%d')
                report_lines.append(f"  • {date_formatted}: {bold(str(day_data['commands']))} commands")
            report_lines.append("")
        
        report_lines.append(f"{italic('Generated by Vzoel User Activity Logger')}")
        
        return "\n".join(report_lines)
    
    def get_daily_report(self, date: Optional[str] = None) -> str:
        """Get daily activity report"""
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if date not in self.daily_stats:
            return f"{self.get_premium_emoji('merah')} No data available for {date}"
        
        day_stats = self.daily_stats[date]
        
        # Top commands for the day
        top_commands = sorted(
            day_stats["commands_breakdown"].items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:5]
        
        success_rate = (day_stats["successful_commands"] / day_stats["total_commands"] * 100) if day_stats["total_commands"] > 0 else 0
        
        report_lines = [
            f"{self.get_premium_emoji('utama')} {bold('DAILY ACTIVITY REPORT')}",
            f"{bold(f'Date: {date}')}",
            "",
            f"{self.get_premium_emoji('centang')} {bold('Overview:')}",
            f"• Total Commands: {bold(str(day_stats['total_commands']))}",
            f"• Successful: {bold(str(day_stats['successful_commands']))}",
            f"• Failed: {bold(str(day_stats['failed_commands']))}",
            f"• Success Rate: {bold(f'{success_rate:.1f}%')}",
            f"• Unique Users: {bold(str(len(day_stats.get('unique_users', []))))}",
            ""
        ]
        
        if top_commands:
            report_lines.append(f"{self.get_premium_emoji('loading')} {bold('Top Commands:')}")
            for i, (cmd, cmd_stats) in enumerate(top_commands, 1):
                rate = (cmd_stats['success'] / cmd_stats['count'] * 100) if cmd_stats['count'] > 0 else 0
                report_lines.append(f"  {i}. {bold(cmd)} - {cmd_stats['count']} uses ({rate:.1f}% success)")
            report_lines.append("")
        
        report_lines.append(f"{italic('Generated by Vzoel Daily Logger')}")
        
        return "\n".join(report_lines)
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Cleanup old activity data"""
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d')
        
        # Clean daily stats
        dates_to_remove = []
        for date_key in self.daily_stats:
            if date_key < cutoff_str:
                dates_to_remove.append(date_key)
        
        for date_key in dates_to_remove:
            del self.daily_stats[date_key]
        
        # Clean user daily activity
        for user_id in self.user_activities:
            user_data = self.user_activities[user_id]
            daily_activity = user_data["statistics"]["daily_activity"]
            
            dates_to_remove = []
            for date_key in daily_activity:
                if date_key < cutoff_str:
                    dates_to_remove.append(date_key)
            
            for date_key in dates_to_remove:
                del daily_activity[date_key]
        
        self.save_user_activities()
        self.save_daily_stats()
        
        return len(dates_to_remove)
    
    def get_top_users(self, limit: int = 10, metric: str = "total_commands") -> List[Dict]:
        """Get top users berdasarkan metric tertentu"""
        
        user_rankings = []
        
        for user_id, user_data in self.user_activities.items():
            stats = user_data["statistics"]
            user_info = user_data["user_info"]
            
            metric_value = stats.get(metric, 0)
            
            user_rankings.append({
                "user_id": user_id,
                "user_info": user_info,
                "metric_value": metric_value,
                "total_commands": stats["total_commands"],
                "success_rate": (stats["successful_commands"] / stats["total_commands"] * 100) if stats["total_commands"] > 0 else 0
            })
        
        # Sort berdasarkan metric
        user_rankings.sort(key=lambda x: x["metric_value"], reverse=True)
        
        return user_rankings[:limit]

# Global instance
user_logger = UserActivityLogger()

# Convenience functions
def log_user_command(user: User, chat: Chat, command: str, success: bool = True):
    """Quick user command logging"""
    user_logger.log_user_activity(user, chat, command, success)

def get_user_report(user_id: Union[int, str]) -> str:
    """Quick user report generation"""
    return user_logger.create_user_report(user_id)

def get_daily_report(date: Optional[str] = None) -> str:
    """Quick daily report generation"""
    return user_logger.get_daily_report(date)

def get_user_activity_logger() -> UserActivityLogger:
    """Get global user logger instance"""
    return user_logger