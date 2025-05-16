# Task Master Tools Guide

This document provides example questions and use cases for each of the Task Master tools available through the Model Context Protocol (MCP) in this project. Each section groups related tools to help you find the right tool for your needs.

## Project Initialization

### 1. Initialize a New Task Master Project
**Question:** "I want to set up a new Task Master project for my Python application. Can you help me organize my tasks using Task Master?"  
**Tool:** `f1e_initialize_project`

### 2. Parse Project Requirements
**Question:** "I've written a Product Requirements Document (PRD) for my project. Can you analyze it and generate a list of tasks to implement those requirements?"  
**Tool:** `f1e_parse_prd`

### 3. Generate Task Files
**Question:** "I've made several changes to my tasks.json file. Can you regenerate all the individual task files to reflect these changes?"  
**Tool:** `f1e_generate`

## Task Viewing and Navigation

### 4. Get All Tasks
**Question:** "Show me all the tasks that are currently in my project. I'd like to see what's pending and what's been completed."  
**Tool:** `f1e_get_tasks`

### 5. Get a Specific Task
**Question:** "I need more details about task #5. Can you show me its description, status, and any subtasks it might have?"  
**Tool:** `f1e_get_task`

### 6. Find the Next Task
**Question:** "Based on our current progress and task dependencies, what should I work on next?"  
**Tool:** `f1e_next_task`

## Task Management

### 7. Add a New Task
**Question:** "I need to add a new task to implement user authentication. Can you help me create this with the right description and dependencies?"  
**Tool:** `f1e_add_task`

### 8. Update an Existing Task
**Question:** "Task #3 needs to be updated with some new requirements. Can you incorporate this additional information into the task description?"  
**Tool:** `f1e_update_task`

### 9. Update a Subtask
**Question:** "Subtask 4.2 needs to be updated with a more detailed implementation approach. Can you add this information without changing the rest of the subtask?"  
**Tool:** `f1e_update_subtask`

### 10. Update Multiple Tasks
**Question:** "We've decided to use a different database technology. Can you update all tasks from ID #10 onwards to reflect this change in approach?"  
**Tool:** `f1e_update`

### 11. Remove a Task
**Question:** "We've decided not to implement the social media integration feature. Can you remove task #7 from our project?"  
**Tool:** `f1e_remove_task`

### 12. Set Task Status
**Question:** "I've completed the database schema implementation. Can you mark task #2 as 'done'?"  
**Tool:** `f1e_set_task_status`

## Task Dependencies and Relationships

### 13. Add a Dependency
**Question:** "Task #6 can't start until task #4 is completed. Can you set up this dependency relationship?"  
**Tool:** `f1e_add_dependency`

### 14. Remove a Dependency
**Question:** "We've restructured our approach, and task #3 no longer depends on task #1. Can you remove this dependency?"  
**Tool:** `f1e_remove_dependency`

### 15. Validate Dependencies
**Question:** "Can you check our task dependencies to make sure there are no circular references or other issues that might block our progress?"  
**Tool:** `f1e_validate_dependencies`

### 16. Fix Dependencies
**Question:** "You found some issues with our task dependencies. Can you automatically fix them to ensure a proper workflow?"  
**Tool:** `f1e_fix_dependencies`

## Task Expansion and Subtasks

### 17. Expand a Task into Subtasks
**Question:** "Task #8 about implementing the REST API seems too large. Can you break it down into more manageable subtasks?"  
**Tool:** `f1e_expand_task`

### 18. Expand All Tasks
**Question:** "I'd like to break down all our pending tasks into subtasks to make them more actionable. Can you do this for all pending tasks at once?"  
**Tool:** `f1e_expand_all`

### 19. Add a Subtask
**Question:** "I need to add a new subtask to task #5 for writing unit tests. Can you add this as a subtask 5.4?"  
**Tool:** `f1e_add_subtask`

### 20. Remove a Subtask
**Question:** "Subtask 3.2 is no longer necessary as we're using a different approach. Can you remove it while keeping the other subtasks?"  
**Tool:** `f1e_remove_subtask`

### 21. Clear all Subtasks
**Question:** "I want to reorganize task #9 completely. Can you remove all its current subtasks so I can start fresh?"  
**Tool:** `f1e_clear_subtasks`

## Task Analysis and Complexity

### 22. Analyze Project Complexity
**Question:** "Can you analyze the complexity of all the tasks in our project? I want to understand which ones might need more resources or time."  
**Tool:** `f1e_analyze_project_complexity`

### 23. Display Complexity Report
**Question:** "Show me a detailed report of the complexity analysis you just ran. I'd like to see the reasoning behind each complexity score."  
**Tool:** `f1e_complexity_report`

## AI Model Configuration

### 24. Configure AI Models
**Question:** "I want to see what AI models are available for Task Master and potentially change which models are used for task generation and research."  
**Tool:** `f1e_models`

## Last Updated

This guide was last updated on: 2025-05-16
