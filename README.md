# 🍽️ Order Manager

**Order Manager** es una aplicación diseñada para la gestión eficiente de comandas en comedores, cafeterías y restaurantes. Permite gestionar reservas, visualizar la disposición de mesas, tomar pedidos y registrar ventas de manera organizada y efectiva.

## 🚀 Características  
- 🛎 **Gestor de reservas:** Permite reservar mesas y verificar disponibilidad en tiempo real.  
- 🗺 **Vista de mesas:** Muestra la disposición real de las mesas y su estado actual.  
- 📝 **Registro de pedidos:** Facilita la toma de órdenes de los clientes.  
- 💰 **Control de ventas:** Registra y gestiona las ventas realizadas.  

## 🛠 Tecnologías  
- **Lenguaje:** Python  
- **Interfaz Gráfica:** PyQt5  
- **Base de datos:** SQLite  

## 📂 Instalación y Uso  

### 🔧 Requisitos previos  
- Tener Python 3.x instalado.  
- Instalar las dependencias necesarias: PyQt5, Flask y SQLite.  

### 🔽 Instalación  
1. Clona el repositorio:  
   ```bash
   git clone https://github.com/enzo2805/order_manager.git
   ```
2. Ingresa a la carpeta del proyecto:  
   ```bash
   cd order_manager
   ```
3. Instala las dependencias necesarias:  
   ```bash
   pip install PyQt5
   pip install Flask

   ```
4. [Crea e inicializa la base de datos](#-inicialización-de-la-base-de-datos)

5. Ejecuta la aplicación:  
   ```bash
   python app.py #Api
   python main.py #Principal
   python cocina.py #Comandas para la cocina
   ```

## 🗄️ Inicialización de la base de datos

Antes de ejecutar la aplicación por primera vez, debes crear la base de datos y las tablas necesarias.

1. **Crea las tablas principales ejecutando:**
   ```bash
   python db.py
   ```
   Esto generará el archivo `comedor.db` con todas las tablas requeridas para el sistema.

2. **(Opcional) Inicializa las mesas con datos de ejemplo:**
   ```bash
   python script.py
   ```
   Este script agrega 10 mesas en estado "Libre" para que puedas comenzar a probar la aplicación de inmediato.

## 🌟 Contribuciones  
¡Las contribuciones son bienvenidas! Si quieres mejorar **Order Manager**, sigue estos pasos:  
1. Haz un fork del repositorio.  
2. Crea una nueva rama:  
   ```bash
   git checkout -b feature/nueva-mejora
   ```
3. Realiza cambios y haz commit:  
   ```bash
   git commit -m "Agregada nueva funcionalidad X"
   ```
4. Sube los cambios:  
   ```bash
   git push origin feature/nueva-mejora
   ```
5. Abre un Pull Request.  

## 📜 Licencia  
Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

