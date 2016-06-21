# Pushkin

![Pushkin logo](https://raw.githubusercontent.com/ilique/pushkin/master/pushkin.as.png)

## What's the name, again?
The name is **Pushkin A.S.** This stands for *Pushkin Automation Services*, *Pushkin Automated Configurations* or something else like this. Not to be confused with [Alexander Sergeyevich](https://en.wikipedia.org/wiki/Alexander_Pushkin), one of the most famous russian poets.

## And what exactly is it?
This is [SDN](https://en.wikipedia.org/wiki/Software-defined_networking) **tool**. Which is **modular** and relatively **simple**. Simplicity comes from the basic idea: to imitate actions of a human engineer, who performs some commands in a row on some device or set of devices.

## Example
For example, we can **create vlan**, or **make ports** operate in '**trunk**' mode at each device in the set and so on.

## Some details, please
Maybe the first thing every network engineer does when in need of device configuration - store some commands somewhere (usually as plain text). Commands will have 'blank points' as some kind of 'arguments'. Then engineer will perform those commands with filled 'arguments' on some specific device(s) to perform configuration of some service on that device(s).

At the very basic level - we do the same, but faster, cleaner and better. We store commands in database and then perform those commands on specific device or devices. (This is what 'base' module does out-of-the-box). As a step further, we automate the whole thing (enabling of a network service). By automation we mean that human operator needs only to choose which service will be enabled and then provide some minimal data - then Pushkin enables this service taking all other data from the network itself or maybe from some other services.

So from simple idea we get effective and uniform tool for programming network services with almost no (or minimal) human-operator effort.

## Where can i get help with this?

Support available at

pushkin@digitalmanufactory.ru

***
P.S. Why 'Pushkin'? Well, first of all it's our's all, so to speak. And second, services are stored as lines of text - just as lyrics. You can even rythm you service instructions, if you want. See documentation for details.
