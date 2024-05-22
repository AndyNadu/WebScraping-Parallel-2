Am utilizat tehnica de web scraping pentru a scoate anumite informatii dintr-un site la alegere (tiriac auto - rulate ). Functia deschide site ul, isi colecteaza datele necesare, iar apoi le foloseste pentru a determina:
  - Grafice
  - Cea mai scumpa masina
  - Cea mai ieftina masina
  - Media preturilor
  - Numarul total de masini extrase de pe site

Ca limbaj de programare am folosit Python, unde am importat anumite librarii:
  - Re (pentru expresii regulate)
  - Beautifoul soup (pentru extragerea datelor)
  - Matlotlib (pentru grafice / mesaje text de afisare)
  - Requests (pentru apelarea unui url)
  - Concurrent.Futures pentru paralelizare
  - report.lab.pagesizes, report.platypus, reportlab.lib.styles pentru crearea, stilizarea fisierului pdf
    
Masina de pe care am rulat aplicatia are urmatoarele caracteristici:
  - Procesor: 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz 2.80 GHz
  - Placa video integrata
  - Memorie RAM DDR4: 16.0GB 4200mHz
  - Sistem de operare: Windows 11
