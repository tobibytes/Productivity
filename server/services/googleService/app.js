require('dotenv').config();
const express = require('express')
const cors = require('cors')
const client_id = process.env.CLIENT_ID
const scope = process.env.SCOPE
const redirect_uri = process.env.REDIRECT_URI

const app = express()

app.use(cors())
app.use(express.json())


app.get('/', async (req, res) => {
    res.redirect(`https://accounts.google.com/o/oauth2/auth?client_id=${client_id}&redirect_uri=${redirect_uri}/callback&response_type=code&scope=${scope}`)
})
app.get('/encode', async (req, res) => {
    const {code} = req.body
    const encoded = Buffer.from(code,'base64').toString('utf-8')
    res.send(encoded)
})

app.get('/callback', async (req, res) => {
   console.log(req.query)
})



app.listen(process.env.PORT, "0.0.0.0", () => {
    console.log(`Server is running on port ${process.env.PORT}`)
})