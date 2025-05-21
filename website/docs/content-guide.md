---
title: "Content Management Guide"
description: "Guide for managing MoFA website content"
---

# MoFA Website Content Management

This directory contains the content files for the MoFA website. The content is organized by language and page type, making it easy to manage multilingual content.

## Directory Structure

```
site/
├── en/             # English content
│   └── home.md     # Homepage content in English
├── zh/             # Chinese content
│   └── home.md     # Homepage content in Chinese
└── README.md       # This guide
```

## How to Edit Content

### Content Format

All content files use Markdown format with YAML frontmatter at the top. The frontmatter contains structured data that defines the content for different sections of the website.

### Language Support

The website currently supports:
- English (`en`)
- Chinese (`zh`)

To add a new language, create a new directory with the language code and copy the content files from an existing language directory as templates.

### Editing Home Page

1. Locate the appropriate language file:
   - English: `en/home.md`
   - Chinese: `zh/home.md`

2. Edit the YAML frontmatter (content between `---` markers) to update the website content.

3. Each section is clearly marked with comments, such as:
   ```yaml
   # Hero section (top banner)
   hero:
     title: "Your title here"
     # ...
   ```

4. Be careful to maintain proper indentation and YAML syntax.

5. The text content at the bottom of the file (after the `---` closing marker) is used as additional content if needed.

## Content Sections

The home page content is organized into these main sections:

- **Basic Metadata**: Website title and description
- **Hero**: Top banner with title, subtitle, and call-to-action buttons
- **Core**: Core philosophy statement
- **Features**: List of features with icons
- **Design**: Design principles and architecture
- **Patterns**: Design patterns for AI agents
- **Quickstart**: Step-by-step guide
- **FAQ**: Frequently asked questions
- **CTA**: Call-to-action section at the bottom
- **Navigation & Footer**: Translation strings for nav and footer elements

## Adding New Pages

To add a new page:

1. Create a new Markdown file in each language directory
2. Define the appropriate frontmatter structure
3. Update the `config.ts` file if adding new content types
4. Create corresponding Astro pages in the `pages` directory

## Images

Images can be added to the `website/src/assets/images/` directory and referenced in your content.

## Need Help?

For questions about content management, please contact the MoFA team or refer to the project documentation. 