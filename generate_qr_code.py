import os
import qrcode

current_directory = os.getcwd()
qr_codes_directory = os.path.join(current_directory, 'qrCodes')


if not os.path.exists(qr_codes_directory):
    os.makedirs(qr_codes_directory)

# settings
common_qr_settings = {
    'version': 10,  
    'error_correction': qrcode.constants.ERROR_CORRECT_H, 
    'box_size': 10,
    'border': 4,
}

host_qr_settings = qrcode.QRCode(**common_qr_settings)
host_data = "https://e-services.uha.fr/fr/index.html zerzerze rze rze zer zer ze rezr ez zer "
host_qr_settings.add_data(host_data)
host_qr = host_qr_settings.make_image(fill_color="black", back_color="white")
host_qr_path = os.path.join(qr_codes_directory, 'host_qr.png')
host_qr.save(host_qr_path)


hidden_qr_settings = qrcode.QRCode(**common_qr_settings)
hidden_data = "Secret Message 5"
hidden_qr_settings.add_data(hidden_data)
hidden_qr = hidden_qr_settings.make_image(fill_color="black", back_color="white")
hidden_qr_path = os.path.join(qr_codes_directory, 'hidden_qr5.png')
hidden_qr.save(hidden_qr_path)


(host_qr_path, hidden_qr_path)
