from yardimci import sure_hesapla, ort_maks, kac_tane_bitti, cpu_oran, degisim_say

def round_robin_calistir(surecler, q=4):
    kalanlar = []
    for s in surecler:
        kalanlar.append({
            "id": s["id"],
            "g": s["g"],
            "s": s["s"],
            "k": s.get("k", s["s"]),
            "o": s["o"]
        })

    zaman = 0
    tablo = []

    hazir = []
    bitti = 0
    toplam = len(kalanlar)

    eklendi = set()

    def yeni_gelenleri_ekle(t):
        deg = False
        for x in kalanlar:
            if x["id"] in eklendi:
                continue
            if x["g"] <= t and x["k"] > 0:
                hazir.append(x)
                eklendi.add(x["id"])
                deg = True
        return deg

    yeni_gelenleri_ekle(zaman)

    while bitti < toplam:
        if not hazir:
            kalan_isler = [x for x in kalanlar if x["k"] > 0]
            if not kalan_isler:
                break
            sonraki = min(kalan_isler, key=lambda x: x["g"])["g"]
            if zaman < sonraki:
                tablo.append((zaman, "IDLE", sonraki))
                zaman = sonraki
            yeni_gelenleri_ekle(zaman)
            continue

        s = hazir.pop(0)

        if zaman < s["g"]:
            tablo.append((zaman, "IDLE", s["g"]))
            zaman = s["g"]

        bas = zaman
        calis = q if s["k"] > q else s["k"]

        for _ in range(calis):
            zaman += 1
            s["k"] -= 1
            yeni_gelenleri_ekle(zaman)
            if s["k"] == 0:
                break

        tablo.append((bas, s["id"], zaman))

        if s["k"] == 0:
            bitti += 1
        else:
            hazir.append(s)

        yeni_gelenleri_ekle(zaman)

    tablo2 = []
    for b, p, s in tablo:
        if tablo2 and tablo2[-1][1] == p and tablo2[-1][2] == b:
            tablo2[-1] = (tablo2[-1][0], p, s)
        else:
            tablo2.append((b, p, s))

    return tablo2


def round_robin_rapor(surecler, dosya_adi, q=4):
    tablo = round_robin_calistir(surecler, q=q)

    bekle, donus = sure_hesapla(tablo, surecler)
    bek_ort, bek_maks = ort_maks(bekle)
    don_ort, don_maks = ort_maks(donus)
    thr = kac_tane_bitti(tablo, [50, 100, 150, 200])
    cpu = cpu_oran(tablo)
    cs = degisim_say(tablo)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write(f"ROUND ROBIN (q={q}) ZAMAN TABLOSU\n")
        for b, p, s in tablo:
            f.write(f"[ {b} ] -- {p} -- [ {s} ]\n")

        f.write("\n")
        f.write(f"Ortalama Bekleme: {bek_ort}\n")
        f.write(f"Maksimum Bekleme: {bek_maks}\n\n")

        f.write(f"Ortalama Donus: {don_ort}\n")
        f.write(f"Maksimum Donus: {don_maks}\n\n")

        f.write("Throughput\n")
        for t in thr:
            f.write(f"T={t}: {thr[t]}\n")

        f.write("\n")
        f.write(f"CPU Verimliligi: {cpu}\n")
        f.write(f"Context Switch Sayisi: {cs}\n")
