import streamlit as st
import pandas as pd
import os

# تنظیمات صفحه
st.set_page_config(page_title="فرم رسمی اطلاعات و عکس", page_icon="📝")
st.title("📝 فرم جمع‌آوری مشخصات و عکس پرسنلی")
st.subheader("موسسه تحصیلات عالی عاطفی")
st.error("⚠️ **توجه بسیار مهم:** لطفاً تمامی مشخصات خود را کاملاً دقیق وارد کرده و عکس پرسنلی باکیفیت و اداری آپلود نمایید.")

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
uploaded_file = st.file_uploader("لطفاً عکس پرسنلی خود را انتخاب کنید (JPG یا PNG):", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="پیش‌نمایش عکس شما", width=150)

agree = st.checkbox("تایید می‌کنم که اطلاعات و عکس فوق کاملاً درست و مطابق با اسناد رسمی من است.")

# ساخت پوشه برای عکس‌ها
SAVE_DIR = "uploaded_photos"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

file_name = "final_friends_data.csv"

if st.button("🚀 ارسال و ثبت نهایی"):
    if not agree:
        st.warning("لطفاً ابتدا تیک تایید صحت اطلاعات را بزنید.")
    elif name_fa and father_name_fa and name_en and father_name_en and id_number and graduation_year and uploaded_file:
        try:
            # ۱. ذخیره عکس
            file_extension = os.path.splitext(uploaded_file.name).lower()
            unique_photo_name = f"{id_number}{file_extension}"
            full_photo_path = os.path.join(SAVE_DIR, unique_photo_name)
            
            with open(full_photo_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # ۲. ذخیره اطلاعات متنی در فایل CSV
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
            
            if not os.path.isfile(file_name):
                df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
            else:
                df_new.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')
                
            st.success("🎉 مشخصات شما با موفقیت ثبت شد! از همکاری شما سپاسگزاریم.")
        except Exception as e:
            st.error(f"خطا در ثبت داخلی: {e}")
    else:
        st.error("❌ لطفاً تمام فیلدها را پر کنید و عکس خود را آپلود نمایید.")

# 🔹 دکمه دانلود مستقیم فایل اکسل در پایین صفحه (بدون پنل پیچیده)
st.write("---")
if os.path.exists(file_name):
    df_download = pd.read_csv(file_name)
    csv_data = df_download.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button(
        label="📥 دانلود فایل اکسل مشخصات (CSV)",
        data=csv_data,
        file_name="friends_data_export.csv",
        mime="text/csv"
    )
