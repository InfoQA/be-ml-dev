def _prompt_mata_kuliah(
    semester: str,
    question: str,
    retrieved_context: str
) -> str:
    return f"""
Konteks Akademik:
- Topik    : Kurikulum dan Mata Kuliah
- Semester : {semester}

Informasi Referensi:
{retrieved_context if retrieved_context else "Tidak ada dokumen tambahan."}

Instruksi:
Jawablah pertanyaan mahasiswa berdasarkan konteks di atas.
Fokus pada:
- daftar mata kuliah
- deskripsi singkat
- bobot SKS
- prasyarat mata kuliah

Pertanyaan Mahasiswa:
{question}
""".strip()

def _prompt_mbkm(
    sub_menu: str,
    question: str,
    retrieved_context: str
) -> str:
    sub_menu_map = {
        "jenis_program_mbkm": "Jenis Program MBKM",
        "konversi_sks": "Konversi SKS",
        "syarat_dan_ketentuan": "Syarat dan Ketentuan MBKM"
    }

    return f"""
Konteks Akademik:
- Topik    : Merdeka Belajar Kampus Merdeka (MBKM)
- Subtopik : {sub_menu_map.get(sub_menu, "Umum")}

Informasi Referensi:
{retrieved_context if retrieved_context else "Tidak ada dokumen tambahan."}

Instruksi:
Berikan penjelasan yang jelas, ringkas, dan terstruktur
sesuai kebijakan MBKM.

Pertanyaan Mahasiswa:
{question}
""".strip()

def _prompt_informasi_umum(
    sub_menu: str,
    question: str,
    retrieved_context: str
) -> str:
    sub_menu_map = {
        "visi_dan_misi": "Visi dan Misi Program Studi",
        "profil_lulusan": "Profil Lulusan",
        "dosen_dan_fasilitas": "Dosen dan Fasilitas"
    }

    return f"""
Konteks Akademik:
- Topik    : Informasi Umum Program Studi
- Subtopik : {sub_menu_map.get(sub_menu, "Umum")}

Informasi Referensi:
{retrieved_context if retrieved_context else "Tidak ada dokumen tambahan."}

Instruksi:
Sampaikan informasi faktual dan terstruktur
sesuai dengan Program Studi Teknik Informatika.

Pertanyaan Mahasiswa:
{question}
""".strip()

def _prompt_default(
    question: str,
    retrieved_context: str
) -> str:
    return f"""
Informasi Referensi:
{retrieved_context if retrieved_context else "Tidak ada dokumen tambahan."}

Pertanyaan Pengguna:
{question}

Berikan jawaban yang relevan dan informatif.
""".strip()

def build_prompt(context: dict) -> str:
    menu = context.get("menu")
    sub_menu = context.get("sub_menu")
    semester = context.get("semester")
    question = context.get("question")
    retrieved_context = context.get("retrieved_context", "")

    # ==============================
    # MENU 1 — MATA KULIAH
    # ==============================
    if menu == "mata_kuliah":
        return _prompt_mata_kuliah(
            semester, question, retrieved_context
        )

    # ==============================
    # MENU 2 — MBKM
    # ==============================
    if menu == "mbkm":
        return _prompt_mbkm(
            sub_menu, question, retrieved_context
        )

    # ==============================
    # MENU 3 — INFORMASI UMUM
    # ==============================
    if menu == "informasi_umum":
        return _prompt_informasi_umum(
            sub_menu, question, retrieved_context
        )

    # ==============================
    # FALLBACK
    # ==============================
    return _prompt_default(question, retrieved_context)
