# Usa la imagen de Node.js
FROM node:18-alpine

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias al contenedor
COPY ./frontend/package.json ./frontend/package-lock.json ./

# Instala las dependencias
RUN npm install

# Copia el resto del código al contenedor
COPY ./frontend .

# Exponer el puerto que usará la app
EXPOSE 3000

# Comando para iniciar la aplicación
CMD ["npm", "start"]
