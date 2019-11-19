# Metaclassifier

*Metaclassifier* is a python library/tools design to help with classification in **ML** datasets. It allow classify text using a **CLI** interface and allow Telegram bots and a web interface for distributed classification.

Notes:

I brake this again, but now the telegrambot interface works, the schemma change a lite.
Now need 2 files the config where why put all configs (`telegram.yml`) and a sentence files
with all the text for classification 1 per line how to use it. Easy:


``` {.bash}
python -m metaclassifier oneconfig telegram.yaml
```

Example of `config.yml`:

```yaml

swapper:
  source: "sentences.txt"

  destination: "data.json"

  options:
    - "verdadero"
    - "falso"
    - "azul"

engine:
  telegram:
    apitoken: 'here goes the token'


```
