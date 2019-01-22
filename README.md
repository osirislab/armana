# Armana

Armana aims to become an real-time Internet monitor to prioritize incident response. Source code is in `src`

## How it works

* The system first attempts to remove anonymity from threat map data by correlating geographical information in Shodan's stream API, various gazetteer and threat map sources.
* It then queries the stream database for server information and then public vulnerability repositories.
* The analyst is responsible for contacting the victim organization for further validation.

## How to build

Visit `src/`

## Roadmap

* Integrate Google Map API as a gazetteer source.
* Build NLP models to parse server information.
* Refine exsiting machine learning models for better usability and scores.
