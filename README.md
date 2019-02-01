# Armana

Armana aims to become an real-time Internet monitor to prioritize incident response.

## How to build

You will need:

* Docker and Docker Compose
* Probably a Linux machine although theoretically it can run on most hosts

```
docker-compose up
```

## How it works

* The system first attempts to remove anonymity from threat map data by correlating geographical information in Shodan's stream API, various gazetteer and threat map sources.
* It then queries the stream database for server information and then public vulnerability repositories.
* The analyst is responsible for contacting the victim organization for further validation.

![Pipeline](./pipeline-diagram.png)

## Roadmap

* Make better parser for Shodan's stream.
* Find more threat data source (free or paid?).
* Integrate Google Map API as a gazetteer source.
* Build NLP models to correlate server fingerprints with gazetteers.
* Refine existing machine learning models (KNN and SVM) for correlating Shodan geography with threat map geography.
* Make web app to advertise product and have organizations sign up or opt out.
* Properly license this thing.
* Code cleanup.
