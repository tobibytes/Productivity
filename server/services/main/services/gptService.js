require("dotenv").config();
const {OpenAI} = require("openai");
const getRedis = require('./redis');
const openai = new OpenAI({apiKey: process.env.OpenAI_API_KEY});



async function Analyze({ serviceName, content }) {
    JSON.parse(content).map(async (text) => {
        try {
            const completion = await openai.chat.completions.create({
                model: "gpt-4o-mini",
            messages: [
                { role: "system", content: `Analyze the following item from my ${serviceName} inbox. Please provide a concise title, a summary of the content, and rank it by priority on a scale from 1 (highest) to 100 (lowest) call that score, considering factors like urgency, importance, and time sensitivity. Return the results with a title, summary, priority level, and the source (e.g., Canvas, Gmail, etc.) in JSON format, don't add the json at the top, just the string so i can parse it easily. Also it's also just going to be one announcement, so i just need one json object back. If you feel its not worth to be analyzed, just return an empty object {} (do this often please and when necessary). Here’s the content:` },
                { role: "user", content: JSON.stringify(text) },
            ],
        });
        
        const result = completion.choices[0].message.content;
        let analysis = JSON.parse(result)
        analysis = {...analysis, score: Number(`${analysis.priority_level}.${new Date().valueOf()}`)}
        const redisClient = await getRedis();
        await redisClient.zAdd('todo_analysis', {score: analysis.score, value: JSON.stringify(analysis)})
    } catch (error) {
        console.error("Error analyzing content:", error);
    }
})
}





module.exports = { Analyze };