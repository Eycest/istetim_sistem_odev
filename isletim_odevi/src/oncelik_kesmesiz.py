from yardimci import sure_hesapla, ort_maks, kac_tane_bitti, cpu_oran, degisim_say

def oncelik_kesmesiz_calistir(surecler):
    zaman = 0
    tablo = []
    kalanlar = surecler[:]

    oncelik_map = {
        "high": 0,
        "normal": 1,
        "low": 2
    }

    while kalanlar:
        gelenler = [s for s in kalanlar if s["g"] <= zaman]

        if not gelenler:
            siradaki = min(kalanlar, key=lambda x: x["g"])
            tablo.append((zaman, "IDLE", siradaki["g"]))
            zaman = siradaki["g"]
            continue

        secilen = min(gelenler, key=lambda x: oncelik_map.get(x["o"], 1))
        bas = zaman
        bit = zaman + secilen["s"]
        tablo.append((bas, secilen["id"], bit))
        zaman = bit
        kalanlar.remove(secilen)

    return tablo


def oncelik_kesmesiz_rapor(surecler, dosya_adi):
    tablo = oncelik_kesmesiz_calistir(surecler)

    bekle, donus = sure_hesapla(tablo)
    bek_ort, bek_maks = ort_maks(bekle)
    don_ort, don_maks = ort_maks(donus)
    thr = kac_tane_bitti(tablo, [50, 100, 150, 200])
    cpu = cpu_oran(tablo)
    cs = degisim_say(tablo)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("ONCELIK KESMESIZ ZAMAN TABLOSU\n")
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
