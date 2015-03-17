# Homework 1

John French

## 1

> The following ciphertext which has been encoded with a shift cipher: `ZNKKTKSEQTUCYZNKYEYZKS`.

### a

> Perform an attack against the cipher using one of the attacks discussed in class. What is the key? What is the plaintext?

The decryption key is -6 (the number of letters to shift to decrypt the text; the encryption key would be 6) and the plaintext is `THEENEMYKNOWSTHESYSTEM`.

The file `shiftcrack.py` contains a script which will decrypt a shift-cypher-encrypted text, either by guessing the shift from character frequencies or from a given shift.

### b

> Who wrote this message?

Auguste Kerckhoffs

## 2
> The ciphertext printed below was encrypted using a substitution cipher. The objective is to decrypt the ciphertext without knowledge of the key.
>
> ```
> NUA JAWRM RSTOJKOR SX W YODDAU UAAR
> WXR MAJJY S IAQDR XAN NJWTOD PANE
> WXR PO AXO NJWTODOJ DAXK S MNAAR
> WXR DAALOR RAUX AXO WM CWJ WM S IAQDR
> NA UEOJO SN POXN SX NEO QXROJKJAUNE
> NEOX NAAL NEO ANEOJ WM HQMN WM CWSJ
> WXR EWTSXK BOJEWBM NEO PONNOJ IDWSF
> POIWQMO SN UWM KJWMMY WXR UWXNOR UOWJ
> NEAQKE WM CAJ NEWN NEO BWMMSXK NEOJO
> EWR UAJX NEOF JOWDDY WPAQN NEO MWFO
> WXR PANE NEWN FAJXSXK OGQWDDY DWY
> SX DOWTOM XA MNOB EWR NJARROX PDWIL
> AE S LOBN NEO CSJMN CAJ WXANEOJ RWY
> YON LXAUSXK EAU UWY DOWRM AX NA UWY
> S RAQPNOR SC S MEAQDR OTOJ IAFO PWIL
> S MEWDD PO NODDSXK NESM USNE W MSKE
> MAFOUEOJO WKOM WXR WKOM EOXIO
> NUA JAWRM RSTOJKOR SX W UAAR WXR S
> S NAAL NEO AXO DOMM NJWTODOR PY
> WXR NEWN EWM FWRO WDD NEO RSCCOJOXIO
> ```

### a

> Provide the relative frequency of all letters A...Z in the ciphertext.

Letter | Count
------ | -----
A      | 49  
B      | 5   
C      | 8   
D      | 26  
E      | 36  
F      | 7   
G      | 1   
H      | 1   
I      | 9   
J      | 32  
K      | 14  
L      | 7   
M      | 32  
N      | 51  
O      | 68  
P      | 12  
Q      | 10  
R      | 36  
S      | 30  
T      | 8   
U      | 18  
V      | 0   
W      | 57  
X      | 37  
Y      | 11  
Z      | 0

### b

> Decrypt the ciphertext with help of the relative letter frequency of the English language (e.g., search Wikipedia for letter frequency analysis). Note that the text is relatively short and might not completely fulfill the given frequencies from the table.

The file `subscrack.py` contains a script which will interactively help to decypher text encrypted with a substitution cypher. Using this script I got the following plaintext:
```
TWO ROADS DIVERGED IN A YELLOW WOOD
AND SORRY I COULD NOT TRAVEL BOTH
AND BE ONE TRAVELER LONG I STOOD
AND LOOKED DOWN ONE AS FAR AS I COULD
TO WHERE IT BENT IN THE UNDERGROWTH
THEN TOOK THE OTHER AS JUST AS FAIR
AND HAVING PERHAPS THE BETTER CLAIM
BECAUSE IT WAS GRASSY AND WANTED WEAR
THOUGH AS FOR THAT THE PASSING THERE
HAD WORN THEM REALLY ABOUT THE SAME
AND BOTH THAT MORNING EQUALLY LAY
IN LEAVES NO STEP HAD TRODDEN BLACK
OH I KEPT THE FIRST FOR ANOTHER DAY
YET KNOWING HOW WAY LEADS ON TO WAY
I DOUBTED IF I SHOULD EVER COME BACK
I SHALL BE TELLING THIS WITH A SIGH
SOMEWHERE AGES AND AGES HENCE
TWO ROADS DIVERGED IN A WOOD AND I
I TOOK THE ONE LESS TRAVELED BY
AND THAT HAS MADE ALL THE DIFFERENCE
```

### c

> Who wrote the text?

Robert Frost
