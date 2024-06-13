import kue from "kue";

// Create a queue
const queue = kue.createQueue();

// Create a job data object
const jobData = {
  phoneNumber: "1234567890",
  message: "Hello, this is a notification!",
};

// Create a job in the queue
const job = queue.create("push_notification_code", jobData);

// Log when the job is created
job.on("enqueue", () => {
  console.log(`Notification job created: ${job.id}`);
});

// Log when the job is completed
job.on("complete", () => {
  console.log("Notification job completed");
});

// Log when the job fails
job.on("failed", () => {
  console.log("Notification job failed");
});

// Save the job to the queue
job.save((err) => {
  if (err) {
    console.error(err);
  }
  // Nothing else will happen here, as processing the job is a separate task
  // To process the job, you need to set up a worker - see the next task
});
