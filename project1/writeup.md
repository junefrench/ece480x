# Homework 1

John French

## 1

> The following ciphertext which has been encoded with a shift cipher: `ZNKKTKSEQTUCYZNKYEYZKS`.

### a

> Perform an attack against the cipher using one of the attacks discussed in class. What is the key? What is the plaintext?

The decryption key is -6 (the number of letters to shift to decrypt the text; the encryption key would be 6) and the plaintext is `theenemyknowsthesystem`.

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

 Letter | Frequency
:------ | ---------:
 A      | 8.67%
 B      | 0.88%
 C      | 1.42%
 D      | 4.60%
 E      | 6.37%
 F      | 1.24%
 G      | 0.18%
 H      | 0.18%
 I      | 1.59%
 J      | 5.66%
 K      | 2.48%
 L      | 1.24%
 M      | 5.66%
 N      | 9.03%
 O      | 12.04%
 P      | 2.12%
 Q      | 1.77%
 R      | 6.37%
 S      | 5.31%
 T      | 1.42%
 U      | 3.19%
 V      | 0.00%
 W      | 10.09%
 X      | 6.55%
 Y      | 1.95%
 Z      | 0.00%

### b

> Decrypt the ciphertext with help of the relative letter frequency of the English language (e.g., search Wikipedia for letter frequency analysis). Note that the text is relatively short and might not completely fulfill the given frequencies from the table.

The file `subscrack.py` contains a script which will interactively help to decypher text encrypted with a substitution cypher. Using this script I got the following plaintext:
```
two roads diverged in a yellow wood
and sorry i could not travel both
and be one traveler long i stood
and looked down one as far as i could
to where it bent in the undergrowth
then took the other as just as fair
and having perhaps the better claim
because it was grassy and wanted wear
though as for that the passing there
had worn them really about the same
and both that morning equally lay
in leaves no step had trodden black
oh i kept the first for another day
yet knowing how way leads on to way
i doubted if i should ever come back
i shall be telling this with a sigh
somewhere ages and ages hence
two roads diverged in a wood and i
i took the one less traveled by
and that has made all the difference
```

### c

> Who wrote the text?

Robert Frost

## 3

> Vigen&egrave;re proposed a stronger cipher than the Vigen&egrave;re cipher. This cipher is an autokey cipher, where the plaintext istself is used as key. It works by starting with a keyword, and using plaintext characters after that.

### a

> Check the example:
> ```
> Plaintext:  lehrundkunst
> Key:        wpihtpyncbxw
> Ciphertext: HTPYNCBXWOPP

The keyword is `wpi`. `./autokey.py encrypt wpi lehrundkunst` outputs `HTPYNCBXWOPP` and `./autokey.py decrypt wpi HTPYNCBXWOPP` outputs `lehrundkunst`. It checks out.

### b

> Provide a formal definition of the `Gen`, `Enc`, and `Dec` algorithms for this cipher. Make sure to include the equation that defines the encryption and decryption operations.

For the `Gen` algorithm, `i` is the index into the key, `kw` is the keyword, and `c` is the cyphertext.

For the `Enc` and `Dec` algorithms, `k` is the key (output of Gen), `p` is the plaintext, and `c` is the cyphertext.

```
Gen(i, kw, c) = { kw[i]          if i <= len(kw) }
                { c[i - len(kw)] if i > len(kw)  }

Enc(k, p) = (p + k) % 26

Dec(k, c) = (c - k) % 26
```

### c

> Provide an implementation of this cipher.

My implementation can be found in `autokey.py`.

### d

> Decrypt the following ciphertext using the key `plato`: `CZHNANBABUNTBZWSYMJWTMWZUDIJBMCQV`

Using my implementation I got `nohumanthingisofseriousimportance`.

## 4

> Another autokey cipher by Vigen&egrave;re uses the letters of the ciphertext instead of the plaintext to form new key letters.

### a

> Show that this is a much weaker cipher than the other: Explain a brute force attack that can recover most of the plaintext quickly.

Most of the key will be known to an attacker because most of the key is just the cyphertext. It is possible to simply try different offsets for the cyphertext (corresponding to different lengths of the keyword). The key is effectively just the length of the keyword, with the contents of the keyword only affecting the first few characters of the cyphertext.

### b

> Decrypt the following ciphertext that has been encrypted with the above method (It is ok to miss the first few letters): `NEASJFINVCMMZJPQKSQXIKXJBZXLXO`

Using the script in `autokey2crack.py` I got the following plaintext: `?????sendthemoneythisafternoon`

