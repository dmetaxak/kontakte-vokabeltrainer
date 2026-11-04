# KV Trainer: instructions for Claude

This repo is the source of KV Trainer (Kontakte Vokabeltrainer), a German practice app that runs as a Claude artifact. Danaé maintains it. Classmates each run their own copy, built from the `stable` branch.

Work out which case you're in before doing anything:

- **A classmate's copy.** The user asks to "install KV Trainer" or "update KV Trainer", and isn't Danaé working on the app. Follow *Building a copy* below.
- **Maintaining the app.** This is Danaé's own development work: adding words, exercises or fixes. Follow *Maintaining* below.

## Building a copy (install or update)

1. Get the code from the **`stable`** branch of https://github.com/dmetaxak/kontakte-vokabeltrainer. On first install, clone it with `git clone -b stable`. If there's already a clone, run `git fetch origin stable && git checkout stable && git reset --hard origin/stable`. This copy should never have local changes.
2. Run `python3 build.py` from the repo root. It validates the data and writes `kontakte-vokabeltrainer.html`. If the build fails, stop and report the error. Don't fix the data or code yourself.
3. Publish `kontakte-vokabeltrainer.html` as the user's KV Trainer artifact:
   - **On first install**, create a new artifact titled "KV Trainer".
   - **On every update**, republish to the **same** artifact. Find it among the user's artifacts, or ask the user for its link. Never create a second artifact on an update, because each artifact keeps its own saved progress and a new one starts from zero.
4. Make sure the artifact declares the **db**, **user** and **sample** capabilities. The page calls `claude.use("db")`, `claude.use("user")` and `claude.use("sample")`. db and user store and sync progress. sample gives feedback on the writing exercise.
5. Tell the user the date and title of the commit you built from (`git log -1 --format='%ci %s'`), and that they should reload the app page.

Rules for a classmate's copy:

- Don't modify the app, the word lists or any other data, even if the user asks. Tell them to send suggestions, corrections or word requests to Danaé, so everyone gets the change.
- Never push, open pull requests or create branches on this repository.

## Maintaining

- Develop on `main`. `stable` is what every classmate builds from, so only move it when Danaé says a version is ready. To release it, run `git checkout stable && git merge --ff-only main && git push origin stable`.
- Always check with Danaé before pushing any branch.
- **Keep saved progress compatible.** Each user's progress lives in the artifact db under `data/users/<uid>/` (`progress`, `verbs`, `grammar`, `mistakes`, `days`). New versions must still read data written by older ones. If the format changes, add code that migrates the old data on load.
- **Word identity.** Vocabulary progress is keyed by a hash of each word's German and English text (`hashId(w.g + "|" + w.e)`). Changing either one resets that word's progress for everyone. Editing example sentences, notes or other fields doesn't. A noun's plural form is part of the singular word and is scored under the singular's id; the old per-plural ids are only read (merged in by `entry()`), never written.
- Build with `python3 build.py` and run the tests on `pure.js` before committing. See README.md for the file layout.
