import express from "express";
import client from "prom-client";

const app = express();
const register = new client.Registry();

// Додаємо стандартні метрики системи (CPU, пам’ять, uptime тощо)
client.collectDefaultMetrics({ register });

// Ендпоінт для метрик
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

// Простий health-check, що сервер працює
app.get("/", (req, res) => {
  res.status(200).send("Frontend metrics service is up");
});


app.listen(3001, () => {
  console.log("✅ Frontend metrics server running on port 3001");
});
