# with open("WeatherStation_Firmware.bin", 'rb') as infile, open("WeatherStation_Firmware.hex", 'w') as outfile:
#     hex_data = infile.read().hex()
#     outfile.write(hex_data)
# with open("WeatherStation_Firmware.hex", 'r') as infile, open("Restored_Firmware.bin", 'wb') as outfile:
#     hex_data = infile.read().strip()
#     binary_data = bytes.fromhex(hex_data)
#     outfile.write(binary_data)

with open("WeatherStation_Firmware.bin", 'rb') as file:
    print(file.read().__len__())
    file.close()

with open("WeatherStation_Firmware.bin", 'rb') as file:
    print(file.read().hex().__len__())
    file.close()    
# print("\n")
# print("\n")

# with open("Restored_Firmware.bin", 'rb') as file:
#     print(file.readline())