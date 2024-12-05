require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { default: axios } = require('axios');
const { processCoursesForDb, saveCoursesToDb, MYCOURSES, processAnnouncementsForKafka } = require('./services/utils');
const getRedis = require('./services/models/redis');
const { initKafka  } = require('./services/models/kafka')
const { producer, consumer} = initKafka()
const startKafka = async (retries = 5, delay = 15000) => {
  while (retries > 0) {
    try {
      await producer.connect();
      // await consumer.connect();
      // await consumer.subscribe({ topic: 'analyze-message', fromBeginning: true });
      console.log('Kafka connected successfully');
      return;
    } catch (error) {
      console.error(`Error connecting to Kafka, retries left: ${retries - 1}`, error);
      retries -= 1;
      if (retries === 0) throw error;
      await new Promise(res => setTimeout(res, delay));
    }
  }
};
const app = express();

app.use(cors());
app.use(express.json());


async function sendMessage({ topic, content }) {
  try {
    await producer.send({
      topic: topic,
      messages: [{ value: JSON.stringify({serviceName: 'Canvas',content}) }],
    });
    console.log('Message sent successfully!');
  } catch (error) {
    console.error('Error sending message:', error);
  }
}

app.get('/', async (req, res) => {
  res.send(`Hello! This is the Canvas Service on port ${process.env.PORT}`);
});

app.get('/courses/', async (req, res) => {
  try {
    const page = req.query.page || 1;
    const result = await axios.get(`https://canvas.instructure.com/api/v1/courses?page=${page}`, {
      headers: { Authorization: `Bearer ${process.env.CANVAS_ACCESS_TOKEN}` },
    });
    const data = result.data;
    await saveCoursesToDb(processCoursesForDb(data));
    res.send({ successful: true });
  } catch (err) {
    console.error(`Error getting courses: ${err}`);
    res.status(500).send({ error: 'Error getting courses' });
  }
});

app.get('/announcements/', async (req, res) => {
  try {
    const q = MYCOURSES.map((course) => `context_codes[]=course_${course}`).join('&');
    const redisClient = await getRedis();

    const start_date = (await redisClient.get('canvas_last_announcement_date')) || new Date().toISOString()
    const new_start_date = new Date().toISOString();
    
    const result = await axios.get(`https://canvas.instructure.com/api/v1/announcements?start_date=${start_date}&${q}`, {
      headers: { Authorization: `Bearer ${process.env.CANVAS_ACCESS_TOKEN}` },
    });

    const data = result.data;
    if (data.length > 0) {
      await redisClient.set('canvas_last_announcement_date', new_start_date);
      const processedData = processAnnouncementsForKafka(data);
      await sendMessage({ topic: 'analyze-message', content: processedData });
      return res.send(JSON.parse(processedData) );
    }
    
    await redisClient.set('canvas_last_announcement_date', new_start_date);
    res.send({ message: 'No new announcements', date: new Date().toISOString() });
  } catch (err) {
    console.error(`Error getting announcements: ${err}`);
    res.status(500).send({ error: 'Error getting announcements' });
  }
});

const start = async () => {
  try {

    await startKafka()
    app.listen(process.env.PORT, () => {
      console.log(`Server running at http://localhost:${process.env.PORT}`);
    });
  } catch (error) {
    console.error('Error starting server or connecting producer:', error);
  }
};


start();