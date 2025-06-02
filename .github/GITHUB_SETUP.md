# GitHub Copilot Configuration

This directory contains configuration files for GitHub Copilot to understand our project's coding standards and best practices.

## Structure

- `copilot-instructions.md` - Main instructions file for the entire workspace
- `/instructions/` - Directory containing specific instruction files for different file types or tasks
- `/prompts/` - Directory containing reusable prompt files for common development tasks

## Instruction Files

These files tell GitHub Copilot about our coding standards, project structure, and best practices:

- `copilot-instructions.md` - Main project-wide instructions
- `instructions/python_style.instructions.md` - Python code style guidelines
- `instructions/testing.instructions.md` - Testing standards and practices
- `instructions/cli.instructions.md` - CLI development guidelines

## Prompt Files

These files provide reusable templates for common development tasks:

- `prompts/generate_tests.prompt.md` - Generate comprehensive test files
- `prompts/add_feature.prompt.md` - Add new features to the project
- `prompts/code_review.prompt.md` - Review and refactor code

## Usage

### Using Instruction Files

Instruction files are automatically applied to relevant files based on the `applyTo` pattern in their front matter. The main `copilot-instructions.md` file is applied to all requests when enabled in settings.

### Using Prompt Files

To use a prompt file:

1. In the Chat view, type `/` followed by the prompt file name
2. Or use the Command Palette (Ctrl+Shift+P) and select "Chat: Run Prompt"
3. Or open the prompt file and click the play button in the editor title

### Configuration

The VS Code settings that enable these features are in `.vscode/settings.json`:

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "chat.promptFiles": true,
  "chat.instructionsFilesLocations": [".github/instructions"],
  "chat.promptFilesLocations": [".github/prompts"]
}
```
