# NEWS

## 2026-11-10

- Added PowerPoint output built on the EU Policy Lab corporate template.
  - `make pptx` writes `_export/<SLUG>.pptx`; `make` builds both PDF and PPTX; `make view-pptx` opens it.
  - `make_reference.py` generates `reference.pptx` (gitignored) from `eu_policy_lab_corporate_template.pptx`: renames layouts to the names pandoc expects (Title Slide, Two Content, Content with Caption), adds a Section Header layout and drops the example slides.
  - `_output.yml`: `powerpoint_presentation` uses `reference.pptx` with `slide_level: 2`.
- `SLUG` no longer includes the extension (`make SLUG=foo` gives `foo.pdf` and `foo.pptx`).
- `presentation.Rmd`: the two-column synthesis slide uses pandoc `columns` divs so it maps to the "Two Content" layout (also works in Beamer).
