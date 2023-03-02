# UOCIS322 - Project 4 #

Web app for ACP Randoneur Control Point time Calculator

**Author:** Kaegan Koski
**email:** kizaegan@gmail.com

## Description

Calculates start and stop times for control points along a ACP Randoneur. 
Calculates as per the specifications listed here: https://rusa.org/pages/acp-brevet-control-times-calculator

Stores run times and km checkpoint distances in mongodb.

Cannot insert anything above 1.2 times the distance of the run.

## Usage

Run:
	docker build -t some-image-name brevets
	docker run -d -p 5001:5000 some-image-name

Access via http://localhost:5001

Input distances in the kilometers or miles field
Will calculate regulation control points start and stop times for those distances.

## Authors

Michal Young, Ram Durairajan, Kaegan Koski