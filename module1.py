MDP1=42910
a=str(input("Bonjour, quel est votre nom ? "))
print("Bienvenu {} dans la base de donnée commune à la CIA & a la DGSI".format(a))
MDP2=int(input("Veuillez entrer votre mot de passe"))
if MDP1!=MDP2:
    print("ALERTE!!!\nINTRUSION!")