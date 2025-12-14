from yardimci import sure_hesapla, ort_maks, kac_tane_bitti, cpu_oran, degisim_say

def sjf_kesmeli_calistir(surecler):
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

    toplam_is = len(kalanlar)
    bitti = 0

    aktif = None
    basla = 0

    while bitti < toplam_is:
        hazir = [x for x in kalanlar if x["g"] <= zaman and x["k"] > 0]

        if not hazir:
            sonraki_gelis = min([x["g"] for x in kalanlar if x["k"] > 0])
            if aktif is not None:
                tablo.append((basla, aktif, zaman))
                aktif = None
            if zaman < sonraki_gelis:
                tablo.append((zaman, "IDLE", sonraki_gelis))
                zaman = sonraki_gelis
            continue

        sec = min(hazir, key=lambda x: (x["k"], x["g"], x["id"]))

        if aktif != sec["id"]:
            if aktif is not None:
                tablo.append((basla, aktif, zaman))
            aktif = sec["id"]
            basla = zaman

        sec["k"] -= 1
        zaman += 1

        if sec["k"] == 0:
            bitti += 1

    if aktif is not None:
        tablo.append((basla, aktif, zaman))

    tablo2 = []
    for b, p, s in tablo:
        if tablo2 and tablo2[-1][1] == p and tablo2[-1][2] == b:
            tablo2[-1] = (tablo2[-1][0], p, s)
        else:
            tablo2.append((b, p, s))

    return tablo2


def sjf_kesmeli_rapor(surecler, dosya_adi):
    tablo = sjf_kesmeli_calistir(surecler)

    bekle, donus = sure_hesapla(tablo, surecler)
    bek_ort, bek_maks = ort_maks(bekle)
    don_ort, don_maks = ort_maks(donus)
    thr = kac_tane_bitti(tablo, [50, 100, 150, 200])
    cpu = cpu_oran(tablo)
    cs = degisim_say(tablo)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("SJF KESMELI ZAMAN TABLOSU\n")
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
