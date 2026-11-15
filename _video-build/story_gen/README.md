# Story script generators

Authoring helpers that write `../scripts/chNN.json` (and `../story_maps/chNN.md`).
The JSON scripts are the source of truth for the build; edit either the JSON directly
or the generator and re-run it:

```bash
../.venv/Scripts/python gen_ch05.py      # rewrites ../scripts/ch05.json
../.venv/Scripts/python -I ../validate_scripts.py 5
```

`story_kit.py` holds the shared helpers (points, scenes, exam-trap tables, method chains, pipelines).
Numbers used in the worked examples are checked in `../verify_examples.py`.
