import kue from "kue";

// Create an array of blacklisted phone numbers
const blacklistedNumbers = ["4153518780", "4153518781"];

// Create a function to send notifications
function sendNotification(phoneNumber, message, job, done) {
  // Track the progress of the job
  job.progress(0, 100);

  // Check if the phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  // Update progress and log the notification
  job.progress(50, 100);
  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`
  );

  // Job is done
  done();
}

// Create a queue
const queue = kue.createQueue({
  prefix: "q",
  redis: {
    port: 6379,
    host: "127.0.0.1",
  },
});

// Process jobs from the queue
queue.process("push_notification_code_2", 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});

// Log when the queue is ready
queue.on("ready", () => {
  console.log("Queue is ready!");
});

// Log when the queue encounters an error
queue.on("error", (err) => {
  console.error("Queue error:", err);
});
