# Chiffrement

1. Quelle est le nom de l'algorithme de chiffrement ? Est-il robuste et pourquoi ?

Inverseur commandé (XOR). Utilisé depuis le début de l'informatique, il est mathématiquement parfait et est en théorie impossible  violer. Toutefois, si la clef n'est pas parfaitement aléatoire, ou que le masque jetable obtenu est réutilisé plus d'une fois, il est possible de contrecarrer ce chiffrement.

===================================================

2. Pourquoi ne pas hacher le sel et la clef directement ? Et avec un hmac ?

Utiliser la fonction secret.token_byte est plus sécurisé qu'avec la méthode PBKDF2HMAC qui nécessite un nombre pseudo aléatoire (donc pas idéal) de os.urandom, qui n'est pas forcément compatible avec les différentes distributions et hardware. Cette génération dépend de l'entropie du système qui n'est pas forcément pris par tous les systèmes.
===================================================

3. Pourquoi il est préférable de vérifier qu'un fichier token.bin n'est pas déjà présent ?

===================================================

4. Comment vérifier que la clef la bonne ?

===================================================


# Bonus

1. Expliquez ce que vous faite et pourquoi

===================================================

2. Expliquez comment le casser et écrivez un script pour récupérer la clef à partir d’un fichier chiffré et d’un fichier clair.

===================================================

3. quelle(s) option(s) vous est(sont) offerte(s) fiable(s) par la bibliothèque cryptographie ? Justifiez

===================================================

4. Quelle ligne de commande vous faut-il avec pyinstaller pour créer le binaire ?

===================================================

5. Où se trouve le binaire créer ?

===================================================



