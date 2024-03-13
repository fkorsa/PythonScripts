colors = ['red', 'grey', 'yellow', 'black', 'green', 'purple', 'blue', 'white', 'orange', 'turquoise']

for color in colors:
    print(
f""".background-color-{color} {{
    background-color: var(--color-constant-{color});
}}

.background-color-{color}.edge-control {{
    border-top-color: var(--color-constant-light-{color});
    border-bottom-color: var(--color-constant-{color});
}}

.background-color-{color}.edge-control:hover {{
    border-bottom-color: var(--color-constant-light-{color});
}}
""")