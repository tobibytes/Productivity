const {createClient} = require('redis');

async function configureRedis() {
  const client = createClient({
      url: 'redis://redis:6379'
    })
    client.on('error', err => console.log('Redis Client Error', err))
    await client.connect()
    return client
}

module.exports = configureRedis;