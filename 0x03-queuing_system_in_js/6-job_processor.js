import kue from "kue";

// Create a queue
const queue = kue.createQueue();

// Function to send notifications
function sendNotification(phoneNumber, message) {
  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`
  );
}

// Process jobs in the queue
queue.process("push_notification_code", (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message);
  // Call done when the job is completed
  done();
});

// Log when the queue is ready
queue.on("ready", () => {
  console.log("Queue is ready!");
});

// Log when the queue encounters an error
queue.on("error", (err) => {
  console.error("Queue error:", err);
});
