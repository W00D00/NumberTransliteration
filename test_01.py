# -*- coding: utf-8 -*-

import re
import itertools


# 1, 10, 100, 1000, 10 000, 100 000
d = "400 0000"

dd = re.sub("\D", "", d)

print(d, dd)


#
#p = re.compile('\\b[\s\d]*\d+(?= *(?:forint\w*|,|\|))')
#unitPattern = re.compile(" *forint\w*")
#
#s = "Hétfőtől | 1 350 wattos kézi körfűrész | 12 999, | 1 500 wattos fúró- és vésőkalapács | 15 999, | profi multifunkciós detektor | 5 999 forint."
#
#ss = unitPattern.sub("", s)
#print(s)
#print(ss)
#
#
#
#
#p = re.compile('(\\b[\s\d]*\d+)( *(?:forint\w*|,|\|))')
#
#s = "Fa tusfürdő vagy habfürdő vagy testápoló, | darabja csak↗ | 599 forint. || Fa dezodorok vagy stiftek | csak↗ | 449 forint."
#s = "Most csütörtöktől | A4-es spirálfüzet | 499, | A5-ös mintás füzet | 49, | keményfedeles jegyzetkönyv | 549 forintért."
#
#pp = p.findall(s)
#
#if pp:
#    print(len(pp), pp)
#    for idx, ppp in enumerate(pp):
#        print(idx, ppp)
#        if "forint" in ppp[1]:
#            print("van forint")
#        # sentence with price and currency
#        s = re.sub(ppp[0], "200", s)
#        print(s)
#        # sentence with price and currency
#        s2 = re.sub(ppp[1], "", s)
#        print(s2)
