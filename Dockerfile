# Usa una imagen base de Node.js
FROM node:18-alpine

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios para instalar las dependencias
COPY package.json package-lock.json ./

# Instala las dependencias
RUN npm install

# Copia todo el código de tu frontend al contenedor
COPY . .

# Construye la aplicación
RUN npm run build

# Exposición del puerto 3000
EXPOSE 3000

# Comando para iniciar el servidor
CMD ["npm", "start"]
