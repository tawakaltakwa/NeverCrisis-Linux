#!/usr/bin/env bash
# ==============================================================================
# FINAL FANTASY VII EVER CRISIS - Offline Server & Game Launcher (Linux)
# ==============================================================================

set -e

GAME_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${GAME_DIR}"

STEAM_ROOT="/home/kal/SagalaAya/data/share/Steam"
COMPAT_DATA="${STEAM_ROOT}/steamapps/compatdata/2484110"
PROTON_BIN="${STEAM_ROOT}/steamapps/common/Proton - Experimental/proton"
ARGS_FILE="${GAME_DIR}/server_args.txt"
LOG_FILE="${GAME_DIR}/server.log"

echo "============================================================"
echo "  FINAL FANTASY VII EVER CRISIS - Offline Mode Launcher"
echo "============================================================"

# 1. Cek port unprivileged untuk port 443
CURRENT_PORT_START=$(cat /proc/sys/net/ipv4/ip_unprivileged_port_start 2>/dev/null || echo 1024)
if [ "${CURRENT_PORT_START}" -gt 443 ]; then
    echo ""
    echo "[PERINGATAN] Port 443 masih dibatasi oleh kernel Linux!"
    echo "Server offline membutuhkan izin untuk bind ke port 443."
    echo "Silakan jalankan perintah ini di Terminal sekali:"
    echo ""
    echo "  sudo sysctl -w net.ipv4.ip_unprivileged_port_start=443"
    echo ""
    echo "Atau agar permanen setelah reboot:"
    echo "  echo 'net.ipv4.ip_unprivileged_port_start = 443' | sudo tee /etc/sysctl.d/50-unprivileged-ports.conf && sudo sysctl --system"
    echo ""
    echo "Menunggu 5 detik sebelum melanjutkan..."
    sleep 5
fi

# 2. Baca argumen dari server_args.txt
EXTRA_ARGS=()
if [ -f "${ARGS_FILE}" ]; then
    while IFS= read -r line || [ -n "$line" ]; do
        # Abaikan komentar (#) dan baris kosong
        line="$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
        if [[ -n "$line" && ! "$line" =~ ^# ]]; then
            # Split kata jika dalam satu baris terdapat lebih dari satu argumen
            for word in $line; do
                EXTRA_ARGS+=("$word")
            done
        fi
    done < "${ARGS_FILE}"
fi

if [ ${#EXTRA_ARGS[@]} -gt 0 ]; then
    echo "[INFO] Argumen server aktif: ${EXTRA_ARGS[*]}"
else
    echo "[INFO] Tidak ada argumen server tambahan (default)."
fi

# 3. Penyesuaian Tanggal Sistem (Bypass batas waktu End of Service / EOS)
# Game hardcoded menolak login jika tanggal sistem > 6 Oktober 2026.
# Kita mundurkan tanggal sementara ke 4 Oktober 2026, lalu otomatis dikembalikan saat game ditutup.
SYSTEM_DATE_MODIFIED=0
CURRENT_EPOCH=$(date +%s)
EOS_LIMIT_EPOCH=$(date -d "2026-10-06 00:00:00" +%s 2>/dev/null || echo 1791244800)

if [ "${CURRENT_EPOCH}" -gt "${EOS_LIMIT_EPOCH}" ]; then
    echo ""
    echo "[INFO] Tanggal sistem terdeteksi melewati batas End of Service (EOS)."
    echo "[INFO] Membutuhkan hak akses sudo untuk memundurkan tanggal sementara ke 4 Okt 2026."
    echo "[INFO] (Tanggal akan otomatis dikembalikan ke normal saat game selesai dimainkan)."
    echo ""
    if sudo timedatectl set-ntp false 2>/dev/null && sudo date -s "2025-03-10 12:00:00" 2>/dev/null; then
        echo "[OK] Tanggal sistem berhasil diset sementara ke: $(date)"
        SYSTEM_DATE_MODIFIED=1
    else
        echo "[PERINGATAN] Gagal memundurkan tanggal. Game mungkin tertahan di Title Screen."
    fi
fi

# 4. Fungsi pembersihan saat keluar (Otomatis restore jam & matikan proses)
cleanup() {
    echo ""
    echo "[INFO] Menutup sesi game & offline server..."
    pkill -f "FF7ECServer.exe" 2>/dev/null || true
    pkill -f "FF7EC.exe" 2>/dev/null || true
    
    if [ "${SYSTEM_DATE_MODIFIED}" -eq 1 ]; then
        echo "[INFO] Mengembalikan jam & tanggal sistem ke otomatis (NTP)..."
        sudo timedatectl set-ntp true 2>/dev/null || true
        echo "[OK] Tanggal sistem dikembalikan: $(date)"
    fi
    echo "[INFO] Selesai. Sampai jumpa!"
}
trap cleanup EXIT INT TERM

# 5. Jalankan FF7ECServer.exe melalui Proton
# Catatan penting: FF7ECServer.exe sudah otomatis meluncurkan FF7EC.exe
# dan menunggu sampai game ditutup, sehingga tidak perlu meluncurkan FF7EC.exe terpisah.
echo "[INFO] Memulai FF7ECServer.exe (Otomatis meluncurkan 1 jendela game FF7EC)..."
export STEAM_COMPAT_CLIENT_INSTALL_PATH="${STEAM_ROOT}"
export STEAM_COMPAT_DATA_PATH="${COMPAT_DATA}"

# Pastikan tidak ada wineserver menggantung dari sesi sebelumnya
"${PROTON_BIN}" run "${GAME_DIR}/FF7ECServer.exe" "${EXTRA_ARGS[@]}"


