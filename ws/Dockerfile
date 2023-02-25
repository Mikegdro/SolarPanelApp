FROM node:16.15.1-alpine
WORKDIR /app
COPY package*.json .
RUN npm install
COPY ./build/server.js ./server.js
COPY ./.env ./.env
COPY ./logs.json ./logs.json
CMD ["node", "server.js"]
EXPOSE 3000