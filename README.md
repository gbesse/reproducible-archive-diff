# reproducible-archive-diff

## Français

Comparer le contenu réel de deux builds sans cacher les changements métier.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m reproducible_archive_diff examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Compare les contenus et métadonnées déclarées de deux vrais ZIP/TAR, en plus des empreintes des archives brutes. Une différence de conteneur peut être expliquée par le seul mtime ; modes, liens et octets restent visibles.

### Limites

Ordre des membres ignoré, chemins conservés exactement ; mtime ignoré seulement sur demande. Lecture bornée sans extraction, pas preuve SLSA, source reproductible ou absence de code malveillant. Doublons rendent la comparaison ambiguë.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Compare actual build contents without hiding meaningful changes.

Synthetic data; no network access or secret required.

```sh
python -m reproducible_archive_diff examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Compares content and declared metadata of actual ZIP/TAR files alongside raw archive hashes. Container differences can be explained by mtime alone; modes, links and bytes remain visible.

### Limits

Member order ignored, paths preserved exactly; mtime ignored only on request. Bounded reading without extraction, no SLSA, reproducible-source or malware-free proof. Duplicate names make comparison ambiguous.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Comparar contenidos reales de dos compilaciones sin ocultar cambios relevantes.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m reproducible_archive_diff examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Compara contenido y metadatos declarados de ZIP/TAR reales junto a resúmenes brutos. Diferencias del contenedor pueden explicarse solo por mtime; modos, enlaces y bytes siguen visibles.

### Límites

Orden de miembros ignorado, rutas exactas; mtime ignorado solo a petición. Lectura acotada sin extracción, sin prueba SLSA, fuente reproducible o ausencia de malware. Duplicados vuelven ambigua la comparación.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://reproducible-builds.org/docs/archives/
- https://docs.python.org/3/library/zipfile.html
