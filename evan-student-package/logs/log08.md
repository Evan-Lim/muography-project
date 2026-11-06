# Week 8 — Report, slides, and reproducibility

**Dates:** Week 8 of the eight-week plan
**Hours spent:** 8

## What I did

Wrote `docs/final_report.tex` using the official MYSSP 2026 `myssp` template
and the official `docs/myssp.sty` style file, with `docs/references.bib`;
compiled it with `pdflatex`/`bibtex`/`pdflatex`.
Restructured the paper to the MYSSP-required sections: Abstract, Introduction,
Methodology, Data Collection, Analysis, Results, Discussion and Conclusion,
with acknowledgements, references and an appendix. Wrote `EXPLAINER.md` for a
general reader, the **12-page** demo-day slide specification and full script in
`docs/slides_and_script.tex`, and the 2.5-minute summary-video script in
`docs/video_script.md`. Re-ran notebooks 02–05 with
`jupyter nbconvert --execute` from fresh kernels, checked that no cell raised an
exception, and confirmed every figure in the report exists in `figures/`. Added
`requirements.txt`, a results summary JSON, and the figure-to-notebook mapping.

## What I found

- The full pipeline is reproducible: notebooks 02–05 execute without errors in
  about two minutes on the project machine, with seed 0.
- The report's headline is 13.4 days (interpolated 13.37, exact 13.33). The
  exact-solid-angle systematic is 15.4 days; the whole-image global value is
  59.5 days.
- All four required studies and the Malaysian extension produce figures; the
  extra studies (area, density, global significance) are in the report's
  supplementary appendix and in `results_summary.json`.
- The paper body is 10 pages, within the MYSSP limit; references and the
  appendix are additional. The 12-slide deck is title + 10 content +
  thank-you/references, with a 15-minute script.

## What went wrong / what I don't understand

- The first report compile failed because a killed `pdflatex` left a corrupted
  `.aux`/`.out` file. Deleting the auxiliary files and recompiling fixed it.
  This is worth remembering: a LaTeX error at `\begin{document}` can be a
  corrupted auxiliary file, not a source error.
- The `FigureCanvasAgg is non-interactive` warning appears when notebooks are
  executed headlessly. It is harmless; the notebooks suppress it so the saved
  outputs are clean.
- The official `myssp.sty` was supplied separately and is now included as
  `docs/myssp.sty`; it replaces the temporary fallback used during drafting.

## Final checklist

- [x] Shared functions implemented and documented.
- [x] Notebooks 02–05 run from fresh kernels with no errors.
- [x] Before/after pair, exposure curve, null control, and all four studies.
- [x] Malaysian extension and three extra studies.
- [x] Official-format LaTeX report, 10-page body, compiled with BibTeX.
- [x] 12-page slide specification, extensive TikZ diagrams, and full script.
- [x] 2.5-minute summary-video script and shot list.
- [x] Sixteen-question Q&A preparation sheet.
- [x] `EXPLAINER.md` for a lay reader.
- [x] Requirements, seed, results JSON, code-availability mapping.
