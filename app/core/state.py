from app.ai.ai_engine import generate_answer

conversation_state = "WAIT_MENU"
conversation_data = {}

def reset_conversation():
    global conversation_state, conversation_data
    conversation_state = "WAIT_MENU"
    conversation_data.clear()


def handle_message(user_message: str) -> str:
    global conversation_state, conversation_data

    # =========================
    # STATE: WAIT_MENU
    # =========================
    if conversation_state == "WAIT_MENU":

        if user_message not in ["1", "2", "3"]:
            return "Pilihan tidak valid. Silakan masukkan angka 1, 2, atau 3."

        menu_map = {
            "1": "mata_kuliah",
            "2": "mbkm",
            "3": "informasi_umum",
        }

        conversation_data.clear()
        conversation_data["menu"] = menu_map[user_message]

        if user_message == "1":
            conversation_state = "WAIT_SEMESTER"
            return (
                "Silakan masukkan semester yang diinginkan (1–8).\n"
                "0. Kembali ke menu utama"
            )

        conversation_state = "WAIT_SUB_MENU"

        if user_message == "2":
            return (
                "Silakan pilih topik MBKM:\n"
                "1. Jenis Program MBKM\n"
                "2. Konversi SKS\n"
                "3. Syarat dan Ketentuan\n"
                "0. Kembali ke menu utama"
            )

        return (
            "Silakan pilih informasi yang diinginkan:\n"
            "1. Visi dan Misi Program Studi\n"
            "2. Profil Lulusan\n"
            "3. Dosen dan Fasilitas\n"
            "0. Kembali ke menu utama"
        )

    # =========================
    # STATE: WAIT_SEMESTER
    # =========================
    if conversation_state == "WAIT_SEMESTER":

        if user_message == "0":
            reset_conversation()
            return (
                "Kembali ke menu utama.\n"
                "Silakan pilih menu berikut:\n"
                "1. Mata Kuliah\n"
                "2. MBKM\n"
                "3. Informasi Umum"
            )

        if not user_message.isdigit() or not (1 <= int(user_message) <= 8):
            return "Semester tidak valid. Masukkan angka 1 sampai 8 atau 0 untuk kembali."

        conversation_data["semester"] = user_message
        conversation_state = "WAIT_QUESTION"
        return "Silakan tuliskan pertanyaan Anda."

    # =========================
    # STATE: WAIT_SUB_MENU
    # =========================
    if conversation_state == "WAIT_SUB_MENU":

        if user_message == "0":
            reset_conversation()
            return (
                "Kembali ke menu utama.\n"
                "Silakan pilih menu berikut:\n"
                "1. Mata Kuliah\n"
                "2. MBKM\n"
                "3. Informasi Umum"
            )

        if not user_message.isdigit():
            return "Input tidak valid. Masukkan angka sesuai pilihan atau 0 untuk kembali."

        choice = int(user_message)

        if conversation_data["menu"] == "mbkm":
            submenu_map = {
                1: "jenis_program_mbkm",
                2: "konversi_sks",
                3: "syarat_dan_ketentuan",
            }

        elif conversation_data["menu"] == "informasi_umum":
            submenu_map = {
                1: "visi_dan_misi",
                2: "profil_lulusan",
                3: "dosen_dan_fasilitas",
            }

        else:
            return "Terjadi kesalahan menu."

        if choice not in submenu_map:
            return "Pilihan tidak tersedia. Silakan pilih angka yang sesuai atau 0 untuk kembali."

        conversation_data["sub_menu"] = submenu_map[choice]
        conversation_state = "WAIT_QUESTION"
        return "Silakan tuliskan pertanyaan Anda."

    # =========================
    # STATE: WAIT_QUESTION
    # =========================
    if conversation_state == "WAIT_QUESTION":

        if user_message == "0":
            reset_conversation()
            return (
                "Kembali ke menu utama.\n"
                "Silakan pilih menu berikut:\n"
                "1. Mata Kuliah\n"
                "2. MBKM\n"
                "3. Informasi Umum"
            )

        conversation_data["question"] = (
            user_message if user_message.strip()
            else "Jelaskan informasi terkait."
        )

        ai_context = {
            "menu": conversation_data.get("menu"),
            "sub_menu": conversation_data.get("sub_menu"),
            "semester": conversation_data.get("semester"),
            "question": conversation_data.get("question"),
        }

        answer = generate_answer(ai_context)

        return (
            f"{answer}\n\n"
        )


