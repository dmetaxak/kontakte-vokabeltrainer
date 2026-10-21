# Kontakte Vokabeltrainer: source

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
- `plural_ex.txt`: one example sentence per plural word.

## Build
Data files live in `data/`. Run `python3 build.py` from the repo root; it writes `kontakte-vokabeltrainer.html` (publish to the same artifact URL) and `pure.js` (for tests).

## Storage (artifact db, per user)
Docs under `data/users/<uid>/`: `progress` (vocab, noun genders, plurals), `verbs`, `grammar` (case endings), `mistakes` (log of misses, skips, hint use and grader overrides), `days` (practice days for the streak: date -> rounds finished).
