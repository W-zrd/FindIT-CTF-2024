FROM node:18-alpine

ENV NODE_ENV=production
WORKDIR /app
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install --production

COPY app.js app.js
COPY flag.txt flag.txt

EXPOSE 6060
CMD ["node", "app.js"]