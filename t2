import streamlit as st
import pandas as pd
import os

# =========================
# تنظیمات صفحه
# =========================
st.set_page_config(
    page_title="فرم رسمی اطلاعات و عکس",
    page_icon="📝",
    layout="wide"
)

SAVE_DIR = "uploaded_photos"
DATA_FILE = "final_friends_data.csv"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


# =========================
# رمز پنل مدیریت
# =========================
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except Exception:
    ADMIN_PASSWORD = "1234"   # فقط برای تست؛ در نسخه آنلاین حتماً Secret تنظیم کنید.


# =========================
# توابع
# =========================
def load_data():
    if os.path.isfile(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE, encoding="utf-8-sig")
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()


def admin_panel():
    st.title("🔐 پنل مدیریت")
    st.write("مدیریت اطلاعات ثبت‌شده محصلان")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        password = st.text_input(
            "رمز عبور مدیر:",
            type="password"
        )

        if st.button("🔓 ورود به پنل"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ رمز عبور نادرست است.")
        return

    # -------------------------
    # دکمه خروج
    # -------------------------
    if st.button("🚪 خروج از پنل"):
        st.session_state.admin_logged_in = False
        st.rerun()

    df = load_data()

    if df.empty:
        st.info("هنوز هیچ اطلاعاتی ثبت نشده است.")
        return

    # -------------------------
    # آمار
    # -------------------------
    st.subheader("📊 آمار ثبت‌نام")

    col1, col2 = st.columns(2)
    col1.metric("تعداد محصلان ثبت‌شده", len(df))
    col2.metric("تعداد عکس‌ها", df["نام فایل عکس"].notna().sum())

    st.divider()

    # -------------------------
    # جستجو
    # -------------------------
    st.subheader("🔎 جستجوی محصل")

    search_text = st.text_input(
        "نام، نام پدر یا شماره تذکره را وارد کنید:"
    )

    filtered_df = df.copy()

    if search_text.strip():
        mask = (
            filtered_df.astype(str)
            .apply(
                lambda column: column.str.contains(
                    search_text,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        )
        filtered_df = filtered_df[mask]

    st.write(f"تعداد نتایج: **{len(filtered_df)}**")

    # -------------------------
    # نمایش جدول
    # -------------------------
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------
    # دانلود Excel/CSV
    # -------------------------
    st.subheader("📥 دریافت اطلاعات")

    csv_data = filtered_df.to_csv(
        index=False,
        encoding="utf-8-sig"
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ دانلود اطلاعات به صورت CSV",
        data=csv_data,
        file_name="students_data.csv",
        mime="text/csv"
    )

    # -------------------------
    # نمایش عکس و مشخصات
    # -------------------------
    st.subheader("👤 مشاهده مشخصات و عکس")

    if len(filtered_df) > 0:
        selected_index = st.selectbox(
            "یک محصل را انتخاب کنید:",
            options=filtered_df.index,
            format_func=lambda i: (
                f"{filtered_df.loc[i, 'نام فارسی']} | "
                f"{filtered_df.loc[i, 'شماره تذکره']}"
            )
        )

        student = filtered_df.loc[selected_index]

        col1, col2 = st.columns([1, 2])

        with col1:
            photo_name = str(student.get("نام فایل عکس", ""))

            if photo_name and photo_name != "nan":
                photo_path = os.path.join(SAVE_DIR, photo_name)

                if os.path.isfile(photo_path):
                    st.image(
                        photo_path,
                        caption=student.get("نام فارسی", "عکس"),
                        width=220
                    )
                else:
                    st.warning("عکس این محصل در پوشه موجود نیست.")
            else:
                st.info("برای این محصل عکس ثبت نشده است.")

        with col2:
            st.write("### مشخصات محصل")

            for column in filtered_df.columns:
                value = student[column]
                st.write(f"**{column}:** {value}")


# =========================
# انتخاب بخش برنامه
# =========================
st.sidebar.title("📋 منوی برنامه")

page = st.sidebar.radio(
    "انتخاب بخش:",
    ["📝 فرم ثبت اطلاعات", "🔐 پنل مدیریت"]
)

# =========================================================
# فرم ثبت اطلاعات
# =========================================================
if page == "📝 فرم ثبت اطلاعات":

    st.title("📝 فرم جمع‌آوری مشخصات و عکس پرسنلی")
    st.subheader("موسسه تحصیلات عالی عاطفی")

    st.error(
        "⚠️ **توجه بسیار مهم:** لطفاً تمامی مشخصات خود را کاملاً دقیق "
        "وارد کرده و عکس پرسنلی باکیفیت و اداری آپلود نمایید."
    )

    st.write("---")

    st.subheader("🔹 مشخصات به زبان فارسی / دری")

    name_fa = st.text_input("نام و نام خانوادگی (فارسی):")
    father_name_fa = st.text_input("نام پدر (فارسی):")

    st.subheader("🔹 مشخصات به زبان انگلیسی")

    name_en = st.text_input("Full Name (English):")
    father_name_en = st.text_input("Father's Name (English):")

    st.subheader("🔹 شماره سند و سال فراغت")

    id_number = st.text_input("شماره تذکره / شناسنامه / پاسپورت:")
    graduation_year = st.text_input("سال دقیق فراغت:")

    st.subheader("📸 عکس پرسنلی اداری")

    uploaded_file = st.file_uploader(
        "لطفاً عکس پرسنلی خود را انتخاب کنید (JPG یا PNG):",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        st.image(
            uploaded_file,
            caption="پیش‌نمایش عکس شما",
            width=150
        )

    agree = st.checkbox(
        "تایید می‌کنم که اطلاعات و عکس فوق کاملاً درست "
        "و مطابق با اسناد رسمی من است."
    )

    if st.button("🚀 ارسال و ثبت نهایی"):

        if not agree:
            st.warning("لطفاً ابتدا تیک تایید صحت اطلاعات را بزنید.")

        elif (
            name_fa
            and father_name_fa
            and name_en
            and father_name_en
            and id_number
            and graduation_year
            and uploaded_file
        ):

            try:
                # -------------------------
                # ذخیره عکس
                # -------------------------
                file_extension = os.path.splitext(
                    uploaded_file.name
                )[1].lower()

                unique_photo_name = (
                    f"{id_number}{file_extension}"
                )

                full_photo_path = os.path.join(
                    SAVE_DIR,
                    unique_photo_name
                )

                with open(full_photo_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # -------------------------
                # ذخیره اطلاعات
                # -------------------------
                new_data = {
                    "نام فارسی": [name_fa],
                    "نام پدر فارسی": [father_name_fa],
                    "نام انگلیسی": [name_en],
                    "نام پدر انگلیسی": [father_name_en],
                    "شماره تذکره": [id_number],
                    "سال فراغت": [graduation_year],
                    "نام فایل عکس": [unique_photo_name]
                }

                df_new = pd.DataFrame(new_data)

                if not os.path.isfile(DATA_FILE):
                    df_new.to_csv(
                        DATA_FILE,
                        index=False,
                        encoding="utf-8-sig"
                    )
                else:
                    df_new.to_csv(
                        DATA_FILE,
                        mode="a",
                        header=False,
                        index=False,
                        encoding="utf-8-sig"
                    )

                st.success(
                    "🎉 مشخصات شما با موفقیت ثبت شد! "
                    "از همکاری شما سپاسگزاریم."
                )

            except Exception as e:
                st.error(f"خطا در ثبت داخلی: {e}")

        else:
            st.error(
                "❌ لطفاً تمام فیلدها را پر کنید "
                "و عکس خود را آپلود نمایید."
            )

# =========================================================
# پنل مدیریت
# =========================================================
else:
    admin_panel()
