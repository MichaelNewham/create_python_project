#!/usr/bin/env python3
"""
Intelligent Context Gathering Module

This module provides the enhanced context gathering system with adaptive questions
and interactive preference tables.
"""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from create_python_project.utils import ai_integration, ai_prompts
from create_python_project.utils.cli import enhanced_input
from create_python_project.utils.preference_tables import (
    create_preference_table,
    display_preference_summary,
)

console = Console()


class IntelligentContextGatherer:
    """Handles the intelligent context gathering workflow."""

    def __init__(
        self, project_name: str, project_description: str, project_info: dict[str, Any]
    ):
        self.project_name = project_name
        self.project_description = project_description
        self.project_info = project_info
        self.context_data: dict[str, Any] = {
            "project_name": project_name,
            "project_description": project_description,
            "questions": [],
            "answers": [],
            "preference_data": [],
            "comments": [],
        }

    def conduct_analysis(self) -> bool:
        """Conduct the Project Instigator analysis to generate adaptive questions."""
        console.print("\n🤖 Project Instigator Analysis Phase 🤖")
        console.print("─" * 80)

        # Check AI providers availability
        with console.status(
            "[bold cyan]Checking available AI providers...[/bold cyan]"
        ):
            providers = ai_integration.get_available_ai_providers()
            import time

            time.sleep(1)  # Visual feedback

        if not providers:
            console.print(
                "[bold red]❌ No AI providers available for analysis.[/bold red]"
            )
            console.print(
                "[yellow]⚠️ Falling back to manual context gathering...[/yellow]"
            )
            return self._fallback_manual_questions()

        # Get Project Instigator analysis
        with Progress(
            SpinnerColumn(),
            TextColumn(
                "[bold cyan]⚡ Analyzing project context and generating adaptive questions...[/bold cyan]"
            ),
            console=console,
        ) as progress:
            task = progress.add_task("Analysis", total=None)

            # Get random AI provider for analysis
            success, provider = ai_integration.get_random_ai_provider(providers)
            if not success or provider is None:
                console.print(
                    "[bold red]❌ Failed to get AI provider for analysis.[/bold red]"
                )
                return self._fallback_manual_questions()

            # Generate analysis prompt
            analysis_prompt = ai_prompts.get_project_instigator_analysis_prompt(
                self.project_name, self.project_description, self.project_info
            )

            # Get analysis response
            analysis_success, analysis_response = provider.generate_response(
                analysis_prompt
            )
            progress.update(task, completed=True)

        if not analysis_success:
            console.print(
                f"[bold red]❌ Analysis failed: {analysis_response}[/bold red]"
            )
            return self._fallback_manual_questions()

        # Parse the analysis response
        self.analysis_response = analysis_response
        console.print("[green]✅ Project analysis complete![/green]")

        # Display analysis summary
        self._display_analysis_summary()

        return True

    def _display_analysis_summary(self) -> None:
        """Display the Project Instigator analysis summary."""
        # Extract key information from analysis response
        lines = self.analysis_response.split("\n")

        domain_analysis = ""
        complexity_assessment = ""

        # Simple parsing - look for key sections
        current_section = ""
        for line in lines:
            if "Domain Analysis:" in line:
                current_section = "domain"
            elif "Complexity Assessment:" in line:
                current_section = "complexity"
            elif "Strategic Considerations:" in line:
                current_section = "strategic"
            elif "5 Iterative Questions Framework:" in line:
                current_section = "questions"
            elif line.strip() and current_section == "domain":
                domain_analysis += line.strip() + " "
            elif line.strip() and current_section == "complexity":
                complexity_assessment += line.strip() + " "

        # Display summary
        console.print("\n## Project Instigator Analysis Summary")

        if domain_analysis:
            domain_panel = Panel(
                Text(domain_analysis.strip(), style="white"),
                title="Domain Analysis",
                title_align="left",
                border_style="blue",
            )
            console.print(domain_panel)

        if complexity_assessment:
            complexity_panel = Panel(
                Text(complexity_assessment.strip(), style="white"),
                title="Complexity Assessment",
                title_align="left",
                border_style="yellow",
            )
            console.print(complexity_panel)

    def conduct_iterative_questions(self) -> bool:
        """Conduct the 5 iterative questions with preference tables."""
        console.print("\n## Enhanced Context Gathering - Interactive Preference System")
        console.print("─" * 80)

        # Parse questions from analysis response or use fallback
        questions = self._parse_questions_from_analysis()

        if not questions:
            console.print(
                "[yellow]⚠️ Could not parse questions from analysis. Using fallback questions.[/yellow]"
            )
            questions = self._get_fallback_questions()

        # Debug information about what we found
        console.print(f"[dim]Found {len(questions)} questions to process[/dim]")

        # Conduct each question iteratively
        for i, question_data in enumerate(questions, 1):
            console.print(f"\n### Question {i}: {question_data['title']}")

            # Show context
            context_panel = Panel(
                Text(question_data["context"], style="italic"),
                title="Context",
                title_align="left",
                border_style="cyan",
            )
            console.print(context_panel)

            # Get user's textual answer first
            answer = enhanced_input(question_data["question"])
            self.context_data["answers"].append(answer)

            # Create and run preference table
            preferences, comment = create_preference_table(
                title=question_data["title"],
                categories=question_data["categories"],
                context=f"Building on your answer: {answer[:100]}...",
            )

            # Store results
            self.context_data["preference_data"].append(
                {
                    "question": question_data["question"],
                    "answer": answer,
                    "preferences": preferences,
                    "comment": comment,
                }
            )

            # Display summary
            display_preference_summary(preferences, comment)

            # Update context for next question
            if i < len(questions):
                questions[i][
                    "context"
                ] = f"Building on your {question_data['title'].lower()} insights: {answer[:50]}..."

        console.print("\n[green]✅ All contextual questions completed![/green]")
        return True

    def _parse_questions_from_analysis(self) -> list[dict[str, Any]]:
        """Parse questions from the AI analysis response with robust fallback."""
        questions = []

        # This is a robust parser that handles various AI response formats
        lines = self.analysis_response.split("\n")

        current_question: dict[str, Any] = {}
        in_question_section = False

        for line in lines:
            line = line.strip()

            # Look for various forms of question framework headers
            if any(
                header in line.lower()
                for header in [
                    "5 iterative questions framework",
                    "iterative questions framework",
                    "question framework",
                    "questions framework",
                    "adaptive questions",
                ]
            ):
                in_question_section = True
                continue

            if in_question_section and line.startswith("**Question"):
                # Save previous question if exists
                if current_question and "title" in current_question:
                    questions.append(current_question)

                # Start new question
                current_question = {}
                # Extract title from "**Question 1: [Title]**" or "**Question 1: Title**"
                title_start = line.find("[") + 1
                title_end = line.find("]")
                if title_start > 0 and title_end > title_start:
                    current_question["title"] = line[title_start:title_end]
                else:
                    # Try to extract title after the colon
                    colon_pos = line.find(":")
                    if colon_pos > 0:
                        title_part = line[colon_pos + 1 :].strip().rstrip("*")
                        current_question["title"] = title_part

            elif in_question_section and line.startswith("Context:"):
                current_question["context"] = line[8:].strip()

            elif in_question_section and line.startswith("Question:"):
                current_question["question"] = line[9:].strip()

            elif in_question_section and line.startswith(
                "Preference Table Categories:"
            ):
                # Parse categories - simple implementation
                # This would need more sophisticated parsing in practice
                # For now, use default categories based on title
                current_question["categories"] = self._get_default_categories(
                    current_question.get("title", "")
                )

        # Add the last question
        if current_question and "title" in current_question:
            questions.append(current_question)

        # If we still don't have questions, try a different approach
        if not questions:
            # Look for any question patterns in the text
            questions = self._extract_questions_from_text()

        return questions if questions else []

    def _extract_questions_from_text(self) -> list[dict[str, Any]]:
        """Extract questions from unstructured text when formal parsing fails."""
        questions = []

        # Common question patterns to look for
        question_patterns = [
            ("data sources", "Data Sources & Inputs"),
            ("core functionality", "Core Functionality"),
            ("user experience", "User Experience"),
            ("technical approach", "Technical Approach"),
            ("deployment", "Deployment & Privacy"),
            ("privacy", "Privacy & Security"),
        ]

        # Look for sections that might contain questions
        lines = self.analysis_response.split("\n")

        for _i, line in enumerate(lines):
            line_lower = line.lower()

            # Check if this line contains a question pattern
            for pattern, title in question_patterns:
                if pattern in line_lower and ("?" in line or "question" in line_lower):
                    # Found a potential question
                    question_text = line.strip()
                    if question_text.endswith("?"):
                        questions.append(
                            {
                                "title": title,
                                "question": question_text,
                                "context": f"Based on the project analysis, this helps understand {pattern.replace('_', ' ')}.",
                                "categories": self._get_default_categories(title),
                            }
                        )
                        break

        return questions

    def _get_default_categories(self, question_title: str) -> list[str]:
        """Get default categories based on question title."""
        category_mapping = {
            "Data Sources": [
                "API direct integration",
                "Manual file uploads",
                "Real-time data streaming",
                "Batch processing",
                "Third-party service integration",
                "Manual data entry",
                "Automated data collection",
            ],
            "Core Functionality": [
                "Automatic processing",
                "Rule-based logic",
                "Machine learning features",
                "User customization",
                "Real-time updates",
                "Batch operations",
                "Advanced analytics",
            ],
            "User Experience": [
                "Web dashboard",
                "Mobile app",
                "Desktop application",
                "Command-line interface",
                "Email notifications",
                "In-app notifications",
                "Minimal interface",
            ],
            "Technical Approach": [
                "Cloud-based deployment",
                "Self-hosted solution",
                "Hybrid approach",
                "Microservices architecture",
                "Monolithic application",
                "Serverless functions",
                "Container deployment",
            ],
            "Privacy": [
                "Local data storage",
                "Encrypted cloud storage",
                "Self-hosted deployment",
                "Data export features",
                "Multi-user support",
                "Two-factor authentication",
                "Privacy-first design",
            ],
        }

        # Simple matching based on title
        for key, categories in category_mapping.items():
            if key.lower() in question_title.lower():
                return categories

        # Default fallback
        return [
            "High priority",
            "Medium priority",
            "Low priority",
            "Optional feature",
            "Not needed",
            "Consider later",
            "Essential requirement",
        ]

    def _get_fallback_questions(self) -> list[dict[str, Any]]:
        """Get fallback questions if AI analysis fails."""
        return [
            {
                "title": "Data Sources & Inputs",
                "context": "Understanding your data sources helps design the optimal processing pipeline.",
                "question": "What types of data or inputs will your system need to handle?",
                "categories": [
                    "API direct integration",
                    "Manual file uploads",
                    "Real-time data streaming",
                    "Batch processing",
                    "Third-party service integration",
                    "Manual data entry",
                    "Automated data collection",
                ],
            },
            {
                "title": "Core Functionality",
                "context": "Building on your data sources, what core processing capabilities do you need?",
                "question": "What are the key features and processing capabilities you want?",
                "categories": [
                    "Automatic processing",
                    "Rule-based logic",
                    "Machine learning features",
                    "User customization",
                    "Real-time updates",
                    "Batch operations",
                    "Advanced analytics",
                ],
            },
            {
                "title": "User Experience",
                "context": "Based on your functionality needs, how do you want to interact with the system?",
                "question": "What type of user interface and interaction model do you prefer?",
                "categories": [
                    "Web dashboard",
                    "Mobile app",
                    "Desktop application",
                    "Command-line interface",
                    "Email notifications",
                    "In-app notifications",
                    "Minimal interface",
                ],
            },
            {
                "title": "Technical Implementation",
                "context": "Considering your interface preferences, what technical approach fits your needs?",
                "question": "What technical architecture and deployment model do you prefer?",
                "categories": [
                    "Cloud-based deployment",
                    "Self-hosted solution",
                    "Hybrid approach",
                    "Microservices architecture",
                    "Monolithic application",
                    "Serverless functions",
                    "Container deployment",
                ],
            },
            {
                "title": "Privacy & Security",
                "context": "Based on your technical approach, what are your privacy and security requirements?",
                "question": "What privacy and security considerations are important to you?",
                "categories": [
                    "Local data storage",
                    "Encrypted cloud storage",
                    "Self-hosted deployment",
                    "Data export features",
                    "Multi-user support",
                    "Two-factor authentication",
                    "Privacy-first design",
                ],
            },
        ]

    def _fallback_manual_questions(self) -> bool:
        """Fallback to manual question gathering if AI analysis fails."""
        console.print("\n[yellow]⚠️ Using manual context gathering...[/yellow]")

        # Simple manual questions
        questions = [
            "What are the main data sources or inputs for your project?",
            "What core functionality do you want to implement?",
            "How do you want users to interact with your system?",
            "What technical constraints or preferences do you have?",
            "What privacy or security requirements are important?",
        ]

        for i, question in enumerate(questions, 1):
            console.print(f"\n[bold cyan]Question {i}:[/bold cyan] {question}")
            answer = enhanced_input("Your answer")
            self.context_data["answers"].append(answer)

        return True

    def get_context_data(self) -> dict[str, Any]:
        """Get the collected context data."""
        return self.context_data.copy()

    def get_structured_context_summary(self) -> str:
        """Get a structured summary of the context for expert consultation."""
        summary = f"""
# Enhanced Context Summary

**Project:** {self.project_name}
**Initial Description:** {self.project_description}

## Structured Preference Data:

"""

        preference_data = self.context_data.get("preference_data", [])
        for i, data in enumerate(preference_data, 1):
            if isinstance(data, dict):
                summary += f"""
### Question {i}: {data.get('question', 'Unknown')}
**Answer:** {data.get('answer', 'No answer provided')}

**Preference Rankings:**
"""
                preferences = data.get("preferences", {})
                if isinstance(preferences, dict) and "selections" in preferences:
                    selections = preferences.get("selections", {})
                    rating_labels = preferences.get("rating_labels", [])
                    if isinstance(selections, dict) and isinstance(rating_labels, list):
                        for category, rating in selections.items():
                            if isinstance(rating, int) and rating <= len(rating_labels):
                                rating_label = rating_labels[rating - 1]
                            else:
                                rating_label = str(rating)
                            summary += f"- {category}: {rating}/5 ({rating_label})\n"

                comment = data.get("comment")
                if comment:
                    summary += f"\n**Additional Comments:** {comment}\n"

        return summary


def conduct_intelligent_context_gathering(
    project_name: str, project_description: str, project_info: dict[str, Any]
) -> tuple[bool, dict[str, Any]]:
    """
    Conduct the enhanced context gathering workflow.

    Args:
        project_name: Name of the project
        project_description: Initial project description
        project_info: Project information dictionary

    Returns:
        Tuple of (success, context_data)
    """
    gatherer = IntelligentContextGatherer(
        project_name, project_description, project_info
    )

    # Conduct analysis
    if not gatherer.conduct_analysis():
        return False, {}

    # Conduct iterative questions
    if not gatherer.conduct_iterative_questions():
        return False, {}

    return True, gatherer.get_context_data()
