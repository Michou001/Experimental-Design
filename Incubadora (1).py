import serial
import time
import csv

# === CONFIGURACIÓN ===
COM_PORT = 'COM6'      # <- ¡CAMBIA ESTO AL PUERTO DE TU ESP32!
BAUD_RATE = 115200     
FILE_NAME = 'Datos_Corrida1_39_7C.csv' # <- ¡CAMBIA EL NOMBRE EN CADA CORRIDA!
TIEMPO_RECOLECCION = 900  # 900 segundos = 15 minutos

try:
    print(f"Conectando al puerto {COM_PORT}...")
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) 
    
    print(f"¡Conectado! Grabando datos por {TIEMPO_RECOLECCION/60} minutos...")
    print("Presiona Ctrl+C en esta ventana si quieres detenerlo antes.\n")
    
    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        start_time = time.time()
        
        while (time.time() - start_time) < TIEMPO_RECOLECCION:
            if ser.in_waiting > 0:
                linea = ser.readline().decode('utf-8').strip()
                
                if linea and "Error" not in linea:
                    print(linea) 
                    datos = linea.split(',')
                    writer.writerow(datos)
                    file.flush() 
                    
    print(f"\n¡Experimento terminado! Datos guardados en {FILE_NAME}")

except KeyboardInterrupt:
    print(f"\nRecolección detenida por ti. Datos guardados en {FILE_NAME}")
except Exception as e:
    print(f"Hubo un error: {e}. ¿Cerraste el Monitor Serie de Arduino?")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()