# Le Trio de Thèmes Minecraft Grub

| *> Menu Principal Minecraft <* | [Menu de Sélection de Monde Minecraft](https://github.com/Lxtharia/minegrub-world-sel-theme) | [Utiliser les deux thèmes ensemble](https://github.com/Lxtharia/double-minegrub-menu) |
| --- | --- | --- |

**Découvrez également ces autres projets :**

| [Thème SDDM Minecraft](https://github.com/Davi-S/sddm-theme-minesddm) par Davi-S | [Thème Plymouth Minecraft](https://github.com/nikp123/minecraft-plymouth-theme) par nikp123 | [Splash de Chargement de Monde Minecraft KDE](https://github.com/Samsu-F/minecraftworldloading-kde-splash) par Samsu-F |
| --- | --- | --- |

Il existe également une [traduction en espagnol](https://github.com/FeRChImoNdE/minegrub-theme-es) !

# Minegrub

Un thème Grub dans le style de Minecraft !

![Aperçu Minegrub "Capture d'écran"](resources/preview_minegrub.png)

# Installation

> ### Remarque : grub vs grub2
> - Si vous avez un dossier `/boot/grub2` au lieu de `/boot/grub`, vous devez adapter les chemins de fichiers mentionnés ici et dans le fichier `minegrub-update.service`.
> - Si vous n’êtes pas sûr, exécutez `grub-mkconfig -V` pour vérifier si vous avez la version 2 de grub (ce que vous devriez avoir).

## Installation manuelle

- Cloner ce dépôt :
```bash
git clone https://github.com/Lxtharia/minegrub-theme.git
```
- (optionnel) Choisir un fond d’écran :
```bash
./choose_background.sh  # ou simplement copier une image personnalisée dans minegrub/background.png
```
  - Si vous souhaitez utiliser le script de mise à jour, copiez un nombre arbitraire d’images dans `minegrub/backgrounds/`. Vous pouvez en trouver quelques-unes dans `background_options/` ou utiliser vos propres images.
  - Si vous ne voulez pas utiliser le script de mise à jour ou si vous voulez toujours utiliser le même fond, utilisez `./choose_background.sh` ou copiez simplement une image personnalisée dans `minegrub/background.png`.

- Copier le dossier sur votre partition de démarrage : (`-ruv` = récursif, mise à jour, verbeux)
```bash
cd ./minegrub-theme
sudo cp -ruv ./minegrub /boot/grub/themes/
```
- Ouvrez `/etc/default/grub` avec votre éditeur de texte et modifiez/décommentez cette ligne :
```bash
GRUB_THEME=/boot/grub/themes/minegrub/theme.txt
```
- Mettez à jour votre configuration grub en direct en exécutant :
```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```
- C’est prêt !
- Consultez la section `Configuration` si vous souhaitez mettre à jour automatiquement le texte splash, le fond et l’affichage des paquets après chaque démarrage.

## Utilisation du script d’installation

- Exécutez le script d’installation en tant que root et à vos risques :
```bash
sudo ./install_theme.sh
```
- Cela installera le thème, le service systemd et activera le fond de la console.
- Vous pouvez également choisir un fond si vous ne voulez pas le randomiser.

---

## Module NixOS (flake)

<details><summary>Exemple minimal</summary>

```nix
# flake.nix
{
  inputs.minegrub-theme.url = "github:Lxtharia/minegrub-theme";
  # ...

  outputs = {nixpkgs, ...} @ inputs: {
    nixosConfigurations.HOSTNAME = nixpkgs.lib.nixosSystem {
      modules = [
        ./configuration.nix
        inputs.minegrub-theme.nixosModules.default
      ];
    };
  }
}

# configuration.nix
{ pkgs, ... }: {

  boot.loader.grub = {
    minegrub-theme = {
      enable = true;
      splash = "100% Flakes!";
      background = "background_options/1.8  - [Classic Minecraft].png";
      boot-options-count = 4;
    };
    # ...
  };
}
```
</details>

# Configuration

## Adapter le nombre d’options de démarrage

- Si vous avez plus ou moins de 4 options, les boutons se chevaucheront avec la barre du bas (celle indiquant "Options" et "Console").
- Pour déplacer cette barre et corriger cela, modifiez [cette ligne](https://github.com/Lxtharia/minegrub-theme/blob/main/minegrub/theme.txt#L71) dans `/boot/grub/themes/minegrub/theme.txt`.
- La formule et certaines valeurs pré-calculées pour 2,3,4,5... options sont dans `theme.txt`, vous permettant de les adapter facilement.

## Mise à jour automatique du splash et du nombre de paquets

Le script `update_theme.py` :
- Choisit une ligne aléatoire dans `assets/splashes.txt`.
- Génère et remplace `logo.png` avec le texte splash.
- Met à jour le nombre de paquets installés.
- Choisit aléatoirement un fichier de `backgrounds/` comme fond (fichiers cachés ignorés).

Prérequis :
- `fastfetch` ou `neofetch` installé.
- Python 3 et Pillow installés (`sudo -H pip3 install pillow`).
- Pour ajouter des textes splash, éditez `./minegrub/assets/splashes.txt`.
- Placez vos fonds dans `./minegrub/backgrounds/`.

Exemple pour définir splash et fond spécifiques :
```bash
python update_theme.py 'backgrounds/1.15 - [Buzzy Bees].png' 'Splashing!'
```
Paramètres vides = choix aléatoire.

### Mise à jour manuelle
```bash
python /boot/grub/themes/minegrub/update_theme.py
```

### Avec init-d (SysVinit)
```bash
sudo cp -v "./minegrub-SysVinit.sh" "/etc/init.d/minecraft-grub"
sudo chmod u+x "/etc/init.d/minecraft-grub"
sudo update-rc.d minecraft-grub defaults
```

### Avec systemd
- Modifiez `./minegrub-update.service` pour `/boot/grub2/` si nécessaire.
- Copiez-le dans `/etc/systemd/system`.
- Activez le service : `systemctl enable minegrub-update.service`.
- Vérifiez `systemctl status minegrub-update.service` si problèmes.

## Définir le fond de la console

Dans grub, appuyez sur 'c' pour ouvrir la console. Pour un fond :
```bash
# Sauvegarde
cp /etc/grub.d/00_header ./00_header.bak
# Modifier elif
sed --in-place -E 's/(.*)elif(.*"x\$GRUB_BACKGROUND" != x ] && [ -f "\$GRUB_BACKGROUND" ].*)/\1fi; if\2/' /etc/grub.d/00_header
```
Puis :
```bash
GRUB_BACKGROUND="/boot/grub/themes/minegrub/dirt.png"
```
Regénérez le `grub.cfg`.

# Notes
- `GRUB_TIMEOUT_STYLE` doit être `menu`.
- Explications détaillées pour débutants.
- Testé sur Arch.
- Amusez-vous bien !

### Remerciements
- https://github.com/toboot pour l'idée.
- Internet (http://wiki.rosalab.ru/en/index.php/Grub2_theme_tutorial)
- Contributeurs pour les améliorations.
- [Vanilla Tweaks](https://vanillatweaks.net) pour certains fonds.

Police : https://www.fontspace.com/minecraft-font-f28180, usage non commercial.
