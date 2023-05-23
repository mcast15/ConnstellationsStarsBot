

import pandas as pd
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import os
plt.style.use("dark_background")

class Graficos:
    def __init__(self):
        self.estrellas = None
        self.dataframes_constelaciones = None
        
    def cargar_datos(self):
        path = "C:\\Users\\mcast\\OneDrive\\Escritorio\\TelescopeBot\\constellations\\stars.txt"
        archivo = open(path, 'r')  # Abre el archivo en modo de lectura
        lineas = archivo.readlines()  # Lee todas las líneas del archivo y las guarda en una lista
        archivo.close()  # Cierra el archivo

        data = []
        for linea in lineas:
            valores = linea.split()  # Divide la línea en una lista de valores separados por espacios
            valor1 = float(valores[0])
            valor2 = float(valores[1])
            valor3 = float(valores[2])
            valor4 = int(valores[3])
            valor5 = float(valores[4])
            valor6 = int(valores[5])
            nombre = ""
            segundo_nombre = ""
            if len(valores) > 6:
                nombres = " ".join(valores[6:]).split(";")
                nombre = nombres[0]
                if len(nombres) > 1:
                    segundo_nombre = nombres[1]
            data.append([valor1, valor2, valor3, valor4, valor5, valor6, nombre, segundo_nombre])

        columnas = ['Coordenada X', 'Coordenada Y', 'Coordenada Z', 'ID', 'Magnitud', 'Harvard Revised', 'Nombre', 'Segundo Nombre']
        self.estrellas = pd.DataFrame(data, columns=columnas)
        self.estrellas["Segundo Nombre"] = self.estrellas["Segundo Nombre"].str.strip()

        CONSTELLATIONS = "C:\\Users\\mcast\\OneDrive\\Escritorio\\TelescopeBot\\constellations"
        archivos_constelaciones = os.listdir(CONSTELLATIONS)[:8]
        self.dataframes_constelaciones = []

        for archivo in archivos_constelaciones:
            ruta_archivo = os.path.join(CONSTELLATIONS, archivo)

            with open(ruta_archivo, 'r') as f:
                lineas = f.readlines()

            conexiones = [linea.strip().split(',') for linea in lineas]
            df_constelacion = pd.DataFrame(conexiones, columns=['Estrella 1', 'Estrella 2'])
            self.dataframes_constelaciones.append(df_constelacion)
        
    def graficar_estrellas(self):
        plt.figure(figsize=(10, 10))
        plt.scatter(self.estrellas["Coordenada X"], self.estrellas["Coordenada Y"], marker="*", s= 25)
        plt.xticks([])
        plt.yticks([])
        file_path = 'zestrellas_plot.png'
        plt.savefig(file_path, facecolor='black', bbox_inches='tight', pad_inches=0)
        return file_path
    

    def graficar_constelacion(self, indice_constelacion):
        plt.figure(figsize=(10, 10))
        plt.scatter(self.estrellas["Coordenada X"], self.estrellas["Coordenada Y"], marker="*", s=25)
        plt.xticks([])
        plt.yticks([])

        colores_constelaciones = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFA500', '#800080']
        nombres_constelaciones = ['Boyero', 'Casiopea', 'Cazo', 'Cygnet', 'Geminis', 'Hydra', 'OsaMayor', 'OsaMenor']

        df_constelacion = self.dataframes_constelaciones[indice_constelacion]
        color = colores_constelaciones[indice_constelacion]
        nombre_constelacion = nombres_constelaciones[indice_constelacion]

        for _, row in df_constelacion.iterrows():
            estrella1 = row["Estrella 1"]
            estrella2 = row["Estrella 2"]

            if (estrella1 in self.estrellas["Nombre"].values or estrella1 in self.estrellas["Segundo Nombre"].values) and \
               (estrella2 in self.estrellas["Nombre"].values or estrella2 in self.estrellas["Segundo Nombre"].values):

                x1 = self.estrellas.loc[(self.estrellas["Nombre"] == estrella1) | (self.estrellas["Segundo Nombre"] == estrella1), "Coordenada X"].values[0]
                y1 = self.estrellas.loc[(self.estrellas["Nombre"] == estrella1) | (self.estrellas["Segundo Nombre"] == estrella1), "Coordenada Y"].values[0]
                x2 = self.estrellas.loc[(self.estrellas["Nombre"] == estrella2) | (self.estrellas["Segundo Nombre"] == estrella2), "Coordenada X"].values[0]
                y2 = self.estrellas.loc[(self.estrellas["Nombre"] == estrella2) | (self.estrellas["Segundo Nombre"] == estrella2), "Coordenada Y"].values[0]

                plt.plot([x1, x2], [y1, y2], color=color, linewidth=1)

        plt.text(0.05, 0.95, nombre_constelacion, transform=plt.gca().transAxes, fontsize=12)
        file_path = 'zconstelacion_plot.png'
        plt.savefig(file_path, facecolor='black', bbox_inches='tight', pad_inches=0)
        return file_path

    def graficar_todas(self):
        plt.figure(figsize=(10, 10))
        plt.scatter(self.estrellas["Coordenada X"], self.estrellas["Coordenada Y"], marker="*", s= 25)
        plt.xticks([])
        plt.yticks([])

        colores_constelaciones = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFA500', '#800080']
        nombres_constelaciones = ['Boyero', 'Casiopea', 'Cazo', 'Cygnet', 'Geminis', 'Hydra', 'OsaMayor', 'OsaMenor']
        legend_lines = [Line2D([0], [0], color=color, lw=2) for color in colores_constelaciones]

        for i, df_constelacion in enumerate(self.dataframes_constelaciones):
            color = colores_constelaciones[i % len(colores_constelaciones)]
            nombre_constelacion = nombres_constelaciones[i % len(nombres_constelaciones)]

            for _, row in df_constelacion.iterrows():
                estrella1 = row["Estrella 1"]
                estrella2 = row["Estrella 2"]

                if (estrella1 in self.estrellas["Nombre"].values or estrella1 in self.estrellas["Segundo Nombre"].values) and \
                   (estrella2 in self.estrellas["Nombre"].values or estrella2 in self.estrellas["Segundo Nombre"].values):

                    x1 = self.estrellas.loc[(self.estrellas["Nombre"] == estrella1) | (self.estrellas["Segundo Nombre"] == estrella1), "Coordenada X"].values[0]
                    y1 = self.estrellas.loc[(self.estrellas["Nombre"] == estrella1) | (self.estrellas["Segundo Nombre"] == estrella1), "Coordenada Y"].values[0]
                    x2 = self.estrellas.loc[(self.estrellas["Nombre"] == estrella2) | (self.estrellas["Segundo Nombre"] == estrella2), "Coordenada X"].values[0]
                    y2 = self.estrellas.loc[(self.estrellas["Nombre"] == estrella2) | (self.estrellas["Segundo Nombre"] == estrella2), "Coordenada Y"].values[0]

                    plt.plot([x1, x2], [y1, y2], color=color, linewidth=1)

        plt.legend(legend_lines, nombres_constelaciones, facecolor='white', edgecolor='black')
        file_path = 'zconstelaciones.png'
        plt.savefig(file_path, facecolor='black', bbox_inches='tight', pad_inches=0)
        return file_path

"""# Bot"""



import telebot

# Crea una instancia del bot de Telegram
bot = telebot.TeleBot('6291288198:AAFMJoL4VKWKUz8dOey6YReCsHeBzbTuS8A')

# Crea una instancia de la clase Graficos
graficos = Graficos()

# Carga los datos al iniciar el bot
graficos.cargar_datos()

# Maneja el comando /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "¡Hola! Soy un bot de gráficos de constelaciones. Elige una opción:\n\n"
                          "1. /graficar_todas - Graficar todas las constelaciones.\n"
                          "2. /graficar_estrellas - Graficar todas las estrellas.\n"
                          "3. /graficar_constelacion - Graficar una constelación específica.")

# Maneja el comando /graficar_todas
@bot.message_handler(commands=['graficar_todas'])
def handle_graficar_todas(message):
    file_path = graficos.graficar_todas()
    with open(file_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)   

# Maneja el comando /graficar_estrellas
@bot.message_handler(commands=['graficar_estrellas'])
def handle_graficar_estrellas(message):
    file_path = graficos.graficar_estrellas()
    with open(file_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
        
# Maneja el comando /graficar_constelacion
@bot.message_handler(commands=['graficar_constelacion'])
def handle_graficar_constelacion(message):
    bot.reply_to(message, "Por favor, ingresa un índice del 0 al 7: \n0. Boyero\n1. Casiopea\n2. Cazo\n3. Cygnet\n4. Geminis\n5. Hydra\n6. Osa Mayor\n7. Osa Menor")
    bot.register_next_step_handler(message, handle_constelacion_index)

def handle_constelacion_index(message):
    try:
        index = int(message.text)
        if 0 <= index <= 7:
            file_path = graficos.graficar_constelacion(index)
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.reply_to(message, "Por favor, ingresa un valor válido del 0 al 7.")
    except ValueError:
        bot.reply_to(message, "El índice ingresado no es válido. Por favor, intenta nuevamente.")

        

# Ejecuta el bot
bot.polling()

