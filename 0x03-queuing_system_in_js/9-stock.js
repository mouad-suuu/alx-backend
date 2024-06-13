import express from "express";
import redis from "redis";
import { promisify } from "util";

const app = express();
const client = redis.createClient();

client.on("connect", () => {
  console.log("Connected to Redis");
});

const listProducts = [
  {
    itemId: 1,
    itemName: "Suitcase 250",
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: "Suitcase 450",
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: "Suitcase 650",
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: "Suitcase 1050",
    price: 550,
    initialAvailableQuantity: 5,
  },
];

const getItemById = (id) =>
  listProducts.find((product) => product.itemId === id);

const reserveStockById = (itemId, stock) => {
  client.set(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = promisify(client.get).bind(client);

app.get("/list_products", (req, res) => {
  res.json(listProducts);
});

app.get("/list_products/:itemId", async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: "Product not found" });
  } else {
    const currentQuantity = await getCurrentReservedStockById(`item.${itemId}`);
    res.json({ ...product, currentQuantity: parseInt(currentQuantity) || 0 });
  }
});

app.get("/reserve_product/:itemId", async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: "Product not found" });
  } else {
    const currentQuantity = await getCurrentReservedStockById(`item.${itemId}`);
    const currentStock = parseInt(currentQuantity) || 0;
    if (currentStock <= 0) {
      res.json({ status: "Not enough stock available", itemId });
    } else {
      reserveStockById(itemId, currentStock - 1);
      res.json({ status: "Reservation confirmed", itemId });
    }
  }
});

app.listen(1245, () => {
  console.log("Server running on port 1245");
});
