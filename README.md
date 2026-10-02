# Global variables

- Tokens : 
```
^UNIDOCGEN_GLOBAL_XXX^

(XXX is the name of the global variable)
```

- Params : 

```
Anything, considered as the value of the global variable
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
