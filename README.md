# Introduction to Agentic Coding

A [Carpentries Workbench][workbench] lesson on working effectively and safely with AI
coding agents (Claude Code, GitHub Copilot, Cursor, OpenCode, …) as a researcher.

The lesson grew out of the 2-hour "Agentic Coding Best Practices" workshop developed for
the [ML Marathon](https://ml-marathon.wisc.edu/) at UW–Madison by Tracy Reuter, Tejvir
Mann, Chris Endemann, and Zain Waseem, and expands it into a self-study resource.

## Core themes

- **Stay in the driver's seat** — the agent types; you decide.
- **Feature-driven development** — well-scoped, verifiable tasks over project-sized prompts.
- **No escaping good data science** — explore your data, know your distributions, know
  what your models are telling you; code that runs clean and scores great can still be wrong.
- **Assume nothing; verify everything** — faster iteration means faster results *and* faster
  misleading.

## Episodes

1. What Does "Agentic" Mean?
2. Words of Caution: Safety, Security, and Policy
3. Trust: Packages, Models, and Providers
4. Early Project Planning
5. Underspecification and Feature-Driven Development
6. Verification and Review: No Escaping Good Data Science
7. Documentation: Notes to Your Future Self (and Your Agent)
8. Common Workflows
9. Cost, Context, and Energy
10. What the Research Shows, and Where This Leaves Us

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

## Maintainers

- Chris Endemann (endemann@wisc.edu)

## License

Lesson content: [CC-BY 4.0](LICENSE.md). Example code: MIT.

[workbench]: https://carpentries.github.io/sandpaper-docs/
