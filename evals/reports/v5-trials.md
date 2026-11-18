# Uji agent untuk Malas Engineer v5.0.0

Pada 18 November 2026, 16 agent menyelesaikan dua tugas di Windows. Masing-masing mendapat salinan fixture baru dan prompt yang sama untuk tugasnya. Pemeriksa dijalankan terpisah setelah agent selesai. Kolom di bawah menunjukkan jumlah pemeriksaan perilaku yang lulus, dijumlahkan untuk dua percobaan per kondisi.

| Instruksi tambahan | Python, 10 pemeriksaan × 2 | JavaScript, 5 pemeriksaan × 2 |
| --- | ---: | ---: |
| Tanpa skill yang ditugaskan | 16/20 | 10/10 |
| Malas Engineer v4.1.0 | 16/20 | Tidak dijalankan |
| Draf lokal sebelum revisi | 16/20 | Tidak dijalankan |
| Superpowers verification-before-completion | 16/20 | 10/10 |
| Malas Engineer v5.0.0 | **20/20** | **10/10** |

### Python, tugas yang dipakai untuk memperbaiki skill

Pengguna meminta input pipe dan stream untuk penghitung JSON Lines yang sebelumnya membaca file UTF-8. Keempat kondisi pembanding berhasil mempertahankan nama file literal `-`, signature keyword, dan kepemilikan stream. Seluruhnya melewatkan dua kasus pada CLI. Dengan konfigurasi stdin ASCII ketat, input UTF-8 yang sah ditolak. Dengan penanganan kesalahan `surrogateescape`, byte yang ditolak oleh jalur file justru diterima dari pipe. Tes yang ditulis agent sendiri lulus di kedua keadaan implementasi yang berbeda itu.

Setelah kegagalan awal terlihat, dua pemeriksaan encoding ditambahkan ke delapan pemeriksaan pertama. Seluruh keluaran, termasuk kontrol awal, dinilai ulang dengan sepuluh pemeriksaan yang sama. Instruksi v5 meminta agent membandingkan jalur yang menjanjikan hasil sama memakai input valid dan rusak sambil mengubah default runtime yang berpengaruh. Kedua agent v5 menulis tes subprocess yang menangkap perbedaan tersebut. Keduanya mengubah konfigurasi stdin di fungsi CLI. Pemanggil yang mengimpor dan menjalankan fungsi CLI di proses sendiri dapat melihat efek itu. Kontrak stream milik pemanggil diuji pada API library.

### JavaScript, tugas baru setelah instruksi dibekukan

Sebuah layanan harus membagikan satu pemuatan yang masih berjalan kepada dua pemanggil. Pemeriksa menguji view default, pemisahan pasangan key/view dan instance, propagasi error asli, serta pemuatan ulang setelah sukses atau gagal. Pemeriksa ditetapkan sebelum percobaan. Ketiga kondisi lulus seluruh pemeriksaan. Tidak ada selisih terukur pada tugas ini.

### Metode dan cakupan

- Semua agent memakai harness kolaborasi yang sama, tanpa riwayat percakapan induk. Setiap kondisi menetapkan satu dokumen skill atau tidak menetapkan skill tambahan. Instruksi sistem dan alat bawaan tetap berlaku. Perbandingan Superpowers memakai satu [skill verifikasi pada revisi tetap](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/verification-before-completion/SKILL.md).
- Pemeriksa disimpan di luar folder tugas. Setelah tiap percobaan, tes buatan agent dijalankan pada hasil akhir dan pada fixture asli. Semua suite lulus pada hasil akhir dan mengembalikan status gagal pada kode asli. Tidak ada koreksi manual pada keluaran yang dinilai.
- Sembilan sesi terputus saat percakapan dilanjutkan, sebelum ada perubahan implementasi pada folder tersebut. Penggantinya mulai dari fixture baru. Percobaan awal yang tidak selesai tidak masuk tabel.
- Model revision persis, token dan biaya tidak tersedia untuk perbandingan. Dua pengulangan per kondisi dan dua tugas belum cukup untuk peringkat lintas proyek. Tugas Python digunakan untuk menyetel instruksi. Tugas JavaScript menguji penerapannya pada pekerjaan lain.

### Discovery pada Codex CLI

Dua sesi baru Codex CLI 0.146.0 berjalan dengan `--ephemeral --ignore-user-config --sandbox read-only`. Direktori uji memiliki skill di `.agents/skills/malas-engineer/`. Prompt review tidak menyebut nama skill. Agent memilihnya dan mencoba membaca salinan lokal. Kebijakan eksekusi menolak perintah baca `rtk`, sehingga sesi ini hanya membuktikan pemilihan dan percobaan membaca. Prompt terjemahan dijawab langsung tanpa pembacaan skill. Satu contoh per jenis belum mengukur akurasi pemicu. Aktivasi Claude Code dan Hermes belum diuji.

### Mengulang penilaian

Unduh [keluaran lengkap](v5/outputs.zip) dan lihat [hasil per percobaan](v5/results.json). Arsip menyimpan direktori untuk setiap tugas dan kondisi, termasuk source dan tes buatan agent. Hasil JSON menyimpan exit code, nama kasus gagal dan hash konteks. Untuk mengulang dari root repo di PowerShell setelah mengekstrak arsip ke direktori `outputs`, jalankan:

```powershell
python evals/check_stream_trial.py outputs/stream/v5-1
$env:TRIAL_DIR = (Resolve-Path outputs/refresh/v5-1).Path
node --test evals/check_refresh_trial.cjs
```

Prompt dan kode awal ada dalam [fixture Python](../fixtures/stream-task) dan [fixture JavaScript](../fixtures/refresh-task). Gunakan fixture asli sebagai kontrol negatif. Kedua pemeriksa harus mengembalikan exit code 1.
