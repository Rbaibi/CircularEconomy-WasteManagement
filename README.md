# Circular Economy and Waste Management

Mothership Coder Mission 2: [Living Environment Challenges](https://www.space4good.com/coder-missions/)

## Problem Definition
There is lack of information of the return on investment ([ROI](https://www.metabolic.nl/news/measuring-the-circular-economy-the-dutch-pioneers-leading-the-way/)) and efficiency of circular economy practices and waste management. You can think of recycling activities, alternative waste collection methods, waste transport logistics, etc. See [circular economy indicators report](https://www.metabolic.nl/publications/circulaire-indicatoren-een-verkenning-voor-de-provincie-zuid-holland/) by Metabolic for  PZH.

## Example research questions
- Can you detect the streets where people are NOT separating wastes into containers and what is their demographic (age, household type)? What new recycling activities, alternative waste collection methods, waste transport logistics can you think of to improve waste management in Zuid-Holland?
- PZH is researching possibilities for construction with wood and other waste material flows for housing and buildings. A circular construction logistics hub is proposed that includes transport of waste materials via ship to polders. Can you help policy makers plan and monitor the sourcing, logistics and use of this these waste streams in construction?
- PZH is part of the Biobased Delta which aims to use plant material and biomass in replacement of fossil based materials. Due to the number of greenhouses and high tech horticulture, PZH is a natural exploration environment for the transition to the biobased economy. How can policymakers measure and map out the biobased initiatives and their overall contribution towards the higher Circular Economy goals?

#### Others
What is the efficiency and financial gains or losses of implementing various policies taking into consideration factors like but not limiting to:
- Recycling policies of different municipalities
- Import and Export of waste
- Industrial vs. Living areas
- Houses vs. Apartment buildings
- Infrastructure and logistics analysis of various waste collection activities
- Urban planning of different cities
- What factory is producing what type of waste?

## Deliverables
The participating team is asked to conduct the necessary research and build a prototype of a system able to:
Investigate the suggested research questions and any additional relevant ones
Find patterns in the historical and real-time data
Simulate different future scenarios (trade-off analysis) 
Calculate the financial projections of the various simulated scenarios for the local government
Deliver a report on the findings and opportunity maps based on the results.

## Stakeholders
- Households
- Local and national government
- Waste management companies
- Business and industrial organizations
- Recycling plants

## Available data

- [Benchmark Huishoudelijk Afval](https://www.benchmarkafval.nl/)
- [Afvalmonitor](https://afvalmonitor.databank.nl//jive?workspace_guid=88bd5a65-fbe0-498e-a3cc-3540cb04dfc0)
- [Afvalverwerking in Nederland 2017](https://www.verenigingafvalbedrijven.nl/public/AfvalverwerkingNL/15/bestand/Werkgroep_Afvalregistratie_Afvalverwerking_in_Nederland_gegevens_2017_november_2018.pdf)
- [Compendium voor de Leefomgeving](https://www.clo.nl/)
- [Waste The Hague](https://ckan.dataplatform.nl/dataset/afvalapartcontainers/resource/371f227d-4414-4e0c-939d-228747b349ce)

## Public Geodata South Holland

Public geodata of the province of South Holland can be found [here](http://geoservices.zuid-holland.nl/arcgis/rest/services). 
You can find information about economy, soil, land, boundaries, environment and water.

#### User guide

1. Click on the link.
2. You can see that there is a thematic classification of folders (Folders).
3. For example, click Rural_area
4. You will now see a list of Services (it is also above) with MapServer in parentheses.
5. For example, click Rural_area / Rural_area_WFS (MapServer)
6. You will now see a list of layers.
7. At the top, you will see the ArcGIS Online Map Viewer option behind "View In:"
8. Click here. A map viewer is opened in a new tab. On the left-hand side under Content you will see Rural area WFS. This is the service that contains the layers that you just saw the list for.
9. Click on the triangle for Rural Area WFS. And you see the same layers appear that you saw in step 6. The default setting is for the NBP 2018 MANAGEMENT AREA layer to be on. Turn this off. This is a heavy file, which means that image building takes a long time.
10. Switch on the "Bicycle traffic intensity" layer. Points now appear in the map image.
11. Now click on the text "Intensity of bicycle traffic". Icons will now appear below this text.
12. Click on the second icon of a table. A table with data per point now appears below the map image.
13. You have now opened a map viewer via the link from the email. Turned on a data layer and opened the table.
14. For people who want to work with data, technical data is also useful, for example to see if a data layer consists of points, lines or surfaces, which area the layer covers or which columns of the table are in it. For this it is useful to click on the "All Layers and Tables" link from the previous tab.
15. The technical data are listed per layer of the service.
 
This guide is for a WFS because with it the data itself (Features, the F in WFS) is shared in accordance with an open standard. In a GIS application, for example, someone who is in Argentina can use this to do an analysis and make a map.

