# vim-complete-es-server

This is a proof-of-concept, using ElasticSearch to power vim autocomplete.


## Requirements

Redirect `vim` autocompletion using https://github.com/gatoatigrado/vim-complete-client. It doesn't do much in the way of scoring.


## Running

After checking out the repository, run `make`. You should be able to run vim with autocomplete using this server.

```bash
export VIM_AUTOCOMPLETE_SERVER_URL="http://$(docker-machine ip default):18013/complete"
mvim
```


## Indexing data

Clear the index with,

```bash
curl -s -XPOST 192.168.99.100:18013/clear-index
```

Index your files with,

```bash
cat **/*.py | curl -s -XPOST 192.168.99.100:18013/index-raw --data-binary @-
```
