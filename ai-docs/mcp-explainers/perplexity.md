# Perplexity Tools Guide

This document provides an overview of Perplexity's capabilities through the Model Context Protocol (MCP) in VS Code. Perplexity is an AI research assistant that helps you find accurate, up-to-date information from across the web.

## Research Capabilities

### 1. Perplexity Ask
**Question:** "Can you research the latest advancements in quantum computing and summarize the key findings?"  
**Tool:** `f1e_perplexity_ask`  
**Description:** Sends a research query to Perplexity's AI, which searches the internet for the most relevant and recent information, then synthesizes the findings into a comprehensive answer.

## Use Cases

### Technical Research

**Question:** "What are the latest best practices for securing Node.js applications in 2025?"  
**Workflow:** Use `f1e_perplexity_ask` with a conversation that builds on this question.

### Problem Solving

**Question:** "I'm getting a 'Memory leak detected' error in my React application. What could be causing this and how can I fix it?"  
**Workflow:** Use `f1e_perplexity_ask` with detailed context about the error.

### Learning New Technologies

**Question:** "Explain the key differences between GraphQL and REST APIs, with examples of when to use each."  
**Workflow:** Use `f1e_perplexity_ask` to get a comprehensive comparison.

### Market Research

**Question:** "What are the most popular JavaScript frameworks in 2025 and what are their relative strengths?"  
**Workflow:** Use `f1e_perplexity_ask` to get current statistics and analysis.

### Algorithm and Implementation Research

**Question:** "What are efficient algorithms for text similarity matching and how would I implement them in Python?"  
**Workflow:** Use `f1e_perplexity_ask` to research algorithms and implementation approaches.

## Conversation-Based Research

The `f1e_perplexity_ask` tool accepts an array of messages, allowing you to have a conversation-like interaction. This is particularly useful for:

1. **Refining Research:** Start with a broad question, then ask follow-up questions based on the initial response.

2. **Providing Context:** Include previous messages to give Perplexity context about your project or specific requirements.

3. **Comparing Alternatives:** Ask about different approaches and then request a comparison.

4. **Diving Deeper:** Request more detailed information on specific aspects of the initial research.

## Sample Conversation Flow

**Initial Question:** "What are the most efficient ways to implement real-time updates in a web application?"

**Follow-up Questions:**
1. "Can you compare WebSockets, Server-Sent Events, and Long Polling in terms of performance and browser support?"
2. "What libraries are commonly used to implement WebSockets in a Node.js and React application?"
3. "Are there any security concerns specific to WebSockets I should be aware of?"
4. "Can you show an example of setting up a WebSocket server in Node.js with Express?"

## Best Practices for Using Perplexity

### 1. Be Specific
Provide as much context and specificity as possible in your questions to get more relevant answers.

### 2. Include Technical Details
When troubleshooting, include error messages, environment details, and steps to reproduce the issue.

### 3. Break Complex Questions Down
For complex research topics, start with a general question and then use follow-up questions to explore specific aspects.

### 4. Indicate Time Sensitivity
If you need current information, explicitly mention that you want the latest data or approaches (e.g., "as of 2025").

### 5. Request Sources
If you need to verify information, ask Perplexity to include its sources in the response.

### 6. Combine with Other Tools
For implementation details or specific documentation, combine Perplexity research with Context7 documentation and GitHub Copilot code generation.

## Integration with Task Master

Perplexity can be especially useful when combined with Task Master for research-backed task planning:

1. Use Perplexity to research best approaches for implementing a feature
2. Use Task Master's research-enabled tools to create well-informed tasks
3. Expand complex tasks with `f1e_expand_task` using the research parameter

## Last Updated

This guide was last updated on: 2025-05-16
