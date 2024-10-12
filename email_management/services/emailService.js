// services/emailService.js
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
    host: process.env.MAIL_HOST,
    port: process.env.MAIL_PORT,
    secure: process.env.MAIL_ENCRYPTION === 'ssl', 
    auth: {
        user: process.env.MAIL_USERNAME,
        pass: process.env.MAIL_PASSWORD,
    },
});

export const sendEmail = async (to, subject, text) => {
    const mailOptions = {
        from: process.env.MAIL_FROM_ADDRESS,
        to,
        subject,
        text,
    };

    try {
        await transporter.sendMail(mailOptions);
        console.log(`Email sent to ${to}`);
    } catch (error) {
        console.error('Error sending email:', error);
    }
};
