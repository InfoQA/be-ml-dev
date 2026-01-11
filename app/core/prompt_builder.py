def build_prompt(context: dict, user_question: str) -> str:
    menu = context.get("menu")
    semester = context.get("semester")

    if menu == "Kurikulum dan Mata Kuliah":
        return _prompt_kurikulum(semester, user_question)

    if menu == "MBKM":
        return _prompt_mbkm(user_question)

    if menu == "Informasi Umum":
        return _prompt_informasi_umum(user_question)

    # fallback (jika konteks tidak lengkap)
    return _prompt_default(user_question)


# ==============================
# PROMPT PER MENU
# ==============================

def _prompt_kurikulum(semester: str, question: str) -> str:
    return f"""
Konteks:
- Topik       : Mata Kuliah
- Semester    : {semester}

Tugas kamu adalah menjawab pertanyaan seputar:
- mata kuliah pada semester tersebut
- prasyarat mata kuliah
- bobot SKS
- deskripsi singkat mata kuliah

Pertanyaan pengguna:
{question}
""".strip()


def _prompt_mbkm(question: str) -> str:
    return f"""
Topik:
- Merdeka Belajar Kampus Merdeka (MBKM)

Tugas kamu adalah menjawab pertanyaan terkait:
- jenis program MBKM
- konversi SKS
- syarat dan ketentuan

Pertanyaan pengguna:
{question}
""".strip()


def _prompt_informasi_umum(question: str) -> str:
    return f"""
Topik:
- Informasi Umum Program Studi

Tugas kamu adalah memberikan informasi terkait:
- visi dan misi program studi
- profil lulusan
- dosen dan fasilitas

Pertanyaan pengguna:
{question}
""".strip()


def _prompt_default(question: str) -> str:
    return f"""
Pertanyaan pengguna:
{question}
""".strip()
