# Minecraft Server Control Block

A 3D printed, microcontroller powered IoT object to manage a Minecraft server hosted in Microsoft Azure.

NOTE: This project is a work in progress. Needs work in several areas.

## Hardware

- Minecraft ore block 3d print enclosure
- Paper for diffuser
- Adafruit feather huzzah
- 3.7v 150mah LiPo battery
- 2x [momentary press buttons](https://www.adafruit.com/product/559)
- 5x "NeoPixel" WS2812b RBG LEDs
- Magnets (for latches to keep top and bottom together)

## Infrastructure

- Azure VM
- Static IP
- 2x Azure Logic Apps to stop/start the server
- TODO: Cloud-init and Bicep scripts to build the infrastructure 
- TODO: Backup/restore with Blob storage

## Software

- [mscs](https://minecraftservercontrol.github.io/docs/mscs/installation)

## References

- [Minecraft diamond ore lamp](https://www.thingiverse.com/thing:524925)
- [MSCS scripts](https://minecraftservercontrol.github.io/docs/msc)
- [Basic Game Server Hosting on Azure](https://docs.microsoft.com/en-us/gaming/azure/reference-architectures/multiplayer-basic-game-server-hosting)
- [Building a Minecraft server with Azure Logic Apps in 45 minutes](https://blogg.knowit.se/innovation-och-systemutveckling/a-30-minutes-project-building-a-minecraft-server-in-azure)