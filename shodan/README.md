# Usage

To launch an instance of the streamer. Do the following:

* Acquire a stream-capable API key from Shodan
* Create a `.env` file in the `shodan` root directory, which should specify `API_KEY`, `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_NAME` and `DB_PORT`. An example will be provided in `shodan/.env-sample`.

## `.env-sample`

The program only works with MariaDB. If you don't specify the ports it will use its default configuration.

```
API_KEY=iamafakeapikeybecausereasons
DB_USER=jake
DB_PASS=passwordispassword
DB_HOST=localhost
DB_NAME=relatednamepls
DB_PORT=
```
