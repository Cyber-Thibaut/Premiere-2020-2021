femme = ["une scientifique","une reine","un pirate"]
homme = ["un policier", "un artiste", "ton grand-père", "un robot tueur"]
lieu = ["sur Pluton.", "au supermarché.", "dans une grotte pleine de chauves-souris."]
ellePortait = ["un masque de plongée.", "des ailes de fée.", "un sac en papier."]
ilPortait = ["un costume violet.", "un déguisement de requin.", "une serviette de plage."]
femmeDit = ["« Qui êtes-vous ? »", "« Combien de haricots font cinq ? »", "« Pourquoi ? »"]
hommeDit = ["« Bip ! »", "« Ne mangez pas de grenouilles! »", "« Comment appelez-vous cela ? »"]
conséquence = ["la paix dans le monde", "le chaos", "un pied les a écrasés", "des arcs-en-ciel"]
mondeDit = ["« C’est absurde ! »", "« Le fromage est à la mode. »", "« Je fonds ! »"]

import random
while True:
  print(random.choice(femme), "a rencontré", random.choice(homme), random.choice(lieu))
  print("Elle portait", random.choice(ellePortait))
  print("Il portait", random.choice(ilPortait))
  print("Elle a dit", random.choice(femmeDit))
  print("Il a dit", random.choice(hommeDit))
  print("La conséquence a été", random.choice(conséquence))
  print("Le monde a dit", random.choice(mondeDit))
  print()
  input("Appuie sur Entrée pour rejouer.")
  print()
