S=u{k}+...+u{p}
somme de termes consecutifs:
    U{k}+U{p}
  S=--------- *(p-k+1)
        2

termes generaux:
  suite geometrique:
    u{n}=u{u}*q^n-p
    OU
    u{n}=u{0}*q^n
  suite arithmetique:
    u{n}=u{p}+(n-p)*r

somme de puissances sucesives:
    1-q^n+1
 S= --------
      1-q

somme des termes consecutifs d'une suite
geometrique:
  S=u0+u1+u2+u3+u4+u5+...+u{n}
        1-q{n-1}
  S=u0*----------
          1-q
  S=u{k}+u{k+1}+...+u{p}
  
          1-q{p-k+1}
  S=u{k}*-------------
              1-q
  
  SOIT:
                    1-raison{nb de termes}
  S= Premier terme*------------------------
                          1-raison

pour justifier que c'est une suite geometrique:
  w{n}=u{n}-x
  calculer w{0} et w{1} (=x)
  w{1}/w{0}
  montrer que w{n+1} = x*w{n} pour tout n