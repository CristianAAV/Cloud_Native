// routes/emailRoutes.js
import express from 'express';
import { sendCreditCardNotification, sendUserVerificationNotification } from '../controllers/emailController.js';

const router = express.Router();

router.post('/notify-credit-card', sendCreditCardNotification);
router.post('/notify-user-verification', sendUserVerificationNotification);

export default router;
