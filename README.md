# 🍊 OrangePi GPIO Controller

**Webový ovládač pre výstupy Orange Pi: zapni, vypni alebo prepni pin z mobilu či prehliadača.**

![Rok](https://img.shields.io/badge/rok-2017-blue) ![Python](https://img.shields.io/badge/Python-2.7-yellow) ![Flask](https://img.shields.io/badge/Flask-web-black) ![Platforma](https://img.shields.io/badge/Orange%20Pi-GPIO-orange)

> **Rok realizácie:** 2017 · **Tagy:** `orange-pi` `flask` `python` `gpio` `iot` `home-automation` `bootstrap` `pyA20`

## O projekte

Malá Flask aplikácia, ktorá z Orange Pi robí sieťový ovládač štyroch výstupov (a jednej testovacej LED). Stránka „Current bar controller“ zobrazuje stav každého pinu a umožňuje ho prepnúť jedným klepnutím.

## Funkcie

- Zapnutie, vypnutie a prepnutie (toggle) jednotlivých pinov.
- Hromadné **On / Off** pre všetky piny naraz.
- Akcia **reset**: pin sa na 5 sekúnd vypne a potom znova zapne (napr. reštart napájaného zariadenia).
- Piny a ich názvy sa konfigurujú v `server.cfg`, kód netreba meniť.
- Responzívne rozhranie cez Flask-Bootstrap.

## Ovládanie cez URL

| Adresa | Čo robí |
|---|---|
| `/` | stav všetkých pinov |
| `/on`, `/off` | všetky piny zapnúť / vypnúť |
| `/<pin>/on`, `/<pin>/off` | konkrétny pin zapnúť / vypnúť |
| `/<pin>/toggle` | prepnúť pin |
| `/<pin>/reset` | vypnúť na 5 s a znova zapnúť |

## Konfigurácia (`server.cfg`)

```python
PINS = {
    17: {'name': 'Interface 0', 'state': '', 'type': 'production'},
    7:  {'name': 'Test LED',    'state': '', 'type': 'test'},
}
```

## Spustenie

```bash
pip install flask flask-bootstrap flask-appconfig
# knižnica pyA20 pre GPIO Orange Pi
sudo python server.py
```

## Bezpečnosť

Aplikácia nemá prihlásenie a stavy mení cez HTTP GET. Spúšťajte ju len v dôveryhodnej sieti. V `server.cfg` je zapnuté `DEBUG` a pevne zadaný `SECRET_KEY`, takže pred reálnym nasadením ich treba zmeniť.

## Autor

**Vratislav Režo** ([@VRDragon](https://github.com/VRDragon))
