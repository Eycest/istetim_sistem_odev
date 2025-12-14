import os
import sys
import threading

from yardimci import dosyadan_cek

from fcfs import fcfs_rapor
from sjf_kesmesiz import sjf_kesmesiz_rapor
from sjf_kesmeli import sjf_kesmeli_rapor
from oncelik_kesmesiz import oncelik_kesmesiz_rapor
from oncelik_kesmeli import oncelik_kesmeli_rapor
from round_robin import round_robin_rapor


def kopya(liste):
    return [dict(x) for x in liste]


def calistir(case_yolu, etiket):
    surecler = dosyadan_cek(case_yolu)

    os.makedirs("cikti", exist_ok=True)

    isler = [
        (fcfs_rapor, kopya(surecler), os.path.join("cikti", f"fcfs_{etiket}.txt")),
        (sjf_kesmesiz_rapor, kopya(surecler), os.path.join("cikti", f"sjf_kesmesiz_{etiket}.txt")),
        (sjf_kesmeli_rapor, kopya(surecler), os.path.join("cikti", f"sjf_kesmeli_{etiket}.txt")),
        (oncelik_kesmesiz_rapor, kopya(surecler), os.path.join("cikti", f"oncelik_kesmesiz_{etiket}.txt")),
        (oncelik_kesmeli_rapor, kopya(surecler), os.path.join("cikti", f"oncelik_kesmeli_{etiket}.txt")),
        (lambda a, b: round_robin_rapor(a, b, q=4), kopya(surecler), os.path.join("cikti", f"round_robin_{etiket}.txt")),
    ]

    th = []
    for fn, s, yol in isler:
        t = threading.Thread(target=fn, args=(s, yol))
        t.start()
        th.append(t)

    for t in th:
        t.join()


def main():
    case1 = os.path.join("veri", "case1.csv")
    case2 = os.path.join("veri", "case2.csv")

    if len(sys.argv) == 2:
        tek = sys.argv[1].strip().lower()
        if tek in ["1", "case1"]:
            calistir(case1, "case1")
            return
        if tek in ["2", "case2"]:
            calistir(case2, "case2")
            return

    calistir(case1, "case1")
    calistir(case2, "case2")


if __name__ == "__main__":
    main()
