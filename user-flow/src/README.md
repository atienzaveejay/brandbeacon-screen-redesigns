# How the flow screens are made

The screenshots in `../img/` are not hand-drawn. They are generated, so a copy
change is a one-line edit rather than a redraw.

```
python3 gen.py            # writes 15 artboards to ./project/*.dc.html
python3 render.py          # headless Chrome -> ./hi/*.png at 2x
python3 export.py          # -> ../img/flow-*.jpg and drops screens no longer in the flow
python3 build-index.py     # rewrites ../index.html from the step list at the top of the file
```

`gen.py` holds the design tokens, the shared components (tiles, buttons, the
Google button, the locked panel) and one function per screen. `render.py` reads
each artboard's declared `$preview` width and height, so a screen that outgrows
its artboard is clipped: raise the `w=` / `h=` on that screen's `root(...)` call.

`build-index.py` is the page itself. The `STEPS` list near the top is the whole
flow; edit a note there rather than in the generated HTML.
