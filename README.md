# gravastar-local

Miroir local du configurateur web GravaStar, préparé pour un usage hors ligne sur `localhost` sans réécriture du frontend d'origine.

## Structure

- `site/original/` contient la copie source non modifiée du site statique.
- `patches/` contient le script de patch reproductible et idempotent.
- `docker/` contient l'image Nginx et la configuration HTTP locale.
- `docs/` contient les notes de prise en charge, sécurité et Linux/WebHID.
- `vendor/` contient les dépendances frontales vendorisées pour le mode hors ligne.
- `site/patched/` est une sortie générée localement, ignorée par Git.
- `.work/` contient les artefacts d'analyse et archives locales, ignorés par Git.

## Lancement

Pour lancer le miroir local :

```bash
docker compose up --build
```

Le site est ensuite disponible sur :

```text
http://127.0.0.1:18088/gravastar/connect
```

Pour changer le port publié :

```bash
GRAVASTAR_PORT=8088 docker compose up --build
```

Le service Nginx ne sert que des fichiers locaux. Les chargements distants automatiques connus ont été remplacés par des fichiers locaux au moment du build.
Les branches automatiques qui menaient vers des hôtes distants non embarqués tombent sur une page locale d'indisponibilité en mode hors ligne.

## Régénérer la version patchée

Le bundle servi n'est pas modifié à la main. Il est régénéré depuis `site/original/` avec :

```bash
python3 patches/apply_patches.py
```

Par défaut, la commande génère :

```text
site/patched/hub.gravastar.com
```

Le script échoue volontairement si les chaînes attendues ont changé dans les bundles d'origine.

## WebHID sous Linux

- Utiliser un navigateur Chromium récent avec WebHID actif.
- Firefox ne prend pas WebHID en charge pour ce configurateur.
- Le site doit être servi depuis `localhost` ou une origine HTTPS de confiance.
- Une règle `udev` est généralement nécessaire pour accéder au périphérique sans lancer le navigateur en root.

La règle d'exemple est fournie dans [docs/99-gravastar-webhid.rules](/home/pepeuch/Documents/gravastar-local-1/docs/99-gravastar-webhid.rules) et la procédure détaillée dans [docs/protocol-notes.md](/home/pepeuch/Documents/gravastar-local-1/docs/protocol-notes.md).

## VID et PID documentés

- VID `14126` (`0x372e`)
- PID officiel observé `4204` (`0x106c`)
- PID additionnel pris en charge par le patch local `4325` (`0x10e5`)

Les détails sont dans [docs/supported-devices.md](/home/pepeuch/Documents/gravastar-local-1/docs/supported-devices.md).

## Sécurité

- L'accès WebHID reste local entre le navigateur et le périphérique.
- Le miroir local ne doit charger aucune ressource distante automatiquement.
- Les liens d'aide et réseaux sociaux présents dans l'UI restent des liens sortants explicites si l'utilisateur clique dessus.
- Les routes automatiques non prises en charge hors ligne aboutissent à une page locale d'information plutôt qu'à une navigation distante.
- La fonction de rythme musical basée sur `localhost:15371` est conservée comme branche optionnelle non validée dans ce miroir local.

Plus de détails dans [docs/security.md](/home/pepeuch/Documents/gravastar-local-1/docs/security.md).
