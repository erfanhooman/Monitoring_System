FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --frozen-lockfile --verbose

COPY . .

RUN npm run build

RUN npm install -g serve

EXPOSE 5000

CMD ["serve", "-s", "build", "-l", "5000"]