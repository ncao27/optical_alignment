import serial
import time
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
print([port.device for port in ports])


# create the connection between the device and my computer

ser = serial.Serial(port = "COM3",
                    bytesize = serial.EIGHTBITS,
                    baudrate = 115200,
                    parity = serial.PARITY_NONE,
                    stopbits = 1,
                    timeout = 1,
                    xonxoff = False,
                    rtscts = False,
                    dsrdtr = False
                    )
'''
# Try a basic command to check connectivity
try:
    ser.write(b'NR10000000A\r\n')
    time.sleep(5)
    ser.write(b'S\r\n')
    response = ser.read(100)
    print("Response:", response)
except Exception as e:
    print("Error:", e)
finally:
    ser.close()
'''
try:
    # Ask user for input
    print("\nEnter command parameters:")
    dir = input("Direction (e.g., 'NR' for Clockwise, 'PR' for Anti-clockwise): ").strip()
    freq = input("Frequency (ranges from 1 - 1500): ").strip()
    pulse = input("Pulse width (ranges from 0000 to 9999 pulses): ").strip()
    axis = input("Axis (A corresponds to Axis 1, B corresponds to Axis 2, etc.): ").strip().upper()

    command_str = f'{dir}{freq}{pulse}{axis}\r\n'

    # check for connectivity first
    ser.write(b'CON\r\n')
    print("Is the connection okay? ", ser.read(100))

    # send the command after
    if pulse == '0000':
        ser.write(command_str.encode('ascii'))
        time.sleep(5)
        ser.write(b'S\r\n')
    else:
        ser.write(command_str.encode('ascii'))

    # Wait and read response
    time.sleep(0.1)
    response = ser.read_all()
    print("Device response:", repr(response))

except Exception as e:
    print("Error:", e)

finally:
    ser.close()

# Read the response
#response = ser.read(100)
#print("📡 Device response:", response.decode(errors='replace').strip())


