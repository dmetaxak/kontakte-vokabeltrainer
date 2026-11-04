# Kontakte Vokabeltrainer: source

**Want your own copy?** Follow the getting-started guide Danaé shared. Copies are built from the `stable` branch. The build-and-publish steps Claude follows are in `CLAUDE.md`.

The published trainer is one self-contained HTML file (artifact "Kontakte Vokabeltrainer"). This folder is the source it is built from.

## Files
- `quiz-template.html`: the whole app (HTML, CSS, JavaScript). Placeholders `/*VOCABDATA*/`, `/*VERBDATA*/`, `/*ACCDATA*/`, `/*PRONDATA*/` are replaced at build time. The `//PURE_START ... //PURE_END` block holds grading logic that is also unit-tested in node.
- `build.py`: reads the data files below, validates them (noun genders, plural words, sentences), builds `kontakte-vokabeltrainer.html` and extracts `pure.js` for tests.
- `data/vocab.md`: the vocabulary table (German | English | type | plural | chapter | notes). 
- `examples.txt`: one example sentence per vocab row, in the same order as `vocab.md` (`German|English`).
- `einfuehrung.txt`: extra Einführung words (`;;`-separated).
- `verbs.txt`, `cloze.txt`: verb data and one fill-in sentence per verb.
- `acc.txt`: case-endings sentences (base;;case;;noun;;sentence;;English).
- `pron.txt`: personal-pronoun sentences (case;;person;;sentence with ___;;English). Person is 1s 2s 3m 3f 3n 1p 2p 3p fo; the answer comes from the pronoun table in the template (`PRON_FORMS`).
- Modal verbs (können, wollen, müssen, sollen, dürfen, möchten) live in `verbs.txt` with a full paradigm and no auxiliary/participle, which keeps them out of the Perfekt drill.
- `plural_en.py`: generates English plurals for the plural words (with hand-written exceptions).
- `plural_ex.txt`: one example sentence per plural form.

Plural forms are built as rows of their own (with `pl` = the singular), but the app folds each one into its singular: one word, one score. Vocab quizzes show the plural form about 40% of the time (a missed form comes back as the same form), and the plural drill scores to the singular too. Scores recorded under a plural's old id by earlier versions are merged into the singular's score when read; nothing in the db is rewritten.

## Build
Data files live in `data/`. Run `python3 build.py` from the repo root; it writes `kontakte-vokabeltrainer.html` (publish to the same artifact URL) and `pure.js` (for tests).

## Storage (artifact db, per user)
Docs under `data/users/<uid>/`: `progress` (vocab, noun genders, plurals; one entry per word, with legacy plural entries merged in on read), `verbs`, `grammar` (case endings), `mistakes` (log of misses, skips, hint use and grader overrides), `days` (practice days for the streak: date -> rounds finished).
