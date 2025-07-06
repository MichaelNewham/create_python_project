# Brave Search Tools Guide

This document provides an overview of Brave Search's capabilities through the Model Context Protocol (MCP) in VS Code. Brave Search provides privacy-focused web search capabilities with real-time results from across the internet.

## Search Capabilities

### 1. Web Search
**Question:** "Search for the latest React 19 features and updates."  
**Tool:** `brave_web_search`  
**Description:** Performs a web search using Brave's search engine and returns relevant results including titles, URLs, descriptions, and publication dates.

### 2. Local Search
**Question:** "Find coffee shops near San Francisco."  
**Tool:** `brave_local_search`  
**Description:** Searches for local businesses, services, and points of interest in a specific geographic area.

### 3. News Search
**Question:** "What are the latest news about TypeScript 5.0?"  
**Tool:** `brave_news_search`  
**Description:** Searches specifically for recent news articles and press releases, with results sorted by date.

## Use Cases

### Technical Research

**Question:** "Find the latest tutorials on implementing WebSockets with Node.js."  
**Workflow:** Use `brave_web_search` with query "WebSockets Node.js tutorial 2025" to get current tutorials and guides.

### Troubleshooting and Error Resolution

**Question:** "Search for solutions to 'npm ERR! code ERESOLVE' error."  
**Workflow:** Use `brave_web_search` with the exact error message to find Stack Overflow posts, GitHub issues, and blog posts with solutions.

### Library and Framework Comparison

**Question:** "Compare Vite vs Webpack performance benchmarks."  
**Workflow:** Use `brave_web_search` to find recent performance comparisons and benchmarks between the two build tools.

### Security and Vulnerability Research

**Question:** "Search for recent security vulnerabilities in Express.js."  
**Workflow:** Use `brave_news_search` to find recent security advisories and CVE reports.

### Best Practices Discovery

**Question:** "What are the current best practices for React performance optimization?"  
**Workflow:** Use `brave_web_search` with "React performance optimization best practices 2025" for up-to-date recommendations.

### API Documentation and Examples

**Question:** "Find examples of using the Stripe API with TypeScript."  
**Workflow:** Use `brave_web_search` to find code examples, tutorials, and implementation guides.

## Search Operators and Tips

### 1. Exact Phrase Matching
Use quotes for exact phrases: `"error handling in async functions"`

### 2. Site-Specific Search
Search within specific sites: `site:github.com React hooks examples`

### 3. Exclude Terms
Use minus sign to exclude: `JavaScript frameworks -jQuery`

### 4. Filetype Search
Find specific file types: `filetype:pdf TypeScript handbook`

### 5. Time-Based Filtering
Request recent results by including time markers: `React 18 features 2025`

## Best Practices for Using Brave Search

### 1. Be Specific with Queries
Include specific version numbers, error codes, or technical terms for more relevant results.

### 2. Use Multiple Searches
Refine your search with follow-up queries based on initial results to dig deeper into topics.

### 3. Combine Search Types
Use `brave_web_search` for general information and `brave_news_search` for recent developments.

### 4. Verify Information
Cross-reference search results, especially for critical technical information or security-related topics.

### 5. Include Context
Add programming language, framework, or platform context to your searches for better results.

### 6. Check Publication Dates
Pay attention to result dates, especially for rapidly evolving technologies.

## Integration with Other Tools

### With Perplexity MCP
Use Brave Search for initial discovery, then use Perplexity for deeper analysis and synthesis of the findings.

### With Context7 MCP
After finding relevant libraries through Brave Search, use Context7 to get detailed documentation.

### With Memory MCP
Store useful search results, solutions, and resources in memory for future reference.

### With Filesystem MCP
After finding code examples, use filesystem tools to implement them in your project.

## Advanced Search Strategies

### Research Workflow

1. **Initial Broad Search:** Start with a general query to understand the landscape
2. **Targeted Searches:** Narrow down with specific technical terms
3. **Solution Verification:** Search for multiple sources confirming the same solution
4. **Implementation Examples:** Look for practical code examples
5. **Recent Updates:** Check for recent changes or deprecations

### Debugging Workflow

1. **Error Message Search:** Search with the exact error message
2. **Context Addition:** Add your tech stack to the search
3. **GitHub Issues:** Use `site:github.com` to find related issues
4. **Stack Overflow:** Search for similar questions and accepted answers
5. **Official Documentation:** Verify solutions against official docs

### Learning Workflow

1. **Overview Search:** Start with "introduction to [topic]"
2. **Tutorial Search:** Look for step-by-step guides
3. **Best Practices:** Search for recommended patterns and practices
4. **Common Pitfalls:** Search for "common mistakes" or "gotchas"
5. **Advanced Topics:** Progress to advanced implementations

## Privacy Benefits

Brave Search provides several privacy advantages:
- No tracking of search queries
- No user profiling
- Independent search index
- No filter bubble effects
- Anonymous searching by default

## Limitations and Considerations

### API Key Requirement
Brave Search MCP requires a valid BRAVE_API_KEY. Sign up at https://brave.com/search/api/ to obtain one.

### Rate Limits
Be aware of API rate limits when performing multiple searches in succession.

### Regional Variations
Local search results may vary by region and availability of local data.

## Last Updated

This guide was last updated on: 2025-06-09