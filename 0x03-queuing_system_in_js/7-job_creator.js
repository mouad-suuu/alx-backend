import kue from "kue";

// Create an array of jobs
const jobs = [
  {
    phoneNumber: "4153518780",
    message: "This is the code 1234 to verify your account",
  },
  {
    phoneNumber: "4153518781",
    message: "This is the code 4562 to verify your account",
  },
  // Add more jobs as needed
];

// Create a queue
const queue = kue.createQueue();

// Process each job in the array
jobs.forEach((jobData, index) => {
  const job = queue.create("push_notification_code_2", jobData).save((err) => {
    if (err) {
      console.error("Failed to create job:", err);
      return;
    }
    console.log(`Notification job created: ${job.id}`);
  });

  job.on("complete", () => {
    console.log(`Notification job ${job.id} completed`);
  });

  job.on("failed", (err) => {
    console.error(`Notification job ${job.id} failed: ${err}`);
  });

  job.on("progress", (progress) => {
    console.log(`Notification job ${job.id} ${progress}% complete`);
  });
});

// Log when the queue is ready
queue.on("ready", () => {
  console.log("Queue is ready!");
});

// Log when the queue encounters an error
queue.on("error", (err) => {
  console.error("Queue error:", err);
});
