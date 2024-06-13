import express from "express";
import redis from "redis";
import { promisify } from "util";
import kue from "kue";

const app = express();
const client = redis.createClient();
const queue = kue.createQueue();

client.on("connect", () => {
  console.log("Connected to Redis");
});

const reserveSeat = (number) => {
  client.set("available_seats", number);
};

const getCurrentAvailableSeats = promisify(client.get).bind(client);

// Initialize the number of available seats and reservation status
reserveSeat(50);
let reservationEnabled = true;

app.get("/available_seats", async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats(
    "available_seats"
  );
  res.json({ numberOfAvailableSeats });
});

app.get("/reserve_seat", (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: "Reservation are blocked" });
  } else {
    const job = queue.create("reserve_seat").save((err) => {
      if (err) {
        res.json({ status: "Reservation failed" });
      } else {
        res.json({ status: "Reservation in process" });
      }
    });
  }
});

app.get("/process", async (req, res) => {
  res.json({ status: "Queue processing" });

  queue.process("reserve_seat", async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats("available_seats");
    const availableSeats = parseInt(currentSeats) || 0;
    if (availableSeats === 0) {
      reservationEnabled = false;
      done(new Error("Not enough seats available"));
    } else {
      reserveSeat(availableSeats - 1);
      if (availableSeats - 1 === 0) {
        reservationEnabled = false;
      }
      done();
    }
  });
});

queue.on("job complete", (id) => {
  console.log(`Seat reservation job ${id} completed`);
});

queue.on("job failed", (id, err) => {
  console.log(`Seat reservation job ${id} failed: ${err.message}`);
});

app.listen(1245, () => {
  console.log("Server running on port 1245");
});
