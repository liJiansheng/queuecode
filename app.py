import streamlit as st
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image
import io
import base64
from urllib.parse import urlparse


# Function to convert image to base64
def get_image_as_base64(image: Image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

def get_url_filename(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    main_domain = domain.split('.')
    main_domain = main_domain[1] if main_domain[0] == 'www' else main_domain[0]
    path = parsed_uri.path.strip('/').replace('/', '_')
    return f"{main_domain}_{path}" if path else main_domain


# QR code content options
qr_content_options = ["URL", "Text"]
# qr_content_options = ["URL", "Text", "Contact Information"]
qr_content_type = st.selectbox("Select QR content type", qr_content_options)


content = st.text_area("Enter your content", height=150)

if st.button("Generate QR Code"):
    if content:
        if content.strip():
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4
            )
            qr.add_data(content)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white", image_factory=PilImage)

            # Convert PilImage to bytes-like object
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_bytes = buffer.getvalue()

            img_base64 = get_image_as_base64(img)

            st.markdown(f"##### {content}")
            st.image(img_bytes, caption=f"QR code for {content}", use_container_width=True)
            file_name = get_url_filename(content)
            st.markdown(f'<a href="data:image/png;base64,{img_base64}" download="{file_name}.png" style="display:inline-block;background-color:#4CAF50;border:none;color:white;padding:8px 16px;text-align:center;text-decoration:none;font-size:16px;margin:4px 2px;cursor:pointer;">Download QR code</a>', unsafe_allow_html=True)
    else:
        st.error("Please enter content for the QR code.")



