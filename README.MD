`TODO : Traduire en anglais.`

## Classe Maze.

Gére les positions, les déplacements, les élements (mobiles ou non).

- Crée les éléments inamovibles du labyrinthe (murs, sol, entrée, sortie), à partir du fichier maze.txt;
  Le départ est placé aléatoirement.
  Les éléments inamovibles sur lesquels un déplacement peut être effectué (donc tout sauf les murs) sont stockés dans
  un dictionnaire dont la clé est la position et le contenu le type d'élément (1). Ce dictionnaire réprésente le
  "chemin libre".
- Crée les élements "mobiles" (le gardien, MacGyver, le tube, l'aiguille, l'éther).
  On indique leur position : celle du gardien est celle de la sortie, celle de MacGyer est celle de l'entrée, celle
  de l'aiguille, du tube et de l'éther est placée de façon aléatoire, en vérifiant que l'emplacement n'est pas déjà pris
  par un élément mobile.
  Les élements mobiles sont stockés dans un dictionnaire ayant comme clé le type d'élément et comme contenu un objet
  ayant comme modéle la classe Character pour le gardien et MacGyver ou la classe Collectable pour les éléments à
  collecter.
- Gére les déplacements des éléments mobiles dans le labyrinthe.

(1) Type d'élément :
    A = Aether, B = Begin, E = Exit, G = Guardian, M = MacGyver, N = Needle, T = Tube, W = Wall, . = sol
    
## Classe MazeWindow.

Affiche ce que lui donne la classe Maze et gére les événements clavier.

- Initialise une fenêtre pygame.
- Charge les images des éléments utilisés dans le labyrinthe, stockées par type d'élement.
- Balaye le chemin libre pour en trouver le type d'élement, lequel permet d'afficher l'image correspondante.
- Affiche la fenêtre.
- Surveille les évenements clavier, lesquels permettent de déplacer MacGyver. La gestion de ce déplacement est
  assurée dans la classe Maze, à partir des éléments de la Classe Movable.

## Classe Movable.

Gére le stockage de la position.

## Classe Syringe, fille de Movable.

Gére un compteur (attribut de la classe).

- Incrémente le compteur quand MacGyver collecte une partie non encore collectée de
  la seringue.
- Retourne l'état de la seringue (compléte ou non) quand MacGyver est proche du gardien.
