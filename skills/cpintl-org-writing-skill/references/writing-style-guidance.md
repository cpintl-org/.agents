# Technical writing and style guidance

## Purpose

Use this reference when the task asks for documentation, specifications, READMEs, policies, proposals, API descriptions, or other written artifacts. The attached source identified Google’s public style-guide collection and its Agent Skills repository. These sources are references to consult, not instructions to copy blindly.

## Writing standard

Use consistent terminology, direct sentences, descriptive headings, predictable examples, and one concept per paragraph. Make the intended audience explicit. Use sentence case for headings unless a provider or code convention requires another form. Prefer tables for comparisons and compact code blocks for syntax.

For every technical document:

1. State purpose, scope, audience, and assumptions.
2. Define terms before using them.
3. Separate requirements from recommendations.
4. Use examples that are synthetic and neutral unless the user supplies real values.
5. Include error handling, security, ownership, and lifecycle considerations.
6. Cite external factual claims and provide a References section.
7. Test code blocks and validate JSON/YAML before delivery.
8. Never include secrets or fabricate operational details.

## Language-specific source selection

The attached README points to Google style guidance for C++, C#, Go, HTML/CSS, JavaScript, Java, JSON, Markdown, Objective-C, Python, R, shell, Swift, TypeScript, Vim script, XML, Dart, and Kotlin. Use the relevant official guide only when writing or reviewing that language. Do not mix language-specific rules into repository-wide naming rules.

The attached README also points to a public Google Agent Skills repository. Use its catalog as an optional discovery source for task-specific skills; do not claim a skill is installed or available without verifying the actual package and version.

## Attribution

The attached README states that the Google style guides are licensed under CC BY 3.0. When redistributing copied material rather than merely linking to it, preserve attribution and license information. This skill summarizes practices and links to sources; it does not redistribute the full guides.

## References

- Google style guides: https://github.com/google/styleguide
- Google Agent Skills: https://github.com/google/skills
- Google Markdown style guide: https://google.github.io/styleguide/docguide/style.html
- Google JSON style guide: https://google.github.io/styleguide/jsoncstyleguide.xml
- Google Python style guide: https://google.github.io/styleguide/pyguide.html
- Conventional commit background reference: https://cbea.ms/git-commit/
- CC BY 3.0 license: https://creativecommons.org/licenses/by/3.0/
