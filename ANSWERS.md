# POUR LE 18 AVRIL 2023 23H59
# Chiffrement

#### 1. Quelle est le nom de l'algorithme de chiffrement ? Est-il robuste et pourquoi ?

Inverseur commandé (XOR). Utilisé depuis le début de l'informatique, il est mathématiquement parfait et est en théorie inviolable. Toutefois, si la clef n'est pas parfaitement aléatoire, ou que le masque jetable obtenu est réutilisé plus d'une fois, il est possible de contrecarrer ce chiffrement pour ce type d'application, surtout si l'on connait au minimum partiellement la clef.



#### 2. Pourquoi ne pas hacher le sel et la clef directement ? Et avec un hmac ?

La méthode PBKDF2 n'est pas une méthode de hashage à proprement parler, elle sert à dériver les clefs. Le HMAC, lui, permet de hasher un message seulement.
Combiner ces 2 méthodes complémentaires permet d'obtenir le résultat escompté.
En hachant directement le sel et la clef, cela correspond à faire cette tâche une seule fois. Avec un HMAC, nous pouvons gérer le nombre d'itérations (ici, 48 000). De cette manière, nous pouvons empêcher les tentatives de bruteforce qui prendrait un temps bien trop long à "dehasher" les informations.  Utiliser la fonction secret.token_byte est plus sécurisé qu'avec la méthode PBKDF2HMAC qui nécessite un nombre pseudo aléatoire (donc pas idéal) de os.urandom, qui n'est pas forcément compatible avec les différentes distributions et hardware. Cette génération dépend de l'entropie du système qui n'est pas forcément pris par tous les systèmes.


#### 3. Pourquoi il est préférable de vérifier qu'un fichier token.bin n'est pas déjà présent ?

La vérification permet de dresser un histogramme de ce qui a déjà été chiffré. Cela évite donc de chiffrer des données déjà chiffrées (gain de temps, énergie).
Afin d'éviter d'écraser un token déjà existant, et donc ne nplus pouvoir accéder aux informations initialement déchiffrable avec ce token.


#### 4. Comment vérifier que la clef la bonne ?

Pour vérifier cela, il suffit de dériver la clef en question avec le sel et de voir si nous retrouvons le bon token enregistré.