English translation using AI [README.md](README-EN.md)

## Deskripsi

fork dari [NeverCrisis](https://github.com/DelistedCloud/NeverCrisis). Bagian utamanya tidak dimodifikasi dan download dari [NeverCrisis Releases](https://github.com/DelistedCloud/NeverCrisis/releases) aslinya disana. NeverCrisis disana adalah untuk instalasi windows. Yang ada disini hanyalah wrapper/script tambahan untuk menjalankan server offline di linux. Saya bukan ahli dalam pemrograman, script ini menggunakan bantuan dari Gemini AI.

## PENGGUNAAN

Catatan pribadi jika saya sudah menghapus dan ternyata setelah sekian waktu ingin main lagi.

Bersasarkan trik terbaru dari beberapa diskusi [issue](https://github.com/DelistedCloud/NeverCrisis/issues/3).
ada yang share panduan dalam bentuk [file pdf](https://cdn.discordapp.com/attachments/1557193074399117322/1557193074562703471/NeverCrisis-Setup-Guide-V2.1.pdf?backend=b2&ex=6ac79150&is=6ac63fd0&hm=4a9f4b74748033522a7d5acc1da3c0b594a0d0a38de4c6324735951e69fd449d&), intinya file yang didownload dari release `NeverCrisis` disimpan folder instalasi game, kecuali bagian folder `save` ditempatkan di lokasi berbeda. Untuk lokasi versi linux ada di dalam direktory steam prefix
`../../compatdata/2484110/pfx/drive_c/users/steamuser/Documents/My Games/FF7EC/Steam`.

di diskusi tersebut juga ada petunjuk mendownload data game. Untuk versi linux bisa menggunakan `steamdepotdownloader` atau `steamdepotdowanloadergui`. Tapi sepertinya memerlukan login Steam dan hanya untuk yang pernah memainkan game online resmi sebelum EOS.

membutuhkan `libfaketime`: 
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
- sekitar line 72: untuk mengubah tanggal. gamenya EOS tanggan 7 Oktober 2026, ada update perubahan file saat tanggal 5 Oktober 2026, saat ini tercantum 4 Oktober 2026. mungkin butuh untuk memanipulasi login reward, hanya disarankan tanggal-tanggal sebelum 5 oktober.

**server_args.txt** adalah file menggunakan tambahan option seperti `--give item...` atau `--reopen-events` . Option ini akan otomatis disertakan saat mengeksekusi file `./start_offline.sh`. List ID itemnya ada didalam sebuah file items.txt termasuk didalam release `NeverCrisis` aslinya.

Untuk menjalankan game dari mengeksekusi `start_offline.sh`. Pastikan terminal berada dalam direktori tempat script ini berada.
> ./start_offline.sh


## Catatan Gameplay, Masalah dengan triknya
Karena sudah pasti tidak semua berjalan seperti sebelum EOS. Beberapa sudah disebutkan di page `NeverCrisis`. Dan ini tambahan yang terjadi di saya. Untuk trik kebanyakan jadi bergantung ke opsi --give item dari `NeverCrisis`.

- padahal offline, tapi jika tersambung ke internet, stuck/blank di launcher setelah "click to start". Hanya bisa masuk jika memutuskan semua jaringan (ada blank sih sebentar).
- di game aslinya. jika dapat weapon ganda akan dapat 200 weapon parts (dari gacha atau dari exchange currency). tapi sekarang hanya dapat 1. jadi dari disarankan tambah dari --give item weapon part per karakter.
- unlock costume/gear sepertinya terkumpul semua di exchange > `gear 3rd anniversary gear` voucher. jadi ambil vouchernya dari --give juga. beberapa costume seperti aerith chocobo atau zack swimsuit excange dari event.
- weapon event juga terkumpul di event sephiroth terbaru. jadi ambil `sephiroth certificate` dari --give item dan exchange di page event.
- memoria tidak bisa drop dari melakukan event. Tapi masih bisa diambil dari exchange > medal > co-op medal (offline gak bisa co-op, juga dari opsi --give)
- materia elemen dan ruin terkumpul di exchange > enhancement > 5* materia
- menaikan level materia hanya bisa menggunakan materia lain.

## Masalah belum ada triknya
- tidak bisa memulai misi summon.
- tidak bisa unlock TUNING, karakter rolestream meski semua misi terpenuhi. rolestream treenya masih bisa.
- tidak bisa buka chocobo farm, stuck di loading stream.
- `Umbral Sword` katanya hanya dari event login 1.5 anniversary dan selain dari itu, tidak tahu darimana lagi cara dapatnya.

## Apa lagi ya?
seperti yang dibilang diawal saya bukan ahli. Jadi tidak akan bisa menanggapi issue. Maaf.