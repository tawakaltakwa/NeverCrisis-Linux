English translation using AI [README.md](README-EN.md)

Hanya catatan pribadi jika saya sudah menghapus dan ternyata setelah sekian waktu ingin main lagi.

## Deskripsi

fork dari [NeverCrisis](https://github.com/DelistedCloud/NeverCrisis). Yang ada disini hanyalah wrapper/script tambahan untuk menjalankan server offline di linux. Saya bukan ahli dalam pemrograman, script ini menggunakan bantuan dari Gemini AI.

Untuk offline servernya sendiri bisa menggunakan sebagai berikut:
1. [NeverCrisis Delisted Cloud](https://github.com/DelistedCloud/NeverCrisis) - ini adalah main repository.
2. [NeverCrisis ShadowMPo](https://github.com/ShadowMPo/NeverCrisis) - salah satu fork dari Delisted Cloud yang aktif, ada update perbaikan dari versi Delisted Cloud.

## PENGGUNAAN

Bersasarkan trik terbaru dari beberapa diskusi [issue](https://github.com/DelistedCloud/NeverCrisis/issues/3).
ada yang share panduan dalam bentuk [file pdf](NeverCrisis-Setup-Guide-V2.1.pdf), intinya file yang didownload dari release `NeverCrisis` disimpan folder instalasi game, kecuali bagian folder `save` ditempatkan di lokasi berbeda. Untuk lokasi versi linux ada di dalam direktory steam prefix
`../../compatdata/2484110/pfx/drive_c/users/steamuser/Documents/My Games/FF7EC/Steam/NUMBERID`. `NUMBERID` adalah nomor id dari file `ff7ec_account_id.txt`.

di diskusi tersebut juga ada petunjuk mendownload data game. Untuk versi linux bisa menggunakan `steamdepotdownloader` atau `steamdepotdowanloadergui`. Tapi sepertinya memerlukan login Steam dan hanya untuk yang pernah memainkan game online resmi sebelum EOS.

membutuhkan `libfaketime` jika ingin memanipulasi tanggal, wajib jika menggunakan versi `DelistedCloud`, opsional jika menggunakan versi `ShadowMPo`: 
> sudo pacman -S libfaketime

perizinan server (port 443) hanya dibutuhkan sekali: 
> sudo sysctl -w net.ipv4.ip_unprivileged_port_start=443

mengedit hosts:
```
sudo sh -c 'cat << "EOF" >> /etc/hosts  
   
# FF7EC Offline Server  
127.0.0.1 game-q74z3cyn.app.gl.ffviiec.com  
127.0.0.1 resources-api-c9ps53g2.app.gl.ffviiec.com  
127.0.0.1 client-masterdata-c9ps53g2.app.gl.ffviiec.com  
127.0.0.1 chat-pd381ne.app.gl.ffviiec.com  
EOF'  
``` 

ada 2 file disalin ke dalam direktori game FF7EC:
- [start_offline.sh](start_offline.sh)
- [server_args.txt](server_args.txt)

**start_offline.sh** adalah file untuk menjalankan server offline. Yang tercantum di dalam berdasarkan PC saya saat dibuat, jadi ada yang harus di cek dan mungkin disesuaikan ulang dari file ini sebagai berikut:
- sekitar line 11: STEAM_ROOT: isinya direktori Steam. Instalan default biasanya di ~/.local/share/Steam. Biasanya ada berisi folder compatibilitytools.d, steam, steamapps, ubuntu12_32, ubuntu12_64, linux32, linux64, dan lain sebagainya.
- sekitar line 12: COMPAT_DATA: isinya direktori compatdata/sream prefix game.
- sekitar line 13: PROTON_BIN: isinya direktori proton. Saat ini menggunakanPROTON experimental.
- jika menggunakan versi `ShadowMPo`, sudah di fix tanggal EOS, mengubah tanggal tidak wajib, jadi sekitar line 59 sampai line 94 bisa di nonaktifkan dengan cara dijadikan comment (menambahkan `#` pada tiap baris).
- jika menggunakan versi `Delisted Cloud`, sekitar line 72: untuk mengubah tanggal. gamenya EOS tanggan 7 Oktober 2026, ada update perubahan file saat tanggal 5 Oktober 2026, saat ini tercantum 4 Oktober 2026. BTW. manipulasi waktu ini berguna di `Delisted Cloud` dan `ShadowMPo` untuk memanipulasi login reward dari event tertentu atau membuka banner gacha Gratitude Event jika di set ke tanggal 29 Juli 2026. atau mungkin coba-coba ke tanggal lebih lama lagi.

**server_args.txt** adalah file menggunakan tambahan option seperti `--give item...` atau `--reopen-events` . Option ini akan otomatis disertakan saat mengeksekusi file `./start_offline.sh`. List ID itemnya ada didalam sebuah file items.txt termasuk didalam release `NeverCrisis` aslinya.

Untuk menjalankan game dari mengeksekusi `start_offline.sh`. Pastikan terminal berada dalam direktori tempat script ini berada.
> ./start_offline.sh

## Apa lagi ya?
seperti yang dibilang diawal saya bukan ahli. Jadi tidak akan bisa menanggapi issue. Maaf.