# Contributing to Midnight Agent Skills

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Node version, etc.)
- **Code examples** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title** describing the enhancement
- **Detailed description** of the proposed functionality
- **Use cases** explaining why this would be useful
- **Examples** of how it would work

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main`
3. **Make your changes**
4. **Test your changes**
5. **Update documentation** if needed
6. **Submit a pull request**

#### Pull Request Guidelines

- Follow the existing code style
- Include tests if applicable
- Update documentation
- Keep commits focused and atomic
- Write clear commit messages

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/midnight-agent-skills.git
cd midnight-agent-skills

# No build step required - pure markdown documentation
```

## Documentation Style Guide

### File Naming
- Use lowercase with hyphens: `quick-start.md`
- Be descriptive: `authentication-patterns.md`

### Content Structure
```markdown
# Title

## Overview
Brief description

## Section 1
Content with examples

### Subsection
More specific content

## Resources
Links to related docs
```

### Code Examples
- Include language identifier: \`\`\`typescript
- Show complete, working examples
- Add comments for clarity
- Include both ✅ correct and ❌ wrong examples

### Cross-References
```markdown
See [other-guide.md](references/other-guide.md) for details.
```

## Testing Changes

### Validate Structure
```bash
# Run validation tests
bash /tmp/final_test.sh
```

### Check Cross-References
```bash
# Verify all links work
for skill in midnight-*; do
  grep -o 'references/[a-z-]*\.md' "$skill/SKILL.md" | \
  while read ref; do
    [ -f "$skill/$ref" ] || echo "Broken: $skill/$ref"
  done
done
```

### Test with Skills CLI
```bash
# Test installation
npx skills add ./midnight-compact
npx skills list
```

## Commit Message Guidelines

### Format
```
type(scope): subject

body

footer
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting changes
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples
```
feat(compact): add debugging guide

Add comprehensive guide for debugging Compact contracts including
common errors and solutions.

Closes #123
```

```
docs(api): fix typo in authentication-patterns.md

Fix incorrect method name in wallet connection example.
```

## Adding New Content

### Adding a New Reference

1. Create the markdown file in appropriate `references/` directory
2. Follow the documentation style guide
3. Add entry to `SKILL.md` with summary
4. Test all code examples
5. Validate cross-references

### Adding a New Skill

1. Create new directory: `midnight-newskill/`
2. Add `SKILL.md` with YAML frontmatter
3. Create `references/` directory
4. Add reference files
5. Update main `README.md`
6. Add to `package.json` skills array

## Review Process

1. **Automated checks** run on PR
2. **Maintainer review** for content quality
3. **Testing** of examples and links
4. **Approval** and merge

## Questions?

- Open an issue for questions
- Join discussions on GitHub
- Check existing documentation first

## Recognition

Contributors are:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Mentioned in documentation

Thank you for contributing! 🙏
