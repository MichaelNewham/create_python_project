# Memory Tools Guide

This document provides an overview of Memory's capabilities through the Model Context Protocol (MCP) in VS Code. The Memory MCP server provides persistent knowledge storage and retrieval across sessions, acting as a long-term memory for your AI assistant.

## Memory Operations

### 1. Create Memory
**Question:** "Remember that our API endpoint for production is https://api.example.com/v2"  
**Tool:** `create_memory`  
**Description:** Creates a new memory entry with a unique name and content. Each memory is stored persistently and can be retrieved in future sessions.

### 2. Retrieve Memory
**Question:** "What was that production API endpoint we discussed last week?"  
**Tool:** `retrieve_memory`  
**Description:** Retrieves a specific memory by its exact name, returning the stored content.

### 3. Search Memories
**Question:** "What do you remember about our authentication setup?"  
**Tool:** `search_memories`  
**Description:** Searches through all stored memories using keywords or phrases, returning relevant memories ranked by similarity.

### 4. List Memories
**Question:** "Show me all the things you've remembered about this project."  
**Tool:** `list_memories`  
**Description:** Lists all stored memories, optionally filtered by tags or limited to a specific number of results.

### 5. Update Memory
**Question:** "Update the API endpoint memory - it's now https://api.example.com/v3"  
**Tool:** `update_memory`  
**Description:** Updates the content of an existing memory while preserving its name and metadata.

### 6. Delete Memory
**Question:** "Forget about the old staging server configuration."  
**Tool:** `delete_memory`  
**Description:** Permanently removes a memory from storage.

### 7. Create Knowledge Graph Relation
**Question:** "Connect the 'UserAuthFlow' memory with the 'APIEndpoints' memory."  
**Tool:** `create_relation`  
**Description:** Creates relationships between memories to build a knowledge graph, enabling more sophisticated retrieval.

### 8. List Relations
**Question:** "Show me how the authentication memories are connected."  
**Tool:** `list_relations`  
**Description:** Lists all relationships for a specific memory or all relationships in the knowledge graph.

## Use Cases

### Project Configuration Management

**Question:** "Remember all our project's important configuration details."  
**Workflow:**
1. Use `create_memory` to store database connection strings
2. Use `create_memory` to store API keys and endpoints
3. Use `create_memory` to store deployment configurations
4. Use `create_relation` to link related configurations

### Code Patterns and Best Practices

**Question:** "Save this authentication pattern we've decided to use across the project."  
**Workflow:**
1. Use `create_memory` with a descriptive name like "auth-pattern-jwt"
2. Include code examples and implementation notes
3. Tag it appropriately for easy retrieval

### Bug Solutions and Workarounds

**Question:** "Remember how we fixed that tricky CORS issue."  
**Workflow:**
1. Use `create_memory` to store the problem description
2. Use `create_memory` to store the solution
3. Use `create_relation` to link problem and solution

### Team Knowledge Base

**Question:** "Store our team's coding conventions and standards."  
**Workflow:**
1. Use `create_memory` for naming conventions
2. Use `create_memory` for code review checklist
3. Use `create_memory` for git workflow
4. Use `list_memories` with tag filtering to organize by category

### Learning and Documentation

**Question:** "Remember these important React hooks patterns I just learned."  
**Workflow:**
1. Use `create_memory` with clear, searchable names
2. Include examples and use cases
3. Use `search_memories` later to quickly find relevant patterns

## Best Practices for Using Memory

### 1. Use Descriptive Names
Create memories with clear, descriptive names that make them easy to find later. Use consistent naming conventions like "config-database", "pattern-authentication", "bug-fix-cors".

### 2. Organize with Tags
Use tags to categorize memories. Common tags might include:
- `config`, `credentials`, `endpoints`
- `pattern`, `best-practice`, `convention`
- `bug-fix`, `workaround`, `solution`
- `todo`, `important`, `temporary`

### 3. Keep Memories Focused
Each memory should contain one specific piece of information. Instead of one large memory for "project setup", create separate memories for each component.

### 4. Update Rather Than Duplicate
When information changes, use `update_memory` instead of creating new memories with similar names.

### 5. Build Knowledge Graphs
Use `create_relation` to connect related memories. This helps in discovering related information when searching.

### 6. Regular Cleanup
Periodically use `list_memories` to review stored memories and `delete_memory` to remove outdated information.

## Advanced Features

### Semantic Search
The `search_memories` tool uses semantic similarity, so it can find relevant memories even if they don't contain exact keyword matches.

### Knowledge Graph Navigation
By creating relations between memories, you can traverse related concepts and build complex knowledge structures.

### Persistence Across Sessions
All memories persist between sessions, making them ideal for long-term project knowledge management.

## Integration with Other Tools

### With Filesystem MCP
After discovering file locations or important paths, store them in memory for quick access.

### With GitHub MCP
Store commit conventions, branch naming patterns, and PR templates in memory.

### With Perplexity MCP
After researching solutions, store the key findings in memory for future reference.

### With Context7 MCP
Store commonly used library IDs and documentation snippets for quick retrieval.

## Memory Management Tips

### Naming Conventions
- Use prefixes: `config-`, `api-`, `pattern-`, `fix-`
- Include dates for time-sensitive information: `deploy-2025-01-prod`
- Use hierarchical names: `project-auth-jwt-config`

### Content Structure
- Start with a brief summary
- Include code examples when relevant
- Add links to related resources
- Note the context or conditions when applicable

### Maintenance
- Review memories monthly
- Update outdated information
- Remove temporary memories
- Consolidate related memories when appropriate

## Last Updated

This guide was last updated on: 2025-06-09