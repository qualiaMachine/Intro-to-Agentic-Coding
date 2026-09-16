# Introduction to Agentic Coding

A [Carpentries Workbench][workbench] lesson on working effectively and safely with AI
coding agents (Claude Code, GitHub Copilot, Cursor, OpenCode, …) as a researcher.

The lesson grew out of the 2-hour "Agentic Coding: (Developing) Best Practices"
workshop developed for the [ML Marathon](https://ml-marathon.wisc.edu/) at UW–Madison
by Chris Endemann, Tracy Reuter, and Tejvir Mann, and expands it into a self-study
resource.

## Core principles

- **Stay in the driver's seat.** The agent writes the code; you review it and decide
  what is merged to `main`.
- **Work feature by feature, not project by project.** A feature is one thing you can
  check. A whole-project prompt produces whole-project guesses.
- **Assume nothing; verify everything.** Rely on tests. Good data science practice
  still applies in full: code that runs without error and scores well can still be
  wrong, and faster iteration shortens the path to a misleading result as much as
  to a correct one.

## Episodes

The first eight episodes follow the two-hour workshop in order; the last three are
asynchronous reading.

1. What Is Agentic Coding?
2. Safety and Security: Limit What the Agent Can Access
3. Trust: Packages, Models, and Providers
4. Planning with Agents
5. Feature-Based Development and Good Prompting
6. Verification and Testing: No Escaping Good Data Science
7. MCP Tools and Skills: Extending Your Agent
8. Cost, Context, and Energy
9. Documentation: Notes to Your Future Self (and Your Agent)
10. Common Workflows
11. What the Research Shows, and Where This Leaves Us

## Building the lesson locally

This lesson uses [The Carpentries Workbench][workbench] (sandpaper). With R installed:

```r
install.packages(c("sandpaper", "varnish", "pegboard"),
                 repos = c("https://carpentries.r-universe.dev", getOption("repos")))
sandpaper::serve()
```

To (re)generate the standard Workbench GitHub Actions workflows, run
`sandpaper::update_github_workflows()`.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). This lesson is in
**pre-alpha**: content is under active development and feedback via issues is
especially valuable.

## Authors and contributors

- **Authors:** Chris Endemann (maintainer, endemann@wisc.edu), Tracy Reuter, Tejvir Mann
- **Contributors:** Zekai Otles (dev container setup on the setup page)

See [CITATION.cff](CITATION.cff) for how to cite the lesson.

## License

Lesson content: [CC-BY 4.0](LICENSE.md). Example code: MIT.

[workbench]: https://carpentries.github.io/sandpaper-docs/
