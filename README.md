# Pushkin

![Pushkin logo](https://raw.githubusercontent.com/ilique/webpushkin/master/pushkin/static/pushkin/img/pushkin.as.png)

## What's the name, again?
The name is **Pushkin A.S.** This stands for *Pushkin Automation Services*, *Pushkin Automated Configurations* or something else like this. Not to be confused with [Alexander Sergeyevich](https://en.wikipedia.org/wiki/Alexander_Pushkin), one of the most famous russian poets.

## And what exactly is it?
This is [SDN](https://en.wikipedia.org/wiki/Software-defined_networking) tool. Which is relatively simple yet effective. Simplicity comes from this basic idea: to imitate actions of a human engineer performing commands on a set of devices. It is also meant to be modular, so that base module communicates with other modules to get some information (about device trunk links, for example).

## Dependencies

* SSH connection module based on [netmiko](https://github.com/ilique/netmiko)
* Web demo is on [Django](https://www.djangoproject.com)
* Multi-command select made by [sortedm2m](https://github.com/gregmuellegger/django-sortedm2m)

## Installation (demo)

    (optional) mkdir pushkindemo && virtualenv pushkindemo && cd pushkindemo && source bin/activate
    pip install netmiko django django-sortedm2m
    git clone https://github.com/ilique/webpushkin.git
    cd webpushkin && python manage.py migrate && python manage.py runserver

## Any support?

Ask pushkin@digitalmanufactory.ru

***
P.S. Why 'Pushkin'? Well, first of all he [is everything for us](https://www.google.ru/search?q=pushkin+is+our+everything), so to speak. And second, services are stored as lines of text - just as in a poem. You can even rhythm you service instructions, if you want. 

See [documentation](https://github.com/ilique/webpushkin/wiki) for details.
