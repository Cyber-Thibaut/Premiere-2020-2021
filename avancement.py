print("Quelles sont les valeurs des coefficients stoechiométriques ?")
a=int(input("Donnez la valeur de a="))
b=int(input("Donnez la valeur de b="))
c=int(input("Donnez la valeur de c="))
d=int(input("Donnez la valeur de d="))
pas=float(input("Donner le pas d'avancement="))
print("Donner les valeurs des quantités na et nb")
nai=float(input("La quantité de a est:"))
nbi=float(input("La quantité de b est:"))
nci=0.0
ndi=0.0
x=0.0
na=nai
nb=nbi
nc=nci
nd=ndi
while na>0.0 and nb>0.0:
    na=nai-a*x
    nb=nbi-b*x
    nc=nci+c*x
    nd=ndi+d*x
    print("na=",na,"\tnb=",nb,"\tnc=",nc,"\tnd=",nd)
    x=x+pas
print("Xmax est",x)
if na==0 and nb==0:
    print("Le mélange a été introduit dans des proportions stoechiométriques.")
elif na==0:
    print("Le réactif limitant est na.")
elif nb==0:
    print("Le réactif limitant est nb.")
