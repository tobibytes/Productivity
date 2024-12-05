require('dotenv').config();
const express = require('express')
const cors = require('cors')


const app = express()

app.use(cors())
app.use(express.json())


app.get('/', async (req, res) => {
    res.send(`Hello This is Github Service on port ${process.env.PORT}`)
})




app.listen(process.env.PORT, "0.0.0.0", () => {
    console.log(`Server is running on port ${process.env.PORT}`)
})