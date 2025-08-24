"""MIT License, see LICENSE for more details."""

import os
import random
import shutil
import subprocess
import sys
from os.path import abspath, dirname
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import hashlib

def update_splash(slogan: str) -> None:
    # Choisit un slogan au hasard dans la liste
    if slogan: # Si un slogan est donné en argument, on l'utilise
        splash_text = slogan
    else:
        splash_text = random.choice(text_options)
        # Utilise l'image mise en cache si elle existe
        splash_file = cache_file_name(splash_text)
        if os.path.isfile(splash_file):
            return use_logo(splash_text, splash_file)
    font = ImageFont.truetype(f"{assetdir}/MinecraftRegular-Bmg3.otf", font_size)
    logo_img = Image.open(f"{assetdir}/logo_clear.png")
    original_size = logo_img.size
    txt_img = Image.new(mode="RGBA", size=original_size, color=(0, 0, 0, 0))
    # Retourne l'image pour que le texte soit droit
    txt_img = txt_img.rotate(360 - angle, expand=True)
    d = ImageDraw.Draw(txt_img)
    # Dessine le texte et l'ombre
    if text_shadow:
        d.text(
            (
                text_coords[0] + shadow_offset,
                text_coords[1] + shadow_offset
            ),
            splash_text, fill=shadow_color, anchor="ms", font=font,
        )
    d.text(text_coords, splash_text, fill=text_color, anchor="ms", font=font)
    # Retourne l'image à son angle d'origine
    txt_img = txt_img.rotate(angle, expand=True)
    # Maths pour centrer l'image du texte sur l'image du logo
    coordinates = (
        (txt_img.size[0] - original_size[0]) / 2,
        (txt_img.size[1] - original_size[1]) / 2,
        (txt_img.size[0] + original_size[0]) / 2,
        (txt_img.size[1] + original_size[1]) / 2,
    )
    new = Image.alpha_composite(logo_img, txt_img.crop(coordinates))
    # pas de cache ici si vous voulez ce que vous aimez
    if slogan:
        print(f"Utilisation du slogan depuis la ligne de commande : '{splash_text}'.")
        new.save(f"{themedir}/logo.png")
    else:
        new.save(splash_file)
        use_logo(splash_text, splash_file)

def use_logo(splash_text: str, splash_file: str):
    print(f"Using splash {splash_file}: '{splash_text}'.")
    shutil.copyfile(splash_file, f"{themedir}/logo.png")

def cache_file_name(splash_text: str) -> str:
    h = hashlib.new('md5')
    h.update(splash_text.encode())
    return f"{cachedir}/{h.hexdigest()}.png"

def get_output(command):
    # lance la commande et capture la sortie
    result = subprocess.run(command, stdout=subprocess.PIPE)
    return result.stdout.decode()

def update_package_count() -> None:
    # Exécute Fastfetch et Neofetch dans l'ordre
    for command in [["fastfetch", "-c", "neofetch"], ["neofetch"]]:
        try:
            output = get_output(command)
            break
        except FileNotFoundError:
            continue
    else:
        print("Erreur : ni fastfetch ni neofetch n'ont été trouvés, le nombre de paquets installés ne peut pas être mis à jour.", file=sys.stderr)
        return

    # Extrait le nombre de paquets installés de la sortie
    packages_line = next(line for line in output.split('\n') if 'Packages' in line)
    _, num_packages_str = packages_line.split(':')
    # divise la chaîne en parties en fonction des espaces
    num_packages_parts = num_packages_str.split()

    # Initialise le compteur de paquets
    total_packages = 0

    # Itère sur les parties et additionne les nombres
    for part in num_packages_parts:
        # Vérifie si la partie est un nombre
        if part.isdigit():
            total_packages += int(part)

    path = Path(f"{themedir}/theme.txt")
    text = "Packages Installed"
    old_lines = path.read_text().splitlines(keepends=False)
    new_line = f'\ttext = "{total_packages} {text}"'

    # Remplace {text} par {new_line}
    for i, old_line in enumerate(old_lines):
        if text in old_line:
            patch(path, i, new_line)

    print(f"Met à jour le nombre de paquets installés à {total_packages}.")

def patch(path: Path, linenum: int, new_line: str) -> None:
    lines = path.read_bytes().splitlines(keepends=True)
    lines[linenum] = new_line.encode() + b"\n"
    text = b"".join(lines)
    path.write_bytes(text)

def get_args() -> (str, str):
    argv_len = len(sys.argv)
    if argv_len == 1:
        return "", ""
    elif argv_len == 2:
        return sys.argv[1], ""
    elif argv_len == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print(f"ATTENTION : attendu au plus 2 arguments, mais obtenu {len(sys.argv)}.", file=sys.stderr)
        return sys.argv[1], sys.argv[2]

def update_background(background_file = "") -> None:
    if background_file == "":   # pas de background donné, choisir au hasard
        list_background_files = [f for f in os.listdir(f"{themedir}/backgrounds/") if f[0] != '.'] # ignore les fichiers cachés
        if len(list_background_files) == 0:
            print("Aucun fichier d'arrière-plan disponible pour le choix, l'arrière-plan restera inchangé.", file=sys.stderr)
            return  # ne rien faire
        background_file = f"{themedir}/backgrounds/{random.choice(list_background_files)}"
    elif not os.path.isfile(background_file):   # background given, check if file exists
        print(f"ERREUR : Le fichier {background_file} n'existe pas.", file=sys.stderr)
        quit(1)
    shutil.copyfile(background_file, f"{themedir}/background.png")
    print(f"Utilisation de l'arrière-plan '{background_file}'.")

if __name__ == "__main__":
    # prépare les dossiers
    themedir = dirname(abspath(__file__))
    if not os.path.isdir(f"{themedir}/cache"):
        os.mkdir(f"{themedir}/cache")
    assetdir = f"{themedir}/assets"
    cachedir = f"{themedir}/cache"

    splash_path = Path(f"{assetdir}/splashes.txt")
    text_options = splash_path.read_text().splitlines(keepends=False)
    font_size = 48
    text_color = "rgb(255, 255, 0)"
    shadow_color = "rgb(59, 64, 2)"
    text_coords = (770, 450)
    angle = 20
    text_shadow = True
    shadow_offset = 5
    bg_file, slogan = get_args()

    update_background(bg_file)
    update_splash(slogan)
    update_package_count()
