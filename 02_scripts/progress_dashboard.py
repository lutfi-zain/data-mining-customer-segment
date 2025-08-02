import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np

# Load project tracker data
df = pd.read_csv('project_tracker.csv')

print("=== PROJECT PROGRESS DASHBOARD ===")

# Overall progress calculation
total_tasks = len(df)
completed_tasks = len(df[df['Status'] == 'Complete'])
overall_progress = (completed_tasks / total_tasks) * 100

print(f"📊 Overall Project Progress: {overall_progress:.1f}% ({completed_tasks}/{total_tasks} tasks)")

# Progress by phase
phase_progress = df.groupby('Phase').agg({
    'Task_ID': 'count',
    'Progress_%': 'mean'
}).round(1)
phase_progress.columns = ['Total_Tasks', 'Avg_Progress']
phase_progress['Phase_Status'] = phase_progress['Avg_Progress'].apply(
    lambda x: '✅ Complete' if x == 100 else '🚀 In Progress' if x > 0 else '📋 Not Started'
)

print("\n=== PROGRESS BY PHASE ===")
print(phase_progress)

# Milestone progress
milestone_progress = df.groupby('Milestone').agg({
    'Task_ID': 'count', 
    'Progress_%': 'mean'
}).round(1)
milestone_progress.columns = ['Total_Tasks', 'Avg_Progress']

print("\n=== PROGRESS BY MILESTONE ===")
print(milestone_progress)

# Timeline analysis
df['Start_Date'] = pd.to_datetime(df['Start_Date'])
df['Target_Date'] = pd.to_datetime(df['Target_Date'])

# Current date
current_date = datetime(2025, 8, 2)

# Tasks due this week
this_week_end = current_date + timedelta(days=7)
tasks_this_week = df[(df['Target_Date'] >= current_date) & 
                     (df['Target_Date'] <= this_week_end) & 
                     (df['Status'] != 'Complete')]

print(f"\n=== TASKS DUE THIS WEEK (Next 7 days) ===")
if len(tasks_this_week) > 0:
    print(tasks_this_week[['Task_Name', 'Priority', 'Owner', 'Target_Date', 'Status']].to_string(index=False))
else:
    print("No tasks due this week")

# High priority pending tasks
high_priority_pending = df[(df['Priority'] == 'High') & 
                          (df['Status'] == 'Not Started')]

print(f"\n=== HIGH PRIORITY PENDING TASKS ===")
if len(high_priority_pending) > 0:
    print(high_priority_pending[['Task_Name', 'Milestone', 'Owner', 'Target_Date']].to_string(index=False))
else:
    print("No high priority pending tasks")

# Create visualizations
plt.style.use('default')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# 1. Overall Progress Pie Chart
progress_data = [completed_tasks, total_tasks - completed_tasks]
progress_labels = ['Completed', 'Remaining']
colors = ['#28a745', '#dc3545']

ax1.pie(progress_data, labels=progress_labels, autopct='%1.1f%%', 
        colors=colors, startangle=90)
ax1.set_title(f'Overall Project Progress\n{overall_progress:.1f}% Complete', 
              fontsize=14, fontweight='bold')

# 2. Progress by Phase Bar Chart
phases = phase_progress.index
progress_vals = phase_progress['Avg_Progress']

bars = ax2.bar(phases, progress_vals, color=['#28a745' if x == 100 else '#ffc107' if x > 0 else '#dc3545' for x in progress_vals])
ax2.set_title('Progress by Phase', fontsize=14, fontweight='bold')
ax2.set_ylabel('Progress (%)')
ax2.set_ylim(0, 100)

# Add value labels on bars
for bar, val in zip(bars, progress_vals):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{val:.0f}%', ha='center', va='bottom')

ax2.tick_params(axis='x', rotation=45)

# 3. Tasks by Priority
priority_counts = df['Priority'].value_counts()
colors_priority = {'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#28a745'}
colors_list = [colors_priority.get(x, '#6c757d') for x in priority_counts.index]

ax3.bar(priority_counts.index, priority_counts.values, color=colors_list)
ax3.set_title('Tasks by Priority Level', fontsize=14, fontweight='bold')
ax3.set_ylabel('Number of Tasks')

# Add value labels
for i, v in enumerate(priority_counts.values):
    ax3.text(i, v + 0.5, str(v), ha='center', va='bottom')

# 4. Timeline Gantt-style view (Next 4 weeks)
next_4_weeks = df[(df['Target_Date'] >= current_date) & 
                  (df['Target_Date'] <= current_date + timedelta(weeks=4))]

if len(next_4_weeks) > 0:
    # Sort by target date
    next_4_weeks_sorted = next_4_weeks.sort_values('Target_Date')
    
    y_positions = range(len(next_4_weeks_sorted))
    dates = next_4_weeks_sorted['Target_Date']
    
    # Convert dates to numbers for plotting
    date_nums = [(d - current_date).days for d in dates]
    
    colors_status = {'Complete': '#28a745', 'In Progress': '#ffc107', 'Not Started': '#dc3545'}
    colors_list = [colors_status.get(status, '#6c757d') for status in next_4_weeks_sorted['Status']]
    
    scatter = ax4.scatter(date_nums, y_positions, c=colors_list, s=100, alpha=0.7)
    
    # Add task labels
    for i, (idx, row) in enumerate(next_4_weeks_sorted.iterrows()):
        ax4.text(date_nums[i] + 0.5, i, row['Task_Name'][:20] + '...', 
                fontsize=8, va='center')
    
    ax4.set_title('Upcoming Tasks (Next 4 Weeks)', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Days from Today')
    ax4.set_ylabel('Tasks')
    ax4.grid(True, alpha=0.3)
else:
    ax4.text(0.5, 0.5, 'No tasks scheduled\nin next 4 weeks', 
             ha='center', va='center', transform=ax4.transAxes, fontsize=12)
    ax4.set_title('Upcoming Tasks (Next 4 Weeks)', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('05_results/project_progress_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()

# Generate summary report
print(f"\n=== PROJECT SUMMARY REPORT ===")
print(f"📅 Report Date: {current_date.strftime('%d %B %Y')}")
print(f"📊 Overall Progress: {overall_progress:.1f}%")
print(f"✅ Completed Tasks: {completed_tasks}")
print(f"📋 Remaining Tasks: {total_tasks - completed_tasks}")
print(f"🔥 High Priority Pending: {len(high_priority_pending)}")
print(f"📆 Tasks Due This Week: {len(tasks_this_week)}")

# Next actions
print(f"\n=== NEXT ACTIONS REQUIRED ===")
print("1. 🚀 Start Market Opportunity Analysis")
print("2. 📊 Set up data collection for competitive analysis")
print("3. 👥 Assign team members to Phase 2 tasks")
print("4. 📅 Schedule weekly progress review meetings")

print(f"\n📈 Dashboard saved: 05_results/project_progress_dashboard.png")
