const Course = require("./models/courses");
const MYCOURSES = ['131540000000038965', '131540000000038005', '131540000000037538', '131540000000039550', '131540000000039695']
async function saveCoursesToDb(courses) {
    try {
    await Course.insertMany(courses)
} catch (err) {
    console.error(`Error adding course to database ${err}`);
}}

function processCoursesForDb(courses) {
    try {
        const validCourses = courses.filter(course => MYCOURSES.includes(course.id))
        const coursesToSave = validCourses.map(course => {
            return {
                id: course.id,
                name: course.name,
                account_id: course.account_id,

                course_code: course.course_code,
                calendar: {
                    ics: course.calendar.ics
                },
                time_zone: course.time_zone,
                course_format: course.course_format
            }
        })
        return coursesToSave
    } catch (err) {
        console.error(`Error processing courses for db ${err}`);
    }
}


function processAnnouncementsForKafka(announcements) {
    try {
        const announcementsToSave = announcements.map(announcement => {
            return {
                title: announcement.title,
                created_at: announcement.created_at,
                url: announcement.url,
                context_code: announcement.context_code,
                message: announcement.message,
                todo_date: announcement.todo_date,
            }
        })
        return JSON.stringify(announcementsToSave)
    } catch (err) {
        console.error(`Error processing announcements for kafka ${err}`);
    }
}




module.exports = {
    saveCoursesToDb,
    processCoursesForDb,
    MYCOURSES, 
    processAnnouncementsForKafka
}