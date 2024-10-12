// controllers/emailController.js
import { sendEmail } from '../services/emailService.js';

export const sendCreditCardNotification = async (req, res) => {
    const { email, cardStatus, cardLastDigits, token, RUV } = req.body;

    // Verificar que todos los datos necesarios estén presentes
    if (!email || !cardStatus || !cardLastDigits || !RUV) {
        return res.status(404).json({ message: 'Faltan datos requeridos para enviar el correo electrónico.' });
    }

    // Verificar que el estado de la tarjeta sea ACEPTADA o RECHAZADA
    if (!['ACEPTADA', 'RECHAZADA'].includes(cardStatus)) {
        return res.status(400).json({ message: 'El estado de la tarjeta debe ser ACEPTADA o RECHAZADA.' });
    }

    const subject = 'Resultado de la inscripción de tarjeta de crédito';
    const message = `
        Estimado usuario,

        El proceso de inscripción de su tarjeta de crédito con los últimos 4 dígitos ${cardLastDigits} ha sido ${cardStatus}.
        ${cardStatus === 'ACEPTADA' ? `El token generado es: ${token}.` : 'No se pudo generar un token.'}
        RUV: ${RUV}

        Gracias por utilizar nuestro servicio.
    `;

    try {
        await sendEmail(email, subject, message);
        res.status(200).json({ message: 'Correo electrónico enviado con éxito.' });
    } catch (error) {
        res.status(500).json({ message: 'Error al enviar el correo electrónico.', error });
    }
};


export const sendUserVerificationNotification = async (req, res) => {
    const { email, userStatus, RUV } = req.body;

    if (!email || !userStatus || !RUV) {
        return res.status(404).json({ message: 'Faltan datos requeridos para enviar el correo electrónico.' });
    }

    if (!['VERIFICADO', 'NO_VERIFICADO'].includes(userStatus)) {
        return res.status(400).json({ message: 'El estado del usuario debe ser VERIFICADO o NO_VERIFICADO.' });
    }

    const subject = 'Resultado del proceso de verificación de usuario';
    const message = `
        Estimado usuario,

        El proceso de verificación de su identidad ha sido ${userStatus}.
        RUV: ${RUV}

        Gracias por utilizar nuestro servicio.
    `;

    try {
        await sendEmail(email, subject, message);
        res.status(200).json({ message: 'Correo electrónico enviado con éxito.' });
    } catch (error) {
        res.status(500).json({ message: 'Error al enviar el correo electrónico.', error });
    }
};