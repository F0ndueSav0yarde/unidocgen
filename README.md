# TODO
- Put everything the same width
- Add table of content with random hex values for anchors (easy search with Ctrl+F)
- Add `<br>` line style
- Recode parsing functions because it's written like shit (but it works)

# Global variables

- Tokens : 
```
^UNIDOCGEN_GLOBAL_VARIABLE^
```

- Params : 

```
NAME=VALUE

Where NAME is the name of the variable to initialize and VALUE is its value, in any type
```

# Block of code

- Tokens : 
```
^UNIDOCGEN_BOX_CODE_START^
^UNIDOCGEN_BOX_CODE_END^
```

- Params : 
```
LINE_TYPE : SINGLE
            DOUBLE
            SINGLE_HEAVY
            SINGLE_CORNERS
WIDTH : <int>
TAB : <str>
LINE_NUMBER : <int>
```

# Title

- Tokens : 
```
^UNIDOCGEN_COMPACT_TITLE_START^
^UNIDOCGEN_COMPACT_TITLE_END^
```

- Params : 
```
TITLE_TYPE : LIGHT
             MEDIUM
             HEAVY
             FULL
WIDTH : <int>
```
