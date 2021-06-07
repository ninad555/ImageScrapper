import streamlit as st
from scrapper import search_and_download


def main():
    st.title("Image Scrapper")
    search_word = st.text_input("Search Image")
    count = st.text_input("Number of Images")

    if not st.button("Download"):
        pass
    else:
        search_and_download(search_term=search_word, number_images=int(count))
        st.success("Your images are downloaded in your local folder")
    if st.button("App info"):
        st.text("This app is built with Streamlit")
    if st.button("About"):
        add_link = "[Github link](https://github.com/ninad555/)"
        linkedin = "[Linked in](https://www.linkedin.com/in/ninad-kadam-4439081b0/)"
        st.markdown(add_link)
        st.markdown(linkedin)


if __name__ == "__main__":
    main()