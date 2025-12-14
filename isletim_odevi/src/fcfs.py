from yardimci import sure_hesapla, ort_maks, kac_tane_bitti, cpu_oran, degisim_say

def fcfs_calistir(surecler):
    surecler = sorted(surecler, key=lambda x: x["g"])
    zaman = 0
    tablo = []

    for s in surecler:
        if zaman < s["g"]:
            tablo.append((zaman, "IDLE", s["g"]))
            zaman = s["g"]

        bas = zaman
        bit = zaman + s["s"]
        tablo.append((bas, s["id"], bit))
        zaman = bit

    return tablo


def fcfs_rapor(surecler, dosya_adi):
    tablo = fcfs_calistir(surecler)

    bekle, donus = sure_hesapla(tablo)
    bek_ort, bek_maks = ort_maks(bekle)
    don_ort, don_maks = ort_maks(donus)
    thr = kac_tane_bitti(tablo, [50, 100, 150, 200])
    cpu = cpu_oran(tablo)
    cs = degisim_say(tablo)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("FCFS ZAMAN TABLOSU\n")
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
