# Context7 Tools Guide

This document provides an overview of Context7's capabilities through the Model Context Protocol (MCP) in VS Code. Context7 specializes in retrieving and providing relevant documentation and code examples from libraries and frameworks.

## Library Documentation

### 1. Resolve Library ID
**Question:** "I need to find the correct library ID for React before I can access its documentation."  
**Tool:** `f1e_resolve-library-id`  
**Description:** Before using Context7 to retrieve library documentation, you must first resolve the exact library identifier. This tool searches for the most relevant library matching your query and returns its Context7-compatible ID.

### 2. Get Library Documentation
**Question:** "Retrieve documentation about React hooks so I can understand how to use useEffect."  
**Tool:** `f1e_get-library-docs`  
**Description:** Once you have a Context7-compatible library ID, this tool fetches comprehensive documentation from that library, focusing on a specific topic if provided.

## Use Cases

### Framework and Library Research

**Question:** "I need to understand how to implement authentication in NextJS."  
**Workflow:**
1. Use `f1e_resolve-library-id` with "nextjs"
2. Use the returned ID with `f1e_get-library-docs` and specify "authentication" as the topic

### API Reference

**Question:** "What are the available options for the fetch API in JavaScript?"  
**Workflow:**
1. Use `f1e_resolve-library-id` with "javascript fetch"
2. Use the returned ID with `f1e_get-library-docs` and specify "options" as the topic

### Component Documentation

**Question:** "How do I use Redux hooks in a React application?"  
**Workflow:**
1. Use `f1e_resolve-library-id` with "redux"
2. Use the returned ID with `f1e_get-library-docs` and specify "hooks" as the topic

### Debugging Assistance

**Question:** "I'm getting an error with Mongoose schema validation. How should I properly define schemas?"  
**Workflow:**
1. Use `f1e_resolve-library-id` with "mongoose"
2. Use the returned ID with `f1e_get-library-docs` and specify "schema validation" as the topic

## Best Practices for Using Context7

### 1. Use Specific Library Names
When using `f1e_resolve-library-id`, be as specific as possible about the library name. For popular libraries with many forks or versions, include the organization name (e.g., "facebook/react" instead of just "react").

### 2. Check Available Libraries
If you're not sure about the exact library name, the `f1e_resolve-library-id` tool returns several matching options. Review these options to select the most appropriate one based on:
- Number of GitHub stars (indicating popularity)
- Number of code snippets (indicating documentation coverage)
- Description relevance

### 3. Focus Topics for Better Results
When using `f1e_get-library-docs`, specify a focused topic to get more relevant documentation rather than broad overviews.

### 4. Understand Limitations
Context7 provides documentation as it was available at the time of its latest update. For cutting-edge features or very recent changes, the documentation might not be complete.

### 5. Combine with Other Tools
For the best results, combine Context7's documentation with Perplexity research for up-to-date information or GitHub repository search for specific code implementations.

## Example Workflow

**Task:** Implementing GraphQL queries in a React application

1. **Resolve Library ID for Apollo Client:**
   ```
   Use f1e_resolve-library-id with "apollo client graphql"
   ```

2. **Get Documentation on Queries:**
   ```
   Use f1e_get-library-docs with the returned ID and "queries" as the topic
   ```

3. **Resolve Library ID for React Documentation:**
   ```
   Use f1e_resolve-library-id with "react"
   ```

4. **Get Documentation on Integrating with External APIs:**
   ```
   Use f1e_get-library-docs with the returned ID and "data fetching" as the topic
   ```

5. **Apply the Documentation to Your Project**

## Last Updated

This guide was last updated on: 2025-05-16
