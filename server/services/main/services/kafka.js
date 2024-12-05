const { Kafka } = require('kafkajs');


function initKafka() {
  const kafka = new Kafka({
    clientId: 'productivity',
    brokers: ['kafka:9092'],
});
const producer = kafka.producer();
const consumer = kafka.consumer({ groupId: 'analyze' });
return { producer, consumer}
}

module.exports = { initKafka };