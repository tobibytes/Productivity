const express = require('express');
const cors = require('cors');
require('dotenv').config();
const getRedis = require('./services/redis');
const { Analyze } = require('./services/gptService');
const { initKafka } = require('./services/kafka');
const {producer, consumer} = initKafka()

async function startKafka(retries = 5, delay = 10000) {
    while (retries > 0) {
        try {
            // await producer.connect();
            await consumer.connect();
            await consumer.subscribe({ topic: 'analyze-message', fromBeginning: true });
            console.log('Kafka connected successfully');
        return;
    } catch (error) {
      console.error(`Error connecting to Kafka, retries left: ${retries - 1}`, error);
      retries -= 1;
      if (retries === 0) throw error;
      await new Promise(res => setTimeout(res, delay));
    }
}
}
const app = express();

app.use(cors());
app.use(express.json());


async function consumerListen() {
    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            const parsedMessage = JSON.parse(message.value.toString());
            const { serviceName, content } = parsedMessage;
            
            if (topic === 'analyze-message'){
                
                await Analyze({ serviceName, content });
            }
        },
    });
}

app.get('/', async (req, res) => {
    const redisClient = await getRedis()
    res.send({last: redisClient.get('gpt_last_analysis')});
});

const start = async () => {
        try {
            await startKafka()
            
            app.listen(process.env.PORT, '0.0.0.0', () => {
                console.log(`Server running at http://localhost:${process.env.PORT}`);
            });
            await consumerListen();
        } catch (error) {
            console.error("Error starting service:", error);
        }
    };
    

start();

// module.exports = { consumer};