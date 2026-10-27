# MINISTERUL EDUCAȚIEI ȘI CERCETĂRII AL REPUBLICII MOLDOVA

### UNIVERSITATEA TEHNICĂ A MOLDOVEI

#### Facultatea Calculatoare, Informatică și Microelectronică

#### Departamentul Software Engineering și Automatică

# RAPORT

### la Lucrarea de Laborator Nr. 4

**Disciplina:** Tehnici de programare

**Tema:** „Cifruri bloc. Algoritmul DES”

**A efectuat:** st. gr. SI – 262, Grigorița Alexandra

**A verificat:** asistent universitar Zaia Maia

**Chișinău – 2026**

## 1. SARCINA LUCRĂRII

* **Scopul lucrării:** Însușirea algoritmului DES prin criptarea manuală a unui bloc de 64 de biți al unui mesaj, într-o versiune scurtată a algoritmului, formată dintr-o singură rundă.

* **Obiective:**

  1. Reprezentarea mesajului și a cheii în cod ASCII și în format binar.

  2. Generarea cheilor de rundă $K_1$ prin permutarea PC-1, împărțirea în jumătățile $C_0$ și $D_0$, deplasarea circulară la stânga și comprimarea PC-2.

  3. Aplicarea permutării inițiale IP și calculul funcției de rundă $f$ (expansiunea E, XOR cu subcheia $K_1$, cutiile de substituție S și permutarea P).

  4. Aplicarea formulelor structurii Feistel, inversarea jumătăților, permutarea finală $IP^{-1}$ și obținerea textului cifrat în reprezentare hexazecimală.

* **Enunțul sarcinii:** Să se realizeze criptarea unui mesaj $m$ de 8 caractere cu algoritmul DES și cheia $k$, considerând o versiune scurtată, formată dintr-o singură rundă: permutarea finală se aplică la sfârșitul rundei 1. Mesajul criptat se reprezintă în hexazecimal. Mesajul și cheia se aleg liber de către student.

**Tabelul 1 – Datele inițiale ale sarcinii**

| Data | Semnificație | Valoarea aleasă | 
| ----- | ----- | ----- | 
| $m$ | Mesajul (exact 8 caractere / 64 biți) | `Criptare` | 
| $k$ | Cheia (exact 8 caractere / 64 biți) | `studenta` | 

## 2. NOTIUNI TEORETICE

### 2.1 Prezentare generală a algoritmului DES

Data Encryption Standard (DES) este un cifru bloc simetric adoptat ca standard oficial în anul 1977, derivat din algoritmul LUCIFER creat de IBM. Algoritmul procesează datele în blocuri fixe de 64 de biți utilizând o cheie de 64 de biți (din care 56 de biți sunt efectivi, iar 8 biți sunt folosiți pentru controlul parității).

**Tabelul 2.1 – Parametrii principali ai algoritmului DES**

| Parametru | Valoare | 
| ----- | ----- | 
| Mărimea blocului de date | 64 biți (8 caractere ASCII / 16 cifre hexazecimale) | 
| Mărimea cheii (introdusă / efectivă) | 64 biți / 56 biți (biții 8, 16, ..., 64 reprezintă biți de paritate) | 
| Structura algoritmului | Rețea Feistel cu 16 runde | 
| Numărul de subchei | 16 subchei de rundă $K_1, ..., K_{16}$, fiecare de 48 biți | 
| Decriptarea | Aceiași pași ca la criptare, utilizând subcheile în ordine inversă ($K_{16}, ..., K_1$) | 

### 2.2 Operații elementare utilizate

DES combină succesiuni repetate de cinci operații fundamentale pe biți:

1. **Conversia ASCII** $\leftrightarrow$ **Binar** $\leftrightarrow$ **Hexazecimal:** Fiecare caracter este stocat pe 8 biți (1 octet). Un bloc de 64 de biți conține 8 caractere ASCII sau 16 cifre hexazecimale (o cifră hexazecimală corespunde exact la 4 biți).

2. **Operația XOR (**$\oplus$**):** Adunare modulo 2 bit cu bit. Proprietatea esențială care asigură posibilitatea decriptării este:
   

   $$
   (a \oplus b) \oplus b = a
   $$

3. **Permutarea după tabel:** Biții dintr-un bloc sunt reordonați în funcție de indecșii specificați într-un tabel de permutare (numerotați de la 1 la stânga). Un tabel de permutare poate comprima un bloc (ex. PC-1, PC-2) sau îl poate extinde prin duplicare (ex. tabelul E).

4. **Deplasarea circulară la stânga:** Biții dintr-un bloc sunt deplasați spre stânga cu 1 sau 2 poziții, bitul extras din stânga fiind reintrodus la capătul din dreapta.

5. **Substituția prin Cutiile S (S-boxes):** Transformă ne-liniar grupuri de 6 biți în grupuri de 4 biți.

### 2.3 Structura de tip Feistel și Runda DES

Cifrul DES se bazează pe o rețea Feistel. Blocul inițial de 64 biți este supus mai întâi Permutării Inițiale (IP) și împărțit în două jumătăți de câte 32 de biți: stânga ($L_0$) și dreapta ($R_0$). În fiecare rundă $i$ ($1 \le i \le 16$), jumătățile noi se calculează după formulele:

$$
L_i = R_{i-1}
$$

$$
R_i = L_{i-1} \oplus f(R_{i-1}, K_i)
$$

Funcția de rundă $f(R_{i-1}, K_i)$ este inima algoritmului și parcurge 4 pași:

* **Expansiunea E:** $R_{i-1}$ de 32 de biți este extins la 48 de biți.

* **XOR cu subcheia:** Se calculează $E(R_{i-1}) \oplus K_i$ și se împarte în 8 blocuri de 6 biți ($B_1, ..., B_8$).

* **Cutiile S (**$S_1...S_8$**):** Fiecare bloc $B_j$ de 6 biți intră în cutia $S_j$ și rezultă un bloc de 4 biți.

* **Permutarea P:** Cele 8 grupuri de 4 biți (32 biți total) sunt permutați prin tabelul P.

În varianta scurtată solicitată în lucrare (cu o singură rundă), se execută doar runda 1 cu subcheia $K_1$, se inversează jumătățile obținute ($R_1 L_1$) și se aplică Permutarea Finală $IP^{-1}$.

## 3. TABELELE OFICIALE ALE ALGORITMULUI DES

### Tabelele pentru Generarea Cheilor

* **Permutarea PC-1 (**$64 \rightarrow 56$ **biți):**

  ```
  57  49  41  33  25  17   9    1  58  50  42  34  26  18
  10   2  59  51  43  35  27   19  11   3  60  52  44  36
  63  55  47  39  31  23  15    7  62  54  46  38  30  22
  14   6  61  53  45  37  29   21  13   5  28  20  12   4
  
  ```

* **Permutarea PC-2 (**$56 \rightarrow 48$ **biți):**

  ```
  14  17  11  24   1   5    3  28  15   6  21  10
  23  19  12   4  26   8   16   7  27  20  13   2
  41  52  31  37  47  55   30  40  51  45  33  48
  44  49  39  56  34  53   46  42  50  36  29  32
  
  ```

### Tabelele pentru Procesarea Datelor

* **Permutarea Inițială IP (**$64 \rightarrow 64$ **biți):**

  ```
  58  50  42  34  26  18  10   2    60  52  44  36  28  20  12   4
  62  54  46  38  30  22  14   6    64  56  48  40  32  24  16   8
  57  49  41  33  25  17   9   1    59  51  43  35  27  19  11   3
  61  53  45  37  29  21  13   5    63  55  47  39  31  23  15   7
  
  ```

* **Tabelul de Expansiune E (**$32 \rightarrow 48$ **biți):**

  ```
  32   1   2   3   4   5     4   5   6   7   8   9
   8   9  10  11  12  13    12  13  14  15  16  17
  16  17  18  19  20  21    20  21  22  23  24  25
  24  25  26  27  28  29    28  29  30  31  32   1
  
  ```

* **Permutarea P (**$32 \rightarrow 32$ **biți):**

  ```
  16   7  20  21   29  12  28  17     1  15  23  26    5  18  31  10
   2   8  24  14   32  27   3   9    19  13  30   6   22  11   4  25
  
  ```

* **Permutarea Finală** $IP^{-1}$ **(**$64 \rightarrow 64$ **biți):**

  ```
  40   8  48  16  56  24  64  32    39   7  47  15  55  23  63  31
  38   6  46  14  54  22  62  30    37   5  45  13  53  21  61  29
  36   4  44  12  52  20  60  28    35   3  43  11  51  19  59  27
  34   2  42  10  50  18  58  26    33   1  41   9  49  17  57  25
  
  ```

## 4. CALCULE DETALIATE PAȘI CU PAȘI

### PARTEA A: GENERAREA SUBCHEII DE RUNDĂ $K_1$

**Pasul 1. Reprezentarea cheii** $k =$ **`studenta` în ASCII și binar (64 biți):**

**Tabelul 4.1 – Reprezentarea binară a cheii**

| Caracter | s | t | u | d | e | n | t | a | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| **Hex** | 73 | 74 | 75 | 64 | 65 | 6E | 74 | 61 | 
| **Binar** | 01110011 | 01110100 | 01110101 | 01100100 | 01100101 | 01101110 | 01110100 | 01100001 | 

$$
K = 01110011 \quad 01110100 \quad 01110101 \quad 01100100 \quad 01100101 \quad 01101110 \quad 01110100 \quad 01100001
$$

**Pasul 2. Aplicarea permutării PC-1 (**$K^+ = PC1(K)$**):**
Numerotăm biții cheii $K$ de la 1 la 64. Biții de pe pozițiile $8, 16, 24, 32, 40, 48, 56, 64$ sunt eliminați. Citim biții conform tabelului PC-1:

* Bitul 57 din K este `0`, bitul 49 este `0`, bitul 41 este `0`, ..., bitul 4 este `1`.

$$
K^+ = 0000000 \quad 0111111 \quad 1111111 \quad 1110100 \quad 0010000 \quad 1011111 \quad 1000100 \quad 0000111
$$

**Pasul 3. Împărțirea în** $C_0$ **și** $D_0$ **(câte 28 de biți):**

* $C_0$ (primii 28 biți) $= 0000000 \quad 0111111 \quad 1111111 \quad 1110100$

* $D_0$ (ultimii 28 biți) $= 0010000 \quad 1011111 \quad 1000100 \quad 0000111$

**Pasul 4. Deplasarea circulară la stânga cu 1 poziție (**$C_1, D_1$**):**

* $C_1 = 0000000 \quad 1111111 \quad 1111111 \quad 1101000$

* $D_1 = 0100001 \quad 0111111 \quad 0001000 \quad 0001110$

**Pasul 5. Permutarea PC-2 (**$K_1 = PC2(C_1D_1)$**):**
Concatenăm $C_1D_1$ (56 biți) și extragem 48 biți conform tabelului PC-2:

$$
K_1 = 111000 \quad 001011 \quad 111001 \quad 100110 \quad 100101 \quad 110000 \quad 001001 \quad 110000
$$

### PARTEA B: EXECUȚIA RUNDEI 1

**Pasul 6. Reprezentarea mesajului** $m =$ **`Criptare` în ASCII și binar (64 biți):**

**Tabelul 4.2 – Reprezentarea binară a mesajului**

| Caracter | C | r | i | p | t | a | r | e | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| **Hex** | 43 | 72 | 69 | 70 | 74 | 61 | 72 | 65 | 
| **Binar** | 01000011 | 01110010 | 01101001 | 01110000 | 01110100 | 01100001 | 01110010 | 01100101 | 

$$
M = 01000011 \quad 01110010 \quad 01101001 \quad 01110000 \quad 01110100 \quad 01100001 \quad 01110010 \quad 01100101
$$

**Pasul 7. Permutarea inițială IP(M) și separarea în** $L_0$ **și** $R_0$**:**

$$
IP(M) = 11111111 \quad 01011010 \quad 10010000 \quad 10100101 \quad 00000000 \quad 11111110 \quad 00000100 \quad 01000011
$$

* $L_0 = 11111111 \quad 01011010 \quad 10010000 \quad 10100101$

* $R_0 = 00000000 \quad 11111110 \quad 00000100 \quad 01000011$

**Pasul 8. Expansiunea** $E(R_0)$ **de la 32 la 48 biți:**
Aplicând tabelul E asupra lui $R_0$ obținem:

$$
E(R_0) = 100000 \quad 000001 \quad 011111 \quad 111100 \quad 000000 \quad 001000 \quad 001000 \quad 000110
$$

**Pasul 9. Operația XOR:** $K_1 \oplus E(R_0)$ **și împărțirea în 8 grupe** $B_1...B_8$**:**

$$
\begin{array}{rcl} K_1 &=& 111000 \quad 001011 \quad 111001 \quad 100110 \quad 100101 \quad 110000 \quad 001001 \quad 110000 \\ \oplus \quad E(R_0) &=& 100000 \quad 000001 \quad 011111 \quad 111100 \quad 000000 \quad 001000 \quad 001000 \quad 000110 \\ \hline K_1 \oplus E(R_0) &=& 011000 \quad 001010 \quad 100110 \quad 011010 \quad 100101 \quad 111000 \quad 000001 \quad 110110 \end{array}
$$

**Pasul 10. Substituția prin Cutiile S (**$S_1...S_8$**):**
Regula de citire: Pentru $B_j = b_1 b_2 b_3 b_4 b_5 b_6$, rândul este dat de biții margini $b_1 b_6$ (în baza 10: 0-3), iar coloana de biții din mijloc $b_2 b_3 b_4 b_5$ (în baza 10: 0-15).

**Tabelul 4.3 – Calculul ieșirilor cutiilor S**

| Cutia | Intrarea $B_j$ | Rândul ($b_1b_6$) | Coloana ($b_2...b_5$) | Valoarea găsită | Ieșirea binară (4 biți) | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| $S_1$ | `011000` | $00_2 = 0$ | $1100_2 = 12$ | 5 | `0101` | 
| $S_2$ | `001010` | $00_2 = 0$ | $0101_2 = 5$ | 11 | `1011` | 
| $S_3$ | `100110` | $10_2 = 2$ | $0011_2 = 3$ | 9 | `1001` | 
| $S_4$ | `011010` | $00_2 = 0$ | $1101_2 = 13$ | 12 | `1100` | 
| $S_5$ | `100101` | $11_2 = 3$ | $0010_2 = 2$ | 12 | `1100` | 
| $S_6$ | `111000` | $10_2 = 2$ | $1100_2 = 12$ | 1 | `0001` | 
| $S_7$ | `000001` | $01_2 = 1$ | $0000_2 = 0$ | 13 | `1101` | 
| $S_8$ | `110110` | $10_2 = 2$ | $1011_2 = 11$ | 13 | `1101` | 

Ieșire S-Box concatenată $= 0101 \quad 1011 \quad 1001 \quad 1100 \quad 1100 \quad 0001 \quad 1101 \quad 1101$

**Pasul 11. Aplicarea Permutării P (rezultatul funcției** $f$**):**
Permutăm cei 32 de biți obținuți conform tabelului P:

$$
f = P(S_1...S_8) = 0100 \quad 1111 \quad 0001 \quad 1100 \quad 1111 \quad 1001 \quad 0110 \quad 0011
$$

**Pasul 12. Calculul noilor jumătăți** $L_1$ **și** $R_1$**:**

* $L_1 = R_0 = 00000000 \quad 11111110 \quad 00000100 \quad 01000011$

* $R_1 = L_0 \oplus f$:

$$
\begin{array}{rcl} L_0 &=& 11111111 \quad 01011010 \quad 10010000 \quad 10100101 \\ \oplus \quad f &=& 01001111 \quad 00011100 \quad 11111001 \quad 01100011 \\ \hline R_1 &=& 10110000 \quad 01000110 \quad 01101001 \quad 11000110 \end{array}
$$

### PARTEA C: REZULTATUL ȘI FORMATAREA HEXAZECIMALĂ

**Pasul 13. Formarea blocului inversat** $R_1 L_1$**:**
Conform specificei structurii Feistel, la ieșirea din runda finală jumătățile se inversează ($R_1$ urmat de $L_1$):

$$
R_1 L_1 = 10110000 \quad 01000110 \quad 01101001 \quad 11000110 \quad 00000000 \quad 11111110 \quad 00000100 \quad 01000011
$$

**Pasul 14. Aplicarea Permutării Finale** $IP^{-1}$**:**

$$
IP^{-1}(R_1 L_1) = 00000110 \quad 00110011 \quad 00111001 \quad 00100100 \quad 01100000 \quad 01100100 \quad 00110111 \quad 01100001
$$

**Pasul 15. Conversia blocului cifrat în reprezentare Hexazecimală:**

**Tabelul 4.4 – Conversia binar-hexazecimală a rezultatului**

| Binar (grupe 4 biți) | 0000 | 0110 | 0011 | 0011 | 0011 | 1001 | 0010 | 0100 | 0110 | 0000 | 0110 | 0100 | 0011 | 0111 | 0110 | 0001 | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| **Hex** | 0 | 6 | 3 | 3 | 3 | 9 | 2 | 4 | 6 | 0 | 6 | 4 | 3 | 7 | 6 | 1 | 

**Textul cifrat final (**$C$**):**

$$
\mathbf{C = 0633392460643761}
$$

## 5. REZULTATE OBȚINUTE

1. **Mesajul și cheia selectate:** $m = \text{`Criptare`}$, $k = \text{`studenta`}$.

2. **Subcheia de rundă obținută:**

   $K_1 = \text{`111000 001011 111001 100110 100101 110000 001001 110000`}$

3. **Ieșirea funcției de rundă:**

   $f(R_0, K_1) = \text{`0100 1111 0001 1100 1111 1001 0110 0011`}$

4. **Blocul cifrat final (1 rundă DES, reprezentare Hex):**

   $$
   \mathbf{C = 0633392460643761}
   $$

## 6. CONCLUZII

În cadrul acestei lucrări de laborator am analizat și aplicat practic algoritmul de criptare simetrică DES (Data Encryption Standard) prin criptarea manuală a unui bloc de date de 64 de biți.

Iată principalele observații desprinse în urma parcurgerii pașilor de calcul:

1. Toate operațiile matematice utilizate sunt extrem de simple din punct de vedere computațional (XOR, permutări fixe, deplasări circulare de biți și substituții prin tabele predefinite), însă necesită o atenție deosebită la indexarea biților (unde prima poziție este numerotată de la 1, de la stânga la dreapta).

2. Substituția realizată prin cutiile S reprezintă singura etapă ne-liniară din tot algoritmul DES, oferind proprietatea esențială de *confuzie*.

3. Într-o versiune simplificată cu o singură rundă, securitatea oferită este nulă: jumătatea dreaptă $R_0$ este transmisă direct necriptată în jumătatea $L_1$, fiind expusă clar în blocul final. În algoritmul complet, repetarea rețelei Feistel pe parcursul celor 16 runde garantează un efect puternic de avalanșă și disipare a datelor.

4. Rezultatul obținut pentru blocul de intrare `Criptare` și cheia `studenta` este valoarea hexazecimală `0633392460643761`, confirmând corectitudinea calculelor efectuate.

# LUCRAREA DE LABORATOR NR. 6

## Informații invizibile: forensics și steganografie

### Lucrarea A — Decoder universal

Probele reproductibile au fost generate local cu `python probe/pregateste.py`. Fișierul `probe/mesaj.txt` conține codări URL, Base64 și hex în straturi succesive. Rularea decoderului cu `--fisier` a obținut:

```text
Strat detectat: hex
Rezultat: FLAG{straturi_decodate}
```

Decodarea a eliminat în ordine straturile URL, Base64 și hex. Fișa rezultată este salvată în `arsenal/forensics/fisa.json`.

Pentru `probe/xor.bin`, testarea celor 256 de chei de un octet a identificat cheia **90 (`0x5a`)** și mesajul:

```text
Mesaj XOR pentru laborator; alfabet imprimabil:  !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
```

Hash-urile din `probe/hashuri.txt` au fost căutate în wordlist-ul local. Rezultatele:

| Algoritm | Parola găsită |
|---|---|
| SHA-256 | `secretlab` |
| MD5 | `parola2026` |
| SHA-1 | `forensics` |

### Lucrarea B — Forensics pe fișiere și steganografie

Semnăturile binare au identificat `probe/foto.jpg` drept **JPEG** și `probe/ascuns.png` drept **PNG**, în acord cu extensiile. Extragerea șirurilor imprimabile din PNG a evidențiat numele `mesaj_ascuns.txt`.

Metadatele EXIF ale fotografiei conțin:

- Latitudine: **47° 00′ 00″ N** = **47.0**
- Longitudine: **28° 50′ 00″ E** = **28.833333°**

Arhiva ZIP lipită după imagine a fost extrasă în `gasit.zip`, începând de la octetul **361**. Fișierul din interior, `mesaj_ascuns.txt`, conține:

```text
Arhiva ascunsa extrasa cu succes din imagine.
```

Mesajul `FLAG{ascuns_in_pixeli}` a fost ascuns în biții cei mai puțin semnificativi ai pixelilor fotografiei, salvat fără pierderi în `stego.png` și recuperat identic.

### Rulare

```powershell
python probe/pregateste.py
python arsenal/forensics/decode.py probe/mesaj.txt --fisier
python arsenal/forensics/decode.py probe/xor.bin --xor
python arsenal/forensics/decode.py probe/hashuri.txt --wordlist probe/wordlist.txt
python arsenal/forensics/decode.py probe/challenge.bin --challenge
python forensics.py
python stego.py ascunde probe/foto.jpg "FLAG{ascuns_in_pixeli}" --iesire stego.png
python stego.py dezvaluie stego.png
python -m pytest -q
```

Scripturile de pregătire și analiză folosesc numai fișierele de probă generate local pentru această lucrare.

### Challenge opțional

Proba opțională `probe/challenge.bin` combină Base64 peste un XOR cu cheie de un octet. Fișierul `probe/challenge_hint.txt` indică pașii și hash-ul SHA-256 pentru verificare. Decoderul a recuperat mesajul `FLAG{challenge_decodat_si_verificat}`, cheia `0x37` și a confirmat hash-ul înainte de a raporta soluția.