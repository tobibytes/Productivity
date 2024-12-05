const { default: axios } = require('axios');
var cron = require('node-cron');

var task = cron.schedule('*/30 * * * *', async () =>  {
    const res = await axios.get('http://localhost:5005/announcements/')
    const data = await res.data
  console.log(data);
});

task.start()